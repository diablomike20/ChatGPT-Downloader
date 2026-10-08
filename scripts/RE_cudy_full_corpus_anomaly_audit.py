#!/usr/bin/env python3
from pathlib import Path
import sys, subprocess, shutil, csv, re, collections, hashlib, os

if len(sys.argv)!=3:
    raise SystemExit("usage: RE_cudy_full_corpus_anomaly_audit.py INPUT_DIR OUT_DIR")
inp=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve()
roots=Path("/tmp/full-corpus/roots"); work=Path("/tmp/full-corpus/work")
for p in (out,roots,work): p.mkdir(parents=True,exist_ok=True)

def run(cmd, **kw):
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, check=False, **kw)
    except Exception as e:
        class R: pass
        r=R(); r.returncode=999; r.stdout=str(e); return r

# Extract each firmware using SquashFS first, then UBI.
extract=[]
for fw in sorted(inp.glob("*.bin")):
    name=fw.stem
    b=fw.read_bytes()
    dst=roots/name
    method=""; off=None; ok=False; note=""
    # squashfs candidates
    pos=0; cands=[]
    while True:
        i=b.find(b"hsqs",pos)
        if i<0: break
        cands.append(i); pos=i+1
    for idx,o in enumerate(cands[:24]):
        sq=work/f"{name}-{idx}-{o:x}.sqfs"; sq.write_bytes(b[o:])
        if dst.exists(): shutil.rmtree(dst,ignore_errors=True)
        p=run(["sudo","unsquashfs","-no-progress","-no-exit-code","-d",str(dst),str(sq)],timeout=120)
        if p.returncode==0 and dst.exists():
            run(["sudo","chmod","-R","a+rX",str(dst)],timeout=60)
            method="squashfs";off=o;ok=True;break
        shutil.rmtree(dst,ignore_errors=True)
    # UBI fallback — reproduce the FU7 P2 extractor: split volumes first,
    # then extract UBIFS filesystem(s), rather than assuming the whole trailing
    # image is one UBIFS volume.
    if not ok:
        u=b.find(b"UBI#")
        if u>=0:
            ubi=work/f"{name}-{u:x}.ubi"; ubi.write_bytes(b[u:])
            vol_dir=work/f"{name}-ubi-volumes"
            file_dir=work/f"{name}-ubi-files"
            shutil.rmtree(vol_dir,ignore_errors=True); vol_dir.mkdir(parents=True,exist_ok=True)
            shutil.rmtree(file_dir,ignore_errors=True); file_dir.mkdir(parents=True,exist_ok=True)

            pi=run(["ubireader_extract_images","-o",str(vol_dir),str(ubi)],timeout=180)
            notes=[pi.stdout[-1000:]]

            # Direct file extraction may succeed even if the image length has
            # harmless trailing bytes.
            pf=run(["ubireader_extract_files","-o",str(file_dir),str(ubi)],timeout=180)
            notes.append(pf.stdout[-1000:])

            candidates=[]
            for base in (file_dir,vol_dir):
                for q in base.rglob("*"):
                    try:
                        if not q.is_dir(): continue
                        score=sum((q/x).exists() for x in ["etc","usr","bin","sbin","www","lib"])
                        if score>=3:
                            count=sum(1 for z in q.rglob("*") if z.is_file() or z.is_symlink())
                            candidates.append((score,count,q))
                    except: pass

            # If split volumes are raw UBIFS, extract each one independently.
            for vol in vol_dir.rglob("*"):
                try:
                    if not vol.is_file(): continue
                    head=vol.read_bytes()[:4]
                except: continue
                if head==b"hsqs":
                    vd=work/f"{name}-vol-{vol.name}-sqfs"
                    shutil.rmtree(vd,ignore_errors=True)
                    pr=run(["sudo","unsquashfs","-no-progress","-no-exit-code","-d",str(vd),str(vol)],timeout=120)
                    if vd.exists():
                        run(["sudo","chmod","-R","a+rX",str(vd)],timeout=60)
                        candidates.append((6,sum(1 for z in vd.rglob("*") if z.is_file() or z.is_symlink()),vd))
                else:
                    vd=work/f"{name}-vol-{vol.name}-files"
                    shutil.rmtree(vd,ignore_errors=True); vd.mkdir(parents=True,exist_ok=True)
                    pr=run(["ubireader_extract_files","-o",str(vd),str(vol)],timeout=120)
                    for q in vd.rglob("*"):
                        try:
                            if not q.is_dir(): continue
                            score=sum((q/x).exists() for x in ["etc","usr","bin","sbin","www","lib"])
                            if score>=3:
                                count=sum(1 for z in q.rglob("*") if z.is_file() or z.is_symlink())
                                candidates.append((score,count,q))
                        except: pass

            if candidates:
                candidates.sort(key=lambda x:(x[0],x[1]),reverse=True)
                src=candidates[0][2]
                if dst.exists(): run(["sudo","rm","-rf",str(dst)],timeout=60)
                run(["sudo","mkdir","-p",str(dst)],timeout=30)
                cp=run(["sudo","cp","-a",str(src)+"/.",str(dst)+"/"],timeout=180)
                run(["sudo","chmod","-R","a+rX",str(dst)],timeout=60)
                if cp.returncode==0:
                    method="ubi";off=u;ok=True;note=" | ".join(notes)
                else:
                    note=("COPY_FAIL "+cp.stdout+" | "+" | ".join(notes))[:1800]
            else:
                shutil.rmtree(dst,ignore_errors=True)
                note=" | ".join(notes)[:1800]
    extract.append([name,method,hex(off) if off is not None else "", "OK" if ok else "NO_ROOT", note.replace("\n"," ")[:1200]])

