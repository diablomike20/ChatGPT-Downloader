#!/usr/bin/env python3
from pathlib import Path
import sys,csv,hashlib,subprocess,shutil,re,collections

if len(sys.argv)!=4:
    raise SystemExit("usage: RE-C200P-ROM-RESEARCH-DEEP-AUDIT.py INPUT_DIR ROOTS_DIR OUT_DIR")

inp=Path(sys.argv[1]).resolve()
roots=Path(sys.argv[2]).resolve()
out=Path(sys.argv[3]).resolve()
out.mkdir(parents=True,exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda:f.read(1024*1024),b""): h.update(ch)
    return h.hexdigest()

beta_names=[n for n in sorted(p.stem for p in inp.glob("*.bin")) if n.startswith("BETA-")]
needle_variants=[b"rom_research",b"/etc/rom_research",b"ROM_RESEARCH",b"research"]
raw_rows=[]
for name in beta_names:
    p=inp/(name+".bin")
    b=p.read_bytes()
    low=b.lower()
    for needle in needle_variants:
        target=needle.lower(); pos=0; count=0
        while True:
            i=low.find(target,pos)
            if i<0: break
            raw_rows.append([name,needle.decode("ascii","replace"),i,hex(i)])
            count+=1; pos=i+1
            if count>=500: break

