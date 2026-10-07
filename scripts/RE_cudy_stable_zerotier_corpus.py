#!/usr/bin/env python3
import csv, gzip, hashlib, io, json, lzma, os, re, shutil, subprocess, tarfile, tempfile, zipfile
from pathlib import Path

REPO=Path(".")
STATUS=REPO/"firmware/cudy/stable/RE-CUDY-STABLE-DOWNLOAD-STATUS.tsv"
OUT=REPO/"analysis/zerotier"
OUT.mkdir(parents=True,exist_ok=True)
WORK=Path("/tmp/RE-CUDY-STABLE-ZT-CORPUS")
shutil.rmtree(WORK,ignore_errors=True)
WORK.mkdir(parents=True)

KNOWN_R25_ZT="c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c"

def sha256_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def run(cmd,timeout=120):
    try:
        r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
        return r.returncode,r.stdout
    except Exception as e:
        return 999,repr(e)

def squash_offsets(p):
    data=p.read_bytes()
    out=[]; start=0
    while True:
        i=data.find(b"hsqs",start)
        if i<0: break
        out.append(i); start=i+4
    return out

def extract_images(pkg,idx):
    dest=WORK/f"pkg-{idx}"
    dest.mkdir()
    imgs=[]
    if zipfile.is_zipfile(pkg):
        try:
            with zipfile.ZipFile(pkg) as z:z.extractall(dest)
        except Exception:return []
        for q in dest.rglob("*"):
            if q.is_file() and q.suffix.lower() in {".bin",".img",".trx",".itb",".fw",".rom"}:
                imgs.append(q)
    else:
        imgs=[pkg]
    return imgs

def extract_rootfs(img,idx,off):
    sq=WORK/f"sq-{idx}-{off:x}.bin"
    with open(img,"rb") as f:
        f.seek(off);sq.write_bytes(f.read())
    root=WORK/f"root-{idx}-{off:x}"
    rc,out=run(["unsquashfs","-no-progress","-d",str(root),str(sq)],180)
    return root if root.exists() else None

def read_release(root):
    vals=[]
    for rel in ("etc/openwrt_release","etc/openwrt_version","etc/rom_version","etc/cudy_version"):
        p=root/rel
        if p.exists():
            try:
                v=p.read_text(errors="ignore").strip().replace("\n","; ")
                if v: vals.append(v)
            except:pass
    return " | ".join(vals)[:1000]

def readelf_header(p):
    rc,s=run(["readelf","-h",str(p)],30)
    d={}
    for line in s.splitlines():
        for key in ("Class:","Data:","Machine:","Flags:"):
            if key in line:
                d[key[:-1].lower()]=line.split(key,1)[1].strip()
    rc2,a=run(["readelf","-A",str(p)],30)
    interesting=[]
    for line in a.splitlines():
        st=line.strip()
        if any(x in st for x in ("ISA:","ISA Extension:","FP ABI:","Tag_GNU_MIPS_ABI_FP","ASEs:")):
            interesting.append(st)
    d["attributes"]=" | ".join(interesting)[:1000]
    rc3,ft=run(["file","-b",str(p)],20)
    d["file"]=ft.strip()
    return d

def needed_libs(p):
    rc,s=run(["readelf","-d",str(p)],30)
    return re.findall(r"Shared library: \[(.*?)\]",s)

def soname(p):
    rc,s=run(["readelf","-d",str(p)],30)
    m=re.search(r"Library soname: \[(.*?)\]",s)
    return m.group(1) if m else None

def find_lib(root,name):
    # exact SONAME path first
    for base in (root/"lib",root/"usr/lib"):
        p=base/name
        if p.exists() or p.is_symlink():return p
    # full-tree exact
    for p in root.rglob(name):
        if p.exists() or p.is_symlink():return p
    # versioned fallback
    stem=name.split(".so")[0]+".so"
    for p in root.rglob(stem+"*"):
        if p.is_file() or p.is_symlink():return p
    return None

def real_file(p):
    try:
        if p.is_symlink():
            q=(p.parent/os.readlink(p)).resolve()
            if q.exists():return q
        return p.resolve()
    except:return p

def file_bytes(p):
    q=real_file(p)
    try:return q.read_bytes()
    except:return b""

def target_sonames(root):
    names=set()
    hashes={}
    for base in (root/"lib",root/"usr/lib"):
        if not base.exists():continue
        for p in base.rglob("*"):
            if not (p.is_file() or p.is_symlink()):continue
            names.add(p.name)
            q=real_file(p)
            if q.exists() and q.is_file():
                try:hashes[p.name]=sha256_file(q)
                except:pass
                sn=soname(q)
                if sn:
                    names.add(sn)
                    try:hashes[sn]=sha256_file(q)
                    except:pass
    return names,hashes