with (out/"RE-FULL-EXTRACTION.tsv").open("w",newline="") as f:
    w=csv.writer(f,delimiter="\t"); w.writerow(["firmware","method","offset","status","note"]); w.writerows(extract)

names=sorted(p.name for p in roots.iterdir() if p.is_dir())

# Canonical feature paths. Presence is more reliable than noisy strings.
feature_patterns=[
 ("ROM_RESEARCH", re.compile(r"(^|/)rom_research$",re.I)),
 ("ROM_DEVELOP", re.compile(r"(^|/)rom_develop$",re.I)),
 ("ROM_DBG", re.compile(r"(^|/)rom_dbg$",re.I)),
 ("ROM_RELEASE", re.compile(r"(^|/)rom_release$",re.I)),
 ("TERMINAL", re.compile(r"(terminal\.lua$|/terminal/|terminal\.htm$)",re.I)),
 ("SANDBOX", re.compile(r"sandbox\.lua$",re.I)),
 ("SSH_CONTROL", re.compile(r"(^|/)(ssh\.lua|ssh_button\.htm)$",re.I)),
 ("BATCHCMD", re.compile(r"batchcmd",re.I)),
 ("TCPDUMP_CONTROL", re.compile(r"tcpdump",re.I)),
 ("MESH_DIAG", re.compile(r"mesh_diag|/diag/mesh",re.I)),
 ("DEBUG_MODULE", re.compile(r"mickedebug|debug\.lua|client_view_debug",re.I)),
 ("ACTIVATE", re.compile(r"(^|/)activate$",re.I)),
 ("ATED", re.compile(r"(^|/)ated$|ated_ext",re.I)),
 ("TEST_MODE", re.compile(r"test[-_]?mode",re.I)),
 ("FIRSTBOOT", re.compile(r"firstboot",re.I)),
 ("PRESET", re.compile(r"(^|/)preset(\.lua)?$",re.I)),
 ("RECOVERY", re.compile(r"recovery|rescue|failsafe",re.I)),
 ("AIR_DUMP", re.compile(r"airdump",re.I)),
 ("LOCALUPDATE", re.compile(r"localupdate",re.I)),
 ("HC_SHD", re.compile(r"hcshd",re.I)),
 ("OEM_CHECK", re.compile(r"oem-check|oem_check",re.I)),
 ("SERIAL_UART", re.compile(r"serial|uart",re.I)),
 ("FACTORY_PATH", re.compile(r"factory",re.I)),
]
interesting_path=re.compile(
 r"debug|develop|research|factory|manufact|production|test|diag|terminal|sandbox|telnet|dropbear|ssh|"
 r"console|uart|recovery|rescue|failsafe|airdump|tcpdump|batchcmd|firstboot|preset|forbidden|"
 r"hcshd|rom_[a-z0-9_-]+|mtd|backup|restore|calib|aging|burn|ate|eng|support|localupdate",re.I)

presence=collections.defaultdict(set); sizes={}
features=collections.defaultdict(lambda:collections.defaultdict(list))
for name in names:
    root=roots/name
    for p in root.rglob("*"):
        try:
            if not (p.is_file() or p.is_symlink()): continue
        except: continue
        rel=p.relative_to(root).as_posix()
        presence[rel].add(name)
        try:sizes[(name,rel)]=p.lstat().st_size
        except:sizes[(name,rel)]=0
        for fid,rx in feature_patterns:
            if rx.search(rel): features[fid][name].append(rel)

