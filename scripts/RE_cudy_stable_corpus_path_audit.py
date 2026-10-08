#!/usr/bin/env python3
from pathlib import Path
import zipfile, subprocess, tempfile, hashlib, csv, re, shutil, sys, collections

if len(sys.argv) != 3:
    raise SystemExit("usage: script STABLE_ROOT OUTPUT_DIR")
root=Path(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)

path_rx=re.compile(r'(?:^|[/_.-])(debug|develop|developer|research|factory|manufactur(?:e|ing)?|production|test|diag|terminal|sandbox|telnet|dropbear|ssh|console|uart|recovery|rescue|failsafe|airdump|tcpdump|batchcmd|firstboot|preset|forbidden|hcshd|rom_[a-z0-9_-]+|mtd|flash|backup|restore|calib(?:ration)?|aging|burnin|ate|eng(?:ineering)?|support)(?:$|[/_.-])',re.I)
marker_names={
 'etc/rom_research','etc/rom_develop','etc/rom_dbg','etc/rom_release','etc/rom_alpha',
 'usr/lib/lua/luci/forbidden.lua','usr/lib/lua/luci/model/cbi/system/sandbox.lua',
 'usr/lib/lua/luci/controller/ssh.lua','usr/lib/lua/cmagent/router/ssh.lua',
 'usr/lib/lua/cmagent/router/batchcmd.lua','usr/lib/lua/cmagent/router/tcpdump.lua',
 'usr/lib/lua/cmagent/router/diag.lua','usr/sbin/hcshd','usr/sbin/mesh_tcpdump.sh','usr/sbin/mesh_diag.sh'
}
def run(cmd, timeout=120):
    try:
        return subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout,check=False)
    except subprocess.TimeoutExpired:
        class R: returncode=124; stdout='TIMEOUT'
        return R()
def sha_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for ch in iter(lambda:f.read(1024*1024),b''): h.update(ch)
    return h.hexdigest()

zips=sorted(root.rglob('*.zip'))
manifest=[]; path_presence=collections.defaultdict(set); fw_paths={}; marker_rows=[]; interesting_rows=[]
with tempfile.TemporaryDirectory(prefix='cudy-all-') as td:
    td=Path(td)
    for zi,zp in enumerate(zips,1):
        fwtag=zp.stem
        print(f'[{zi}/{len(zips)}] {fwtag}',flush=True)
        work=td/'work'; shutil.rmtree(work,ignore_errors=True); work.mkdir()
        try:
            with zipfile.ZipFile(zp) as zf:
                cands=[n for n in zf.namelist() if n.lower().endswith(('.bin','.img','.trx','.itb')) and not n.endswith('/')]
                if not cands:
                    manifest.append([fwtag,str(zp.relative_to(root)),'','','NO_INNER_FIRMWARE','','']); continue
                info=max((zf.getinfo(n) for n in cands),key=lambda x:x.file_size)
                fw=work/'firmware.bin'
                with zf.open(info) as src, open(fw,'wb') as dst: shutil.copyfileobj(src,dst)
        except Exception as e:
            manifest.append([fwtag,str(zp.relative_to(root)),'','','ZIP_ERROR',str(e),'']); continue
        b=fw.read_bytes(); offs=[]; pos=0
        while True:
            i=b.find(b'hsqs',pos)
            if i<0: break
            offs.append(i); pos=i+1
        sq=None; sqoff=None
        for off in offs[:32]:
            cand=work/f'root-{off:x}.sqfs'; cand.write_bytes(b[off:])
            s=run(['unsquashfs','-s',str(cand)],30)
            if s.returncode==0: sq=cand; sqoff=off; break
        if sq is None:
            manifest.append([fwtag,str(zp.relative_to(root)),info.filename,info.file_size,'NO_SQUASHFS','','']); continue
        dst=work/'root'
        p=run(['unsquashfs','-no-progress','-d',str(dst),str(sq)],180)
        if p.returncode!=0 or not dst.exists():
            manifest.append([fwtag,str(zp.relative_to(root)),info.filename,info.file_size,'EXTRACT_FAIL',hex(sqoff),p.stdout[-500:]]); continue
        paths=[]
        for q in dst.rglob('*'):
            try: isentry=q.is_file() or q.is_symlink()
            except: isentry=False
            if not isentry: continue
            rel=q.relative_to(dst).as_posix(); paths.append(rel); path_presence[rel].add(fwtag)
        fw_paths[fwtag]=set(paths)
        manifest.append([fwtag,str(zp.relative_to(root)),info.filename,info.file_size,'OK',hex(sqoff),len(paths)])
        for rel in sorted(marker_names):
            q=dst/rel
            if q.exists() or q.is_symlink():
                try: size=q.lstat().st_size
                except: size=-1
                h=''; kind='symlink' if q.is_symlink() else 'file'
                if q.is_file() and size<=2_000_000:
                    try: h=sha_file(q)
                    except: pass
                marker_rows.append([fwtag,rel,kind,size,h])
        for rel in paths:
            if not (path_rx.search(rel) or rel in marker_names): continue
            q=dst/rel
            try: size=q.lstat().st_size
            except: size=-1
            evidence=''
            if q.is_file() and 0<=size<=2_000_000:
                try:
                    raw=q.read_bytes()
                    txt=raw.decode('utf-8','ignore') if b'\x00' not in raw[:4096] else run(['strings','-a','-n','5',str(q)],10).stdout
                    needles=[]
                    for term in ['technical support','debug','factory','research','rom_release','rom_dbg','rom_develop','rom_alpha','rom_research','batchcmd','tcpdump','telnet','dropbear','ssh','console','uart','recovery','failsafe','firstboot','preset','calibration','manufacturing','production','test only']:
                        if term.lower() in txt.lower(): needles.append(term)
                    evidence=';'.join(needles)
                except: pass
            interesting_rows.append([fwtag,rel,size,evidence])