with (out/"RE-ROM-RESEARCH-RAW-OFFSETS.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["firmware","needle","offset_dec","offset_hex"]); w.writerows(raw_rows)

consumer_rows=[]; marker_rows=[]
for name in beta_names:
    root=roots/name
    if not root.exists(): continue
    marker=root/"etc/rom_research"
    marker_rows.append([name,int(marker.exists()),
        marker.stat().st_size if marker.exists() else "",
        sha(marker) if marker.exists() and marker.is_file() else ""])
    for p in root.rglob("*"):
        try:
            if not p.is_file(): continue
            data=p.read_bytes()
        except: continue
        rel=p.relative_to(root).as_posix(); low=data.lower()
        for needle in (b"rom_research",b"/etc/rom_research"):
            if needle in low and rel!="etc/rom_research":
                offs=[]; pos=0
                while True:
                    i=low.find(needle,pos)
                    if i<0: break
                    offs.append(hex(i)); pos=i+1
                    if len(offs)>=50: break
                consumer_rows.append([name,rel,len(data),sha(p),needle.decode(),";".join(offs)])
        if b"research" in low and rel!="etc/rom_research":
            consumer_rows.append([name,rel,len(data),sha(p),"research-lead",""])

with (out/"RE-ROM-RESEARCH-MARKER-MATRIX.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["firmware","marker_present","size","sha256"]); w.writerows(marker_rows)
with (out/"RE-ROM-RESEARCH-CONSUMER-HITS.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["firmware","path","size","sha256","match_type","offsets"]); w.writerows(consumer_rows)

selected=[
"usr/lib/lua/cmagent/router/batchcmd.lua","usr/lib/lua/cmagent/router/ssh.lua",
"usr/lib/lua/cmagent/router/diag.lua","usr/lib/lua/cmagent/router/tcpdump.lua",
"usr/lib/lua/cmagent/router/sysreport.lua","usr/lib/lua/cmagent.lua",
"usr/lib/lua/mickedebug.lua","usr/lib/lua/luci/controller/ssh.lua",
"usr/lib/lua/luci/model/cbi/ssh/ssh.lua","usr/lib/lua/luci/model/cbi/mesh/ssh.lua",
"usr/lib/lua/luci/view/ssh/ssh_button.htm","usr/lib/lua/luci/controller/apcontroller.lua",
"usr/lib/lua/luci/model/cbi/apcontroller/client_view.lua",
"usr/lib/lua/luci/model/cbi/apcontroller/client_view_debug.lua",
"usr/lib/lua/luci/model/cbi/apcontroller/client_view_tcpdump.lua",
"usr/lib/lua/luci/view/apcontroller/diag_log_button.htm",
"usr/lib/lua/luci/model/cbi/diag/mesh.lua","usr/sbin/mesh_diag.sh",
"usr/sbin/mesh_tcpdump.sh","etc/init.d/cmagent","usr/sbin/cmagent",
"etc/init.d/activate","usr/sbin/activate","usr/lib/lua/luci/controller/autoupgrade.lua",
"usr/lib/lua/luci/model/cbi/autoupgrade/localupdate.lua"
]

root_names=sorted(p.name for p in roots.iterdir() if p.is_dir())
matrix=[]; hash_groups=collections.defaultdict(list)
for rel in selected:
    for name in root_names:
        p=roots/name/rel
        if p.is_file():
            h=sha(p); matrix.append([rel,name,1,p.stat().st_size,h]); hash_groups[(rel,h)].append(name)
        else:
            matrix.append([rel,name,0,"",""])

with (out/"RE-C200P-CROSSMODEL-FILE-MATRIX.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["path","firmware","present","size","sha256"]); w.writerows(matrix)

md=["# C200P engineering/control-plane cross-model hash groups","",
    "Identical SHA-256 means byte-for-byte identical file payload.",""]
for rel in selected:
    md.append("## "+rel)
    groups=[(h,names) for (r,h),names in hash_groups.items() if r==rel]
    if not groups: md.append("- ABSENT in all selected roots")
    for h,names in sorted(groups,key=lambda x:(-len(x[1]),x[0])):
        md.append("- "+h+" — "+", ".join(sorted(names)))
    absent=[n for n in root_names if not (roots/n/rel).is_file()]
    if absent: md.append("- absent: "+", ".join(absent))
    md.append("")
(out/"RE-C200P-CROSSMODEL-HASH-GROUPS.md").write_text("\n".join(md)+"\n")

ev=out/"RE-EVIDENCE-FILES"
candidates=[n for n in root_names if n.startswith("C200P-")]
c200p=candidates[0] if candidates else None
if c200p:
    for rel in selected:
        src=roots/c200p/rel
        if not src.is_file(): continue
        dst=ev/c200p/rel; dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dst,follow_symlinks=False)

if c200p:
    cm=roots/c200p/"usr/sbin/cmagent"
    if cm.is_file():
        s=subprocess.run(["strings","-a","-t","x",str(cm)],stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL,text=True,check=False).stdout
        rx=re.compile(r"mqtt|publish|service_call|/usr/lib/lua/cmagent|call:|send:|payload|topic|jwt|broker|client",re.I)
        (out/"RE-C200P-CMAGENT-DISPATCH-STRINGS.txt").write_text(
            "\n".join(line for line in s.splitlines() if rx.search(line))+"\n")

if c200p:
    root=roots/c200p; rows=[]
    for p in root.rglob("*"):
        try:
            if not p.is_file(): continue
            d=p.read_bytes()
        except: continue
        rel=p.relative_to(root).as_posix()
        for term in (b"setLevel",b"mickedebug"):
            if term.lower() in d.lower():
                rows.append([rel,term.decode(),p.stat().st_size,sha(p)])
    with (out/"RE-C200P-MICKEDEBUG-REFERENCES.csv").open("w",newline="") as f:
        w=csv.writer(f); w.writerow(["path","term","size","sha256"]); w.writerows(rows)

exact_consumers=[r for r in consumer_rows if r[4] in ("rom_research","/etc/rom_research")]
broad_leads=[r for r in consumer_rows if r[4]=="research-lead"]
summary=["# Deep C200P engineering + beta rom_research audit — machine pass","",
"Evidence scope: STATIC_VERIFIED path/file/byte evidence only.","",
"- beta inputs: "+str(len(beta_names)),
"- extracted roots compared: "+str(len(root_names)),
"- exact rom_research consumer hits outside marker files: "+str(len(exact_consumers)),
"- broad research leads: "+str(len(broad_leads)),"","## rom_research result"]
if exact_consumers:
    summary.append("- Exact literal consumer candidates were found; inspect RE-ROM-RESEARCH-CONSUMER-HITS.csv.")
else:
    summary += [
      "- No extracted userland file outside /etc/rom_research contains the exact rom_research or /etc/rom_research literal.",
      "- Therefore marker presence is STATIC_VERIFIED, but direct consumer semantics remain UNKNOWN at this pass.",
      "- Broad research matches are leads only and must not be treated as consumers."
    ]
summary += ["","## Cross-model scope"]+["- "+n for n in root_names]
(out/"RE-DEEP-AUDIT-MACHINE-SUMMARY.md").write_text("\n".join(summary)+"\n")

hl=[]
for p in sorted(out.rglob("*")):
    if p.is_file() and p.name!="RE-SHA256SUMS.txt":
        hl.append(sha(p)+"  "+p.relative_to(out).as_posix())
(out/"RE-SHA256SUMS.txt").write_text("\n".join(hl)+"\n")
print("beta",len(beta_names),"roots",len(root_names),"exact_consumers",len(exact_consumers),"broad_leads",len(broad_leads))