with (out/"RE-FULL-PATH-RARITY.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["path","count","firmwares","interesting"])
    for rel,s in sorted(presence.items(),key=lambda kv:(len(kv[1]),kv[0])):
        w.writerow([rel,len(s),";".join(sorted(s)),int(bool(interesting_path.search(rel)))])

with (out/"RE-FULL-UNIQUE-INTERESTING.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["firmware","path","size"])
    for rel,s in sorted(presence.items()):
        if len(s)==1 and interesting_path.search(rel):
            n=next(iter(s));w.writerow([n,rel,sizes.get((n,rel),0)])

with (out/"RE-FEATURE-PRESENCE.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["feature","firmware","paths"])
    for fid in sorted(features):
        for n in sorted(features[fid]):
            w.writerow([fid,n,";".join(sorted(features[fid][n]))])

# Targeted terms in scripts/Lua/config and small binaries.
terms=[
 "rom_research","rom_develop","rom_dbg","rom_release","testonly.js","hcshd",
 "technical support","debugging purposes","batchcmd","mesh_tcpdump","mesh_diag",
 "debug_mode","factorytest","pintest","manufacturing","production","research",
 "developer","dropbear","telnetd","authorized_keys","os.execute","luci.util.exec",
 "sysupgrade","oem-check","firstboot","airdump","tcpdump","ated","test mode"
]
rx=re.compile("|".join(re.escape(t) for t in terms),re.I)
hits=[]
for n in names:
    root=roots/n
    for p in root.rglob("*"):
        try:
            if not p.is_file(): continue
            sz=p.stat().st_size
        except: continue
        rel=p.relative_to(root).as_posix()
        # Focus on source/config/control-plane plus small binaries.
        focus=(sz<=350_000 or rel.startswith(("etc/","usr/lib/lua/","usr/lib/diag/","usr/sbin/","usr/bin/")))
        if not focus or sz>3_000_000: continue
        try:
            data=p.read_bytes()
            # for bytecode/binary use strings
            if b"\x00" in data[:4096]:
                txt=run(["strings","-a","-n","5",str(p)],timeout=8).stdout
            else:
                txt=data.decode("utf-8","ignore")
        except: continue
        m=sorted(set(x.group(0).lower() for x in rx.finditer(txt)))
        if m: hits.append([n,rel,sz,";".join(m)])

with (out/"RE-FULL-TARGETED-STRING-HITS.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["firmware","path","size","terms"]);w.writerows(hits)

# Rarity ranking, emphasize true unique controls and explicit markers.
hitmap=collections.defaultdict(set)
for n,rel,sz,ts in hits: hitmap[(n,rel)].update(ts.split(";"))
rank=[]
for rel,s in presence.items():
    for n in s:
        score=0
        if len(s)==1: score+=16
        elif len(s)==2: score+=10
        elif len(s)<=4: score+=5
        if interesting_path.search(rel): score+=8
        ts=hitmap.get((n,rel),set())
        score+=min(12,3*len(ts))
        if any(k in rel.lower() for k in ["rom_research","rom_develop","rom_dbg","batchcmd","mesh_tcpdump","mesh_diag","mickedebug","/ssh/","controller/ssh","test-mode"]): score+=8
        if score>=13:
            rank.append([score,n,rel,len(s),";".join(sorted(ts))])
rank.sort(key=lambda x:(-x[0],x[1],x[2]))
with (out/"RE-FULL-ANOMALY-RANKING.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["score","firmware","path","corpus_count","terms"]);w.writerows(rank)

# Family-specific marker report.
family=lambda n:n.split("__",1)[0] if "__" in n else n.split("-",1)[0]
md=["# Full Cudy corpus anomaly audit — pass 02","",
    "STATIC_VERIFIED path/string inventory. Rarity is triage, not intent proof.","",
    f"- input images: {len(list(inp.glob('*.bin')))}",
    f"- extracted roots: {len(names)}",
    f"- ranked candidates: {len(rank)}","",
    "## Extraction failures"]
for r in extract:
    if r[3]!="OK": md.append(f"- {r[0]}: {r[4] or 'NO_ROOT'}")
md += ["","## Explicit feature/marker distribution"]
for fid in sorted(features):
    arr=sorted(features[fid])
    if arr:
        md.append(f"- **{fid}**: {len(arr)} firmware(s): "+", ".join(arr))
md += ["","## Top rarity candidates"]
for r in rank[:250]:
    md.append(f"- {r[0]:02d} | {r[1]} | `{r[2]}` | corpus={r[3]} | {r[4]}")
(out/"RE-FULL-CORPUS-SUMMARY.md").write_text("\n".join(md)+"\n")

# hashes
hl=[]
for p in sorted(out.rglob("*")):
    if p.is_file() and p.name!="RE-SHA256SUMS.txt":
        h=hashlib.sha256()
        with p.open("rb") as f:
            for ch in iter(lambda:f.read(1024*1024),b""):h.update(ch)
        hl.append(f"{h.hexdigest()}  {p.relative_to(out).as_posix()}")
(out/"RE-SHA256SUMS.txt").write_text("\n".join(hl)+"\n")
print("inputs",len(list(inp.glob("*.bin"))),"roots",len(names),"ranked",len(rank))