with open(out/'RE-STABLE-CORPUS-EXTRACTION.tsv','w',newline='') as f:
    w=csv.writer(f,delimiter='\t'); w.writerow(['firmware','package','inner','inner_size','status','squashfs_offset','entry_count_or_error']); w.writerows(manifest)
with open(out/'RE-STABLE-CORPUS-MARKERS.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['firmware','path','kind','size','sha256']); w.writerows(marker_rows)
with open(out/'RE-STABLE-CORPUS-INTERESTING-PATHS.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['firmware','path','size','content_markers']); w.writerows(interesting_rows)
with open(out/'RE-STABLE-CORPUS-PATH-RARITY.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['path','count','firmwares','interesting'])
    for rel,s in sorted(path_presence.items(),key=lambda x:(len(x[1]),x[0])):
        w.writerow([rel,len(s),';'.join(sorted(s)),bool(path_rx.search(rel) or rel in marker_names)])

rank=[]
for fw,rel,size,evidence in interesting_rows:
    cnt=len(path_presence.get(rel,()))
    score=10 if cnt==1 else 7 if cnt<=2 else 4 if cnt<=4 else 2 if cnt<=8 else 0
    if rel in marker_names: score+=10
    if re.search(r'rom_(research|develop|dbg|alpha)|batchcmd|hcshd|mesh_tcpdump|mesh_diag|controller/ssh|cmagent/router/ssh',rel,re.I): score+=8
    if evidence: score+=min(8,2*len(evidence.split(';')))
    rank.append([score,fw,rel,cnt,size,evidence])
rank.sort(key=lambda r:(-r[0],r[1],r[2]))
with open(out/'RE-STABLE-CORPUS-RANKING.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['score','firmware','path','presence_count','size','content_markers']); w.writerows(rank)

by_family=collections.defaultdict(list)
for fw in fw_paths:
    m=re.match(r'(.+?-R\d+)',fw,re.I); by_family[m.group(1) if m else fw].append(fw)
diffdir=out/'RE-FAMILY-DIFFS'; diffdir.mkdir()
for fam,items in sorted(by_family.items()):
    if len(items)<2: continue
    items=sorted(items)
    for a,b in zip(items,items[1:]):
        A=fw_paths[a]; B=fw_paths[b]
        ia=sorted(p for p in B-A if path_rx.search(p) or p in marker_names)
        ir=sorted(p for p in A-B if path_rx.search(p) or p in marker_names)
        (diffdir/f'RE-{a}-TO-{b}.txt').write_text(
            f'{a} -> {b}\nadded={len(B-A)} removed={len(A-B)} common={len(A&B)}\n\n=== INTERESTING ADDED ===\n'+'\n'.join(ia)+'\n\n=== INTERESTING REMOVED ===\n'+'\n'.join(ir)+'\n')

ok=[r for r in manifest if r[4]=='OK']
md=['# Cudy stable corpus anomaly audit — pass 02','',f'- Packages scanned: {len(zips)}',f'- SquashFS roots extracted: {len(ok)}',f'- Unique paths across extracted roots: {len(path_presence)}','', '## Cross-firmware markers']
for r in marker_rows: md.append(f'- {r[0]} | `{r[1]}` | size={r[3]} | sha256={r[4]}')
md += ['','## Highest rarity/engineering candidates']
for r in rank[:250]: md.append(f'- score {r[0]:02d} | {r[1]} | `{r[2]}` | corpus={r[3]} | size={r[4]} | {r[5]}')
(out/'RE-STABLE-CORPUS-SUMMARY.md').write_text('\n'.join(md)+'\n')
print(f'scanned={len(zips)} extracted={len(ok)} unique_paths={len(path_presence)} ranked={len(rank)}')
