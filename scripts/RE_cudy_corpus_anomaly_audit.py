#!/usr/bin/env python3
from pathlib import Path
import sys, subprocess, shutil, csv, re, collections, os, hashlib

if len(sys.argv) != 3:
    raise SystemExit("usage: RE_cudy_corpus_anomaly_audit.py INPUT_DIR OUTPUT_DIR")

inp=Path(sys.argv[1]).resolve()
out=Path(sys.argv[2]).resolve()
work=Path("/tmp/corpus/work")
roots=Path("/tmp/corpus/roots")
bw=Path("/tmp/corpus/binwalk")
for p in (out,work,roots,bw):
    p.mkdir(parents=True,exist_ok=True)

def run(cmd, **kw):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, check=False, **kw)

# ---- extraction ----
extract_rows=[['firmware','method','offset','status','root']]
for fw in sorted(inp.glob("*.bin")):
    name=fw.stem
    b=fw.read_bytes()
    pos=0
    candidates=[]
    while True:
        i=b.find(b"hsqs",pos)
        if i<0: break
        candidates.append(i); pos=i+1
    success=False
    for idx,off in enumerate(candidates[:32]):
        sq=work/f"{name}-{idx}-{off:x}.sqfs"
        sq.write_bytes(b[off:])
        dst=roots/name
        if dst.exists(): shutil.rmtree(dst,ignore_errors=True)
        p=run(["unsquashfs","-no-progress","-d",str(dst),str(sq)])
        if p.returncode==0 and dst.exists():
            extract_rows.append([name,"squashfs",hex(off),"OK",str(dst)])
            success=True
            break
        shutil.rmtree(dst,ignore_errors=True)
    if not success:
        d=bw/name
        d.mkdir(parents=True,exist_ok=True)
        log=out/f"RE-BINWALK-{name}.log"
        with log.open("w") as lf:
            p=subprocess.run(["binwalk","-Me","--run-as=root",str(fw)],
                             cwd=d,stdout=lf,stderr=subprocess.STDOUT,text=True,
                             timeout=240,check=False)
        # Binwalk may create restrictive dirs.
        subprocess.run(["chmod","-R","a+rX",str(d)],check=False)
        cand=[]
        for pth in d.rglob("*"):
            try:
                if not pth.is_dir(): continue
                score=sum((pth/x).exists() for x in ["etc","usr","bin","sbin","www","lib"])
                if score>=3:
                    count=sum(1 for q in pth.rglob("*") if q.is_file() or q.is_symlink())
                    cand.append((score,count,pth))
            except Exception:
                continue
        if cand:
            cand.sort(key=lambda x:(x[0],x[1]),reverse=True)
            src=cand[0][2]
            dst=roots/name
            shutil.copytree(src,dst,symlinks=True,dirs_exist_ok=True)
            extract_rows.append([name,"binwalk-root","-", "OK",str(dst)])
        else:
            extract_rows.append([name,"binwalk","-","NO_ROOT_FOUND","-"])

with (out/"RE-EXTRACTION.tsv").open("w",newline="") as f:
    w=csv.writer(f,delimiter="\t");w.writerows(extract_rows)

fw_names=sorted(p.name for p in roots.iterdir() if p.is_dir())

# ---- path rarity / string evidence ----
interesting_path=re.compile(
 r"(debug|develop|research|factory|manufact|production|test|diag|terminal|sandbox|telnet|dropbear|ssh|"
 r"console|uart|recovery|rescue|failsafe|airdump|tcpdump|batchcmd|firstboot|preset|forbidden|"
 r"hcshd|rom_[a-z0-9_-]+|mtd|flash|backup|restore|calib|aging|burn|ate|eng|support)",re.I)

terms=[
 "rom_research","rom_develop","rom_dbg","rom_release","testonly.js",
 "hcshd","terminal","sandbox","telnet","dropbear","sshd","authorized_keys",
 "factory","factorytest","manufacturing","production","engineering","developer",
 "debug","debug_mode","research","pintest","testmode","ate","aging","burnin","calibration",
 "recovery","rescue","failsafe","firstboot","preset","airdump","tcpdump",
 "batchcmd","mesh_tcpdump","mesh_diag","dmesg","logread","console","uart",
 "oem-check","sysupgrade","backup","restore","mtd","flash","shell"
]
termrx=re.compile("|".join(re.escape(x) for x in terms),re.I)

presence=collections.defaultdict(set)
sizes={}
for fw in fw_names:
    root=roots/fw
    for p in root.rglob("*"):
        try:
            is_entry=p.is_file() or p.is_symlink()
        except Exception:
            is_entry=False
        if not is_entry: continue
        rel=p.relative_to(root).as_posix()
        presence[rel].add(fw)
        try:sizes[(fw,rel)]=p.lstat().st_size
        except:sizes[(fw,rel)]=0

