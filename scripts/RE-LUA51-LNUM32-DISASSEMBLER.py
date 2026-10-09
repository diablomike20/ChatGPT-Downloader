#!/usr/bin/env python3
"""RE-LUA51-LNUM32-DISASSEMBLER

Minimal static disassembler for the OpenWrt/Cudy Lua 5.1 LNUM32 bytecode
profile seen in CSP2.5 firmware. It does not execute Lua bytecode.

Header currently expected/observed:
  1b4c75615100010404040804
which is Lua 5.1, little-endian, 4-byte int, 4-byte size_t,
4-byte instruction, 8-byte lua_Number and 4-byte lua_Integer.

This tool intentionally prints constants and instruction operands only.
It is an RE aid, not a complete Lua decompiler.
"""
import sys
from pathlib import Path

OP=[
"MOVE","LOADK","LOADBOOL","LOADNIL","GETUPVAL","GETGLOBAL","GETTABLE",
"SETGLOBAL","SETUPVAL","SETTABLE","NEWTABLE","SELF","ADD","SUB","MUL",
"DIV","MOD","POW","UNM","NOT","LEN","CONCAT","JMP","EQ","LT","LE",
"TEST","TESTSET","CALL","TAILCALL","RETURN","FORLOOP","FORPREP",
"TFORLOOP","SETLIST","CLOSE","CLOSURE","VARARG"
]

class Reader:
    def __init__(self,data:bytes):
        self.d=data
        if len(data)<12 or data[:4]!=b"\x1bLua" or data[4]!=0x51:
            raise ValueError("not Lua 5.1 bytecode")
        self.o=12
        self.le=data[6]==1
        self.isz=data[7]
        self.ssz=data[8]
        self.insz=data[9]
        self.nsz=data[10]
        self.intsz=data[11]

    def take(self,n):
        b=self.d[self.o:self.o+n]
        if len(b)!=n: raise EOFError((self.o,n,len(b)))
        self.o+=n
        return b

    def uint(self,n):
        return int.from_bytes(self.take(n),"little" if self.le else "big")

    def lua_int(self):
        return self.uint(self.isz)

    def string(self):
        n=self.uint(self.ssz)
        if not n: return None
        b=self.take(n)
        if b[-1:]==b"\0": b=b[:-1]
        return b.decode("latin1","replace")

    def proto(self,parent_source=None):
        start=self.o
        src=self.string() or parent_source
        line_defined=self.lua_int()
        last_line_defined=self.lua_int()
        nups=self.uint(1)
        nparams=self.uint(1)
        is_vararg=self.uint(1)
        maxstack=self.uint(1)

        ncode=self.lua_int()
        code=[self.uint(self.insz) for _ in range(ncode)]

        nk=self.lua_int()
        const=[]
        for _ in range(nk):
            t=self.uint(1)
            if t==0: v=None
            elif t==1: v=bool(self.uint(1))
            elif t==3: v={"lua_number_hex":self.take(self.nsz).hex()}
            elif t==9: v=self.uint(self.intsz)  # LNUM LUA_TINT
            elif t==4: v=self.string()
            else: raise ValueError(("unsupported constant type",t,self.o))
            const.append(v)

        np=self.lua_int()
        protos=[self.proto(src) for _ in range(np)]

        nline=self.lua_int()
        lines=[self.lua_int() for _ in range(nline)]

        nloc=self.lua_int()
        locals_=[(self.string(),self.lua_int(),self.lua_int()) for _ in range(nloc)]

        nupnames=self.lua_int()
        upnames=[self.string() for _ in range(nupnames)]

        return {
            "start":start,"source":src,"line_defined":line_defined,
            "last_line_defined":last_line_defined,"nups":nups,
            "nparams":nparams,"vararg":is_vararg,"maxstack":maxstack,
            "code":code,"K":const,"P":protos,"lines":lines,
            "locals":locals_,"upnames":upnames
        }

def rk(x,K):
    if x & 256:
        i=x&255
        return f"K{i}={K[i]!r}" if i<len(K) else f"K{i}"
    return f"R{x}"

def insn_text(x,K,pc):
    o=x&63; A=(x>>6)&255; C=(x>>14)&511; B=(x>>23)&511
    Bx=(x>>14)&262143; sBx=Bx-131071
    n=OP[o] if o<len(OP) else f"OP{o}"
    if n=="LOADK":
        e=f"R{A}=K{Bx}={K[Bx]!r}" if Bx<len(K) else f"R{A}=K{Bx}"
    elif n in ("GETGLOBAL","SETGLOBAL"):
        e=f"A={A} K{Bx}={K[Bx]!r}" if Bx<len(K) else f"A={A} K{Bx}"
    elif n in ("GETTABLE","SETTABLE","SELF","ADD","SUB","MUL","DIV","MOD","POW","EQ","LT","LE"):
        e=f"A={A} B={rk(B,K)} C={rk(C,K)}"
    elif n in ("JMP","FORLOOP","FORPREP"):
        e=f"A={A} sBx={sBx} -> {pc+sBx+1}"
    elif n=="CLOSURE":
        e=f"A={A} Proto={Bx}"
    else:
        e=f"A={A} B={B} C={C}"
    return f"{pc:04d} {n:10} {e}"

def walk(p,depth=0,idx="0"):
    pad="  "*depth
    print(f"\n{pad}PROTO {idx} depth={depth} source={p['source']!r} "
          f"code={len(p['code'])} maxstack={p['maxstack']} "
          f"params={p['nparams']} upvalues={p['nups']}")
    print(f"{pad}CONSTANTS={p['K']!r}")
    if p["locals"]: print(f"{pad}LOCALS={p['locals']!r}")
    if p["upnames"]: print(f"{pad}UPVALUE_NAMES={p['upnames']!r}")
    for pc,x in enumerate(p["code"],1):
        print(pad+insn_text(x,p["K"],pc))
    for i,q in enumerate(p["P"]):
        walk(q,depth+1,f"{idx}.{i}")

def main():
    if len(sys.argv)!=2:
        raise SystemExit("usage: RE-LUA51-LNUM32-DISASSEMBLER.py FILE.lua")
    fn=Path(sys.argv[1])
    d=fn.read_bytes()
    print(f"FILE={fn}")
    print(f"SIZE={len(d)}")
    print(f"HEADER={d[:12].hex()}")
    r=Reader(d)
    p=r.proto()
    print(f"PARSE_END={r.o} TOTAL={len(d)}")
    walk(p)

if __name__=="__main__":
    main()
