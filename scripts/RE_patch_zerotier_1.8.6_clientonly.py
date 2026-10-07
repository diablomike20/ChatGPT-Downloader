#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()

# 1. Stop linking the embedded local controller/database implementation.
p=root/"objects.mk"
lines=p.read_text().splitlines()
controller_objs={
    "controller/EmbeddedNetworkController.o",
    "controller/DBMirrorSet.o",
    "controller/DB.o",
    "controller/FileDB.o",
    "controller/LFDB.o",
    "controller/PostgreSQL.o",
}
removed=[]
kept=[]
for line in lines:
    key=line.strip().rstrip("\\").strip()
    if key in controller_objs:
        removed.append(key)
    else:
        kept.append(line)
if set(removed) != controller_objs:
    raise SystemExit(f"controller objects mismatch: removed={removed}")
p.write_text("\n".join(kept)+"\n")

# 2. Make OneService a pure client: no local network controller instance,
# no /controller management endpoints, no controller remote-trace dispatch.
p=root/"service/OneService.cpp"
s=p.read_text()

patches=[
(
"""\t\tdelete _controller;
\t\tdelete _rc;""",
"""\t\t// Embedded network controller omitted in client-only build."""
),
(
"""\t\t\t// Network controller is now enabled by default for desktop and server
\t\t\t_controller = new EmbeddedNetworkController(_node,_homePath.c_str(),_controllerDbPath.c_str(),_ports[0], _rc);
\t\t\tif (!_ssoRedirectURL.empty()) {
\t\t\t\t_controller->setSSORedirectURL(_ssoRedirectURL);
\t\t\t}
\t\t\t_node->setNetconfMaster((void *)_controller);""",
"""\t\t\t// Embedded local network controller omitted: client-only router build."""
),
(
"""\t\t\t\t} else {
\t\t\t\t\tif (_controller) {
\t\t\t\t\t\tscode = _controller->handleControlPlaneHttpGET(std::vector<std::string>(ps.begin()+1,ps.end()),urlArgs,headers,body,responseBody,responseContentType);
\t\t\t\t\t} else scode = 404;
\t\t\t\t}""",
"""\t\t\t\t} else {
\t\t\t\t\tscode = 404;
\t\t\t\t}"""
),
(
"""\t\t\t\t} else {
\t\t\t\t\tif (_controller)
\t\t\t\t\t\tscode = _controller->handleControlPlaneHttpPOST(std::vector<std::string>(ps.begin()+1,ps.end()),urlArgs,headers,body,responseBody,responseContentType);
\t\t\t\t\telse scode = 404;
\t\t\t\t}""",
"""\t\t\t\t} else {
\t\t\t\t\tscode = 404;
\t\t\t\t}"""
),
(
"""\t\t\t\t} else {
\t\t\t\t\tif (_controller)
\t\t\t\t\t\tscode = _controller->handleControlPlaneHttpDELETE(std::vector<std::string>(ps.begin()+1,ps.end()),urlArgs,headers,body,responseBody,responseContentType);
\t\t\t\t\telse scode = 404;
\t\t\t\t}""",
"""\t\t\t\t} else {
\t\t\t\t\tscode = 404;
\t\t\t\t}"""
),
(
"""\t\t\t\tif ((rt)&&(rt->len > 0)&&(rt->len <= ZT_MAX_REMOTE_TRACE_SIZE)&&(rt->data))
\t\t\t\t\t_controller->handleRemoteTrace(*rt);""",
"""\t\t\t\t(void)rt;"""
),
]

for old,new in patches:
    if old not in s:
        raise SystemExit("source patch target not found: "+old[:120].replace("\n"," "))
    s=s.replace(old,new,1)

p.write_text(s)

# Sanity: no callable controller method must remain.
for forbidden in (
    "_controller = new EmbeddedNetworkController",
    "_controller->handleControlPlane",
    "_controller->handleRemoteTrace",
    "_node->setNetconfMaster((void *)_controller)",
):
    if forbidden in s:
        raise SystemExit("forbidden controller reference remains: "+forbidden)

print("client-only patch OK")
print("removed objects:")
for x in sorted(removed):
    print(" -",x)