with (out/"RE-FILE-RARITY.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["path","firmware_count","firmwares","interesting_path"])
    for rel,s in sorted(presence.items(),key=lambda kv:(len(kv[1]),kv[0])):
        w.writerow([rel,len(s),";".join(sorted(s)),bool(interesting_path.search(rel))])

with (out/"RE-UNIQUE-INTERESTING-PATHS.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["firmware","path","size"])
    for rel,s in sorted(presence.items()):
        if len(s)==1 and interesting_path.search(rel):
            fw=next(iter(s));w.writerow([fw,rel,sizes.get((fw,rel),0)])

hits=[]
for fw in fw_names:
    root=roots/fw
    for p in root.rglob("*"):
        try:
            if not p.is_file(): continue
            sz=p.stat().st_size
        except: continue
        if sz>12_000_000: continue
        rel=p.relative_to(root).as_posix()
        try:
            if sz<=2_000_000:
                text=p.read_bytes().decode("utf-8","ignore")
            else:
                text=run(["strings","-a","-n","5",str(p)],timeout=12).stdout
        except Exception:
            continue
        matches=sorted(set(m.group(0).lower() for m in termrx.finditer(text)))
        if matches:
            hits.append((fw,rel,sz,";".join(matches)))

with (out/"RE-KEYWORD-HITS.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["firmware","path","size","terms"]);w.writerows(hits)

# ---- same-model path diffs ----
pairs=[
 ("P2-BETA","P2-STABLE-2.4.22"),
 ("TR1200-BETA","TR1200-STABLE-2.1.3"),
 ("WR3000-BETA","WR3000-STABLE-2.3.7"),
 ("WR3000-BETA","WR3000-STABLE-2.4.7"),
]
diff_stats=[]
for a,b in pairs:
    if a not in fw_names or b not in fw_names: continue
    A={p.relative_to(roots/a).as_posix() for p in (roots/a).rglob("*") if p.is_file() or p.is_symlink()}
    B={p.relative_to(roots/b).as_posix() for p in (roots/b).rglob("*") if p.is_file() or p.is_symlink()}
    diff_stats.append((a,b,len(A-B),len(B-A),len(A&B)))
    lines=[f"{a} only: {len(A-B)}",f"{b} only: {len(B-A)}",f"common: {len(A&B)}","",
           f"=== {a} ONLY ===",*sorted(A-B),"",f"=== {b} ONLY ===",*sorted(B-A)]
    (out/f"RE-DIFF-{a}-VS-{b}.txt").write_text("\n".join(lines)+"\n")

# ---- score + classify ----
hit_by=collections.defaultdict(set)
for fw,rel,sz,ts in hits:
    hit_by[(fw,rel)].update(ts.split(";"))

def classify(rel, ts):
    t=(" "+rel+" "+" ".join(ts)).lower()
    if any(x in t for x in ["factorytest","manufactur","production","aging","burnin"," ate ","calibr"]):
        return "MANUFACTURING"
    if any(x in t for x in ["rom_research","research","engineering","engpc","developer"]):
        return "ENGINEERING"
    if any(x in t for x in ["debug_mode","rom_dbg","debug","dmesg","logread"]):
        return "DEBUG"
    if any(x in t for x in ["factory","testonly.js","rom_develop"]):
        return "FACTORY"
    if any(x in t for x in ["terminal","sandbox","telnet","dropbear","sshd","hcshd","shell","console","uart"]):
        return "HIDDEN"
    if any(x in t for x in ["recovery","rescue","failsafe","firstboot","preset","backup","restore","sysupgrade","oem-check"]):
        return "INTERNAL-SUPPORT"
    if any(x in t for x in ["airdump","tcpdump","diag","batchcmd","mesh_diag","mesh_tcpdump"]):
        return "INTERNAL-SUPPORT"
    return "UNKNOWN"

rank=[]
for rel,s in presence.items():
    for fw in s:
        ts=hit_by.get((fw,rel),set())
        score=(10 if len(s)==1 else 5 if len(s)<=2 else 0)
        if interesting_path.search(rel): score+=6
        score+=min(12,len(ts)*2)
        if score>=8:
            rank.append((score,fw,rel,len(s),classify(rel,ts),";".join(sorted(ts))))
rank.sort(key=lambda x:(-x[0],x[1],x[2]))

with (out/"RE-ANOMALY-RANKING.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["score","firmware","path","corpus_presence_count","classification","terms"]);w.writerows(rank)

# ---- preserve small high-value files ----
ev=out/"RE-HIGHVALUE-FILES"
for score,fw,rel,count,cls,ts in rank:
    if score<12: continue
    src=roots/fw/rel
    try:
        if not src.is_file() or src.stat().st_size>2_000_000: continue
    except: continue
    dst=ev/fw/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    try: shutil.copy2(src,dst,follow_symlinks=False)
    except: pass

# ---- summary ----
md=[
 "# Cudy firmware corpus anomaly audit — pass 01","",
 "Evidence level: STATIC_VERIFIED for extracted path/file/string presence only.",
 "Rarity is a triage score, not proof of engineering intent.","",
 "## Corpus"
]
for fw in fw_names:
    n=sum(1 for p in (roots/fw).rglob("*") if p.is_file() or p.is_symlink())
    md.append(f"- {fw}: {n} file/symlink entries")
md += ["","## Same-model path diffs"]
for a,b,ao,bo,c in diff_stats:
    md.append(f"- {a} vs {b}: {ao} beta/A-only, {bo} control/B-only, {c} common")
md += ["","## Highest scored candidates"]
for row in rank[:200]:
    md.append(f"- score {row[0]:02d} | {row[4]} | {row[1]} | `{row[2]}` | corpus={row[3]} | {row[5]}")
(out/"RE-CORPUS-ANOMALY-SUMMARY.md").write_text("\n".join(md)+"\n")

# exact per-output hashes
hash_lines=[]
for p in sorted(out.rglob("*")):
    if p.is_file() and p.name!="RE-SHA256SUMS.txt":
        h=hashlib.sha256()
        try:
            with p.open("rb") as f:
                for ch in iter(lambda:f.read(1024*1024),b""):h.update(ch)
            hash_lines.append(f"{h.hexdigest()}  {p.relative_to(out).as_posix()}")
        except: pass
(out/"RE-SHA256SUMS.txt").write_text("\n".join(hash_lines)+"\n")

subprocess.run(["chmod","-R","a+rX",str(out)],check=False)
print(f"firmwares={len(fw_names)}")
print(f"ranked_candidates={len(rank)}")
print(f"roots={fw_names}")