def compress_payload(files):
    # files: list[(archive_name, bytes)]
    bio=io.BytesIO()
    with tarfile.open(fileobj=bio,mode="w") as tf:
        for name,data in files:
            ti=tarfile.TarInfo(name)
            ti.size=len(data);ti.mtime=0;ti.uid=0;ti.gid=0;ti.mode=0o755 if "zerotier-one" in name else 0o644
            tf.addfile(ti,io.BytesIO(data))
    tar=bio.getvalue()
    gz=gzip.compress(tar,compresslevel=9,mtime=0)
    xz=lzma.compress(tar,format=lzma.FORMAT_XZ,preset=9|lzma.PRESET_EXTREME)
    return len(tar),len(gz),len(xz)

with open(STATUS,encoding="utf-8",newline="") as f:
    stable=list(csv.DictReader(f,delimiter="\t"))

# Extract every firmware image/rootfs exactly once.
roots=[]
image_counter=0
for si,row in enumerate(stable):
    pkg=Path(row["path"])
    if not pkg.exists():continue
    for img in extract_images(pkg,si):
        ih=sha256_file(img)
        for off in squash_offsets(img)[:4]:
            root=extract_rootfs(img,image_counter,off)
            image_counter+=1
            if root:
                roots.append({
                    "row":row,"package":pkg,"image":img,"image_sha256":ih,
                    "squashfs_offset":off,"root":root,"release":read_release(root)
                })

# Exact target baseline: stock WR1200 V2 / R26.
target=None
for r in roots:
    if r["row"].get("board")=="R26" or "WR1200V2-R26" in r["row"].get("filename",""):
        target=r;break
if not target:
    raise SystemExit("R26 target rootfs not found")
target_names,target_hashes=target_sonames(target["root"])

records=[]
for r in roots:
    root=r["root"]
    zts=[p for p in root.rglob("zerotier-one") if p.is_file() and not p.is_symlink()]
    for zt in zts:
        zh=sha256_file(zt)
        hdr=readelf_header(zt)
        needed=needed_libs(zt)
        additions=[]
        payload=[("usr/bin/zerotier-one",zt.read_bytes())]
        seen_real={str(real_file(zt))}
        unresolved=[]
        for n in needed:
            # If stock R26 already exports this SONAME/name, it is not donor payload.
            if n in target_names:
                additions.append({
                    "needed":n,"status":"R26_PRESENT","donor_path":"","real_name":"",
                    "size":0,"sha256":target_hashes.get(n,"")
                })
                continue
            lp=find_lib(root,n)
            if not lp:
                unresolved.append(n)
                additions.append({"needed":n,"status":"MISSING_IN_DONOR","donor_path":"","real_name":"","size":0,"sha256":""})
                continue
            rp=real_file(lp); key=str(rp)
            b=file_bytes(rp)
            h=hashlib.sha256(b).hexdigest() if b else ""
            additions.append({
                "needed":n,"status":"ADD_FROM_DONOR","donor_path":str(lp.relative_to(root)),
                "real_name":rp.name,"size":len(b),"sha256":h
            })
            if key not in seen_real:
                seen_real.add(key)
                payload.append(("usr/lib/"+rp.name,b))
        logical=sum(len(b) for _,b in payload)
        tar_sz,gz_sz,xz_sz=compress_payload(payload)
        mips_little=("MIPS" in hdr.get("machine","") and "little endian" in hdr.get("data","").lower())
        records.append({
            "family":r["row"].get("family",""),"model":r["row"].get("model",""),"board":r["row"].get("board",""),
            "firmware_version":r["row"].get("version",""),"package":r["row"].get("filename",""),
            "package_sha256":r["row"].get("sha256",""),"image":r["image"].name,"image_sha256":r["image_sha256"],
            "squashfs_offset":hex(r["squashfs_offset"]),"release":r["release"],
            "zerotier_path":str(zt.relative_to(root)),"zerotier_size":zt.stat().st_size,
            "zerotier_sha256":zh,"elf":hdr,"needed":needed,"dependency_resolution":additions,
            "unresolved_needed":unresolved,"r26_direct_elf_compatible":mips_little,
            "r26_payload_logical":logical,"r26_payload_tar":tar_sz,"r26_payload_gzip9":gz_sz,"r26_payload_xz9e":xz_sz,
            "is_known_r25_build":zh==KNOWN_R25_ZT
        })

# Distinct binary + dependency-set builds.
by={}
for r in records:
    dep_sig=tuple((x["needed"],x["status"],x["size"],x["sha256"]) for x in r["dependency_resolution"])
    key=(r["zerotier_sha256"],dep_sig)
    if key not in by:
        z=dict(r);z["provenance"]=[f'{r["model"]}/{r["board"]} {r["firmware_version"]} :: {r["package"]}'];by[key]=z
    else:
        by[key]["provenance"].append(f'{r["model"]}/{r["board"]} {r["firmware_version"]} :: {r["package"]}')

distinct=list(by.values())
distinct.sort(key=lambda r:(not r["r26_direct_elf_compatible"],bool(r["unresolved_needed"]),r["r26_payload_xz9e"],r["r26_payload_gzip9"],r["r26_payload_logical"]))

baseline=next((r for r in distinct if r["is_known_r25_build"]),None)
for r in distinct:
    if baseline:
        r["saving_vs_r25_logical"]=baseline["r26_payload_logical"]-r["r26_payload_logical"]
        r["saving_vs_r25_gzip9"]=baseline["r26_payload_gzip9"]-r["r26_payload_gzip9"]
        r["saving_vs_r25_xz9e"]=baseline["r26_payload_xz9e"]-r["r26_payload_xz9e"]

result={
    "stable_packages":len(stable),"rootfs_images_scanned":len(roots),"zerotier_occurrences":len(records),
    "distinct_zerotier_payloads":len(distinct),
    "target":{
        "package":target["row"]["filename"],"board":target["row"]["board"],"release":target["release"],
        "available_soname_count":len(target_names)
    },
    "known_r25_hash":KNOWN_R25_ZT,
    "baseline":baseline,
    "ranked":distinct
}
json_path=OUT/"RE-CUDY-STABLE-ZEROTIER-CORPUS-01.json"
json_path.write_text(json.dumps(result,indent=2,ensure_ascii=False))

fields=["rank","model","board","firmware_version","zerotier_size","zerotier_sha256","r26_direct_elf_compatible",
        "unresolved_needed","r26_payload_logical","r26_payload_gzip9","r26_payload_xz9e",
        "saving_vs_r25_logical","saving_vs_r25_gzip9","saving_vs_r25_xz9e","needed","provenance"]
with open(OUT/"RE-CUDY-STABLE-ZEROTIER-CORPUS-01.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for i,r in enumerate(distinct,1):
        w.writerow({
            "rank":i,"model":r["model"],"board":r["board"],"firmware_version":r["firmware_version"],
            "zerotier_size":r["zerotier_size"],"zerotier_sha256":r["zerotier_sha256"],
            "r26_direct_elf_compatible":r["r26_direct_elf_compatible"],
            "unresolved_needed":"|".join(r["unresolved_needed"]),
            "r26_payload_logical":r["r26_payload_logical"],"r26_payload_gzip9":r["r26_payload_gzip9"],
            "r26_payload_xz9e":r["r26_payload_xz9e"],
            "saving_vs_r25_logical":r.get("saving_vs_r25_logical",""),
            "saving_vs_r25_gzip9":r.get("saving_vs_r25_gzip9",""),
            "saving_vs_r25_xz9e":r.get("saving_vs_r25_xz9e",""),
            "needed":"|".join(r["needed"]),"provenance":" | ".join(r["provenance"])
        })

md=[
"# RE Cudy stable ZeroTier corpus 01","",
f"- Stable packages: **{len(stable)}**",
f"- Rootfs images scanned: **{len(roots)}**",
f"- ZeroTier occurrences: **{len(records)}**",
f"- Distinct ZeroTier+dependency payloads: **{len(distinct)}**",
f"- Target baseline: **{target['row']['filename']}**","",
"Ranking is by direct R26 ELF compatibility, resolved dependencies, then XZ footprint.","",
"| Rank | Donor | ZT bytes | R26 payload | gzip-9 | XZ-9e | Δ XZ vs R25 | Direct R26 ELF | ZT SHA |",
"|---:|---|---:|---:|---:|---:|---:|---|---|"
]
for i,r in enumerate(distinct,1):
    md.append(
        f'| {i} | {r["model"]}/{r["board"]} {r["firmware_version"]} | {r["zerotier_size"]} | '
        f'{r["r26_payload_logical"]} | {r["r26_payload_gzip9"]} | {r["r26_payload_xz9e"]} | '
        f'{r.get("saving_vs_r25_xz9e","")} | {"YES" if r["r26_direct_elf_compatible"] else "NO"} | '
        f'`{r["zerotier_sha256"][:16]}…` |'
    )
md += ["","## Dependency details"]
for i,r in enumerate(distinct,1):
    md.append(f'### {i}. {r["model"]}/{r["board"]} {r["firmware_version"]}')
    md.append(f'- ZT SHA-256: `{r["zerotier_sha256"]}`')
    md.append(f'- ELF: {r["elf"].get("file","")}')
    md.append(f'- Attributes: {r["elf"].get("attributes","")}')
    md.append(f'- NEEDED: {", ".join(r["needed"]) or "(none)"}')
    for d in r["dependency_resolution"]:
        md.append(f'- {d["needed"]}: {d["status"]} {d["real_name"]} {d["size"]} B {d["sha256"]}')
    md.append(f'- Provenance: {"; ".join(r["provenance"])}')
(OUT/"RE-CUDY-STABLE-ZEROTIER-CORPUS-01.md").write_text("\n".join(md)+"\n")

print(json.dumps({
    "stable_packages":len(stable),"rootfs_images_scanned":len(roots),
    "zerotier_occurrences":len(records),"distinct":len(distinct),
    "best":({
        "model":distinct[0]["model"],"board":distinct[0]["board"],"version":distinct[0]["firmware_version"],
        "zt_size":distinct[0]["zerotier_size"],"payload_logical":distinct[0]["r26_payload_logical"],
        "gzip9":distinct[0]["r26_payload_gzip9"],"xz9e":distinct[0]["r26_payload_xz9e"],
        "sha":distinct[0]["zerotier_sha256"]
    } if distinct else None)
},indent=2))
