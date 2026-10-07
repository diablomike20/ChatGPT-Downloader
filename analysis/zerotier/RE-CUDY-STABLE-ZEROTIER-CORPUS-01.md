# RE Cudy stable ZeroTier corpus 01

- Stable packages: **33**
- Rootfs images scanned: **33**
- ZeroTier occurrences: **30**
- Distinct ZeroTier+dependency payloads: **16**
- Target baseline: **WR1200V2-R26-2.4.23-20251224-145945-flash.zip**

Ranking is by direct R26 ELF compatibility, resolved dependencies, then XZ footprint.

| Rank | Donor | ZT bytes | R26 payload | gzip-9 | XZ-9e | Δ XZ vs R25 | Direct R26 ELF | ZT SHA |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 1 | WR1300 V1/R10 1.13.6 | 791080 | 2140557 | 779682 | 566472 | 84 | YES | `57c2f0f40039db7f…` |
| 2 | M1200/R22 2.4.19 | 791080 | 2140557 | 779813 | 566556 | 0 | YES | `c4b43b43ca8baaa5…` |
| 3 | LT500 Outdoor/R35 2.3.14 | 791080 | 2140557 | 779813 | 566556 | 0 | YES | `c4b43b43ca8baaa5…` |
| 4 | M1200/R22 2.0.8 | 791080 | 2140557 | 779817 | 566628 | -72 | YES | `c4b43b43ca8baaa5…` |
| 5 | LT400 Outdoor/R40 1.15.34 | 791080 | 2140557 | 779818 | 566640 | -84 | YES | `c4b43b43ca8baaa5…` |
| 6 | LT500 Outdoor/R35 2.1.10 | 791080 | 2140557 | 779819 | 566644 | -88 | YES | `c4b43b43ca8baaa5…` |
| 7 | LT700/R32 1.15.29 | 791080 | 2140557 | 779817 | 566676 | -120 | YES | `c4b43b43ca8baaa5…` |
| 8 | WR1300 V2/R23 2.4.4 | 791080 | 2140557 | 779811 | 566708 | -152 | YES | `c4b43b43ca8baaa5…` |
| 9 | WR1300 V2/R23 2.2.6 | 791080 | 2140557 | 779818 | 566712 | -156 | YES | `c4b43b43ca8baaa5…` |
| 10 | TR1200/R46 2.2.7 | 791080 | 2140557 | 779817 | 566740 | -184 | YES | `c4b43b43ca8baaa5…` |
| 11 | TR1200/R46 1.16.3 | 791080 | 2140557 | 779818 | 566960 | -404 | YES | `c4b43b43ca8baaa5…` |
| 12 | LT500 V2 / LT500D V2/R25 1.15.28 | 791080 | 2140557 | 779815 | 566972 | -416 | YES | `c4b43b43ca8baaa5…` |
| 13 | WR1300 V2/R23 2.0.4 | 791080 | 2140557 | 779816 | 566972 | -416 | YES | `c4b43b43ca8baaa5…` |
| 14 | LT400/R6 1.15.27 | 791080 | 2140557 | 779818 | 566972 | -416 | YES | `c4b43b43ca8baaa5…` |
| 15 | LT400E/R61 2.1.10 | 791080 | 2140557 | 779818 | 566972 | -416 | YES | `c4b43b43ca8baaa5…` |
| 16 | LT400V/R75 2.2.2 | 791080 | 2140557 | 779818 | 566972 | -416 | YES | `c4b43b43ca8baaa5…` |

## Dependency details
### 1. WR1300 V1/R10 1.13.6
- ZT SHA-256: `57c2f0f40039db7f6f91b24232be0120a9b75ce268c8da859ac6f85d48e7f4b2`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B ffe09fd625d21bf74bc5cbc8bd4a6fb9d18a27411264317e90fa1544534c571c
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: WR1300 V1/R10 1.13.6 :: WR1300-R10-1.13.6-20220314-112409-flash_1.zip
### 2. M1200/R22 2.4.19
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B 534c19fe404208e1065cc6b988b152d0b2a70e29e5865ab6dfa5a6b189cc5481
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: M1200/R22 2.4.19 :: M1200-R22-2.4.19-20250826-164643-flash.zip; M1200/R22 2.4.24 :: M1200-R22-2.4.24-20260105-103138-flash.zip; TR1200/R46 2.4.15 :: TR1200-R46-2.4.15-20250721-164017-flash.zip; LT500 V2 / LT500D V2/R25 2.4.16 :: LT500V2-R25-2.4.16-20250804-150319-flash.zip; LT500 Outdoor/R35 2.4.9 :: LT500Outdoor-R35-2.4.9-20250625-180244-flash.zip; LT700/R32 2.4.21 :: LT700-R32-2.4.21-20250922-170147-flash.zip
### 3. LT500 Outdoor/R35 2.3.14
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B 40a1df73cf014c7b90ea40461cb559d3d2277ef624029f2bab28bf5613af0d62
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: LT500 Outdoor/R35 2.3.14 :: LT500Outdoor-R35-2.3.14-20250307-112700-flash.zip
### 4. M1200/R22 2.0.8
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B d6b946089fa531fce55646dd2ab54ca8b8f5a0340b0ec4cf8c8f8e08ab2bf071
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: M1200/R22 2.0.8 :: M1200-R22-2.0.8-20240306-170059-flash.zip
### 5. LT400 Outdoor/R40 1.15.34
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B cfc7902ddcda5cb6d5de92d05cca737d78cb370d53bc1e70c7342e5f9688fa2e
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: LT400 Outdoor/R40 1.15.34 :: LT400Outdoor-R40-1.15.34-20230525-155951-flash.zip; LT400 Outdoor/R40 2.1.9 :: LT400Outdoor-R40-2.1.9-20240522-110221-flash.zip
### 6. LT500 Outdoor/R35 2.1.10
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B 8b783558eeb245e5697368fabc2d74c88c911df0757154af807f2cb4868ee65c
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: LT500 Outdoor/R35 2.1.10 :: LT500Outdoor-R35-2.1.10-20240528-163250-flash.zip
### 7. LT700/R32 1.15.29
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B 597412319da2bfe6f3ddb9fc221c729427bcd41596e0dabd052c4c4de03840a1
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: LT700/R32 1.15.29 :: LT700-R32-1.15.29-20230418-161423-flash.zip; LT700/R32 2.1.3 :: LT700-R32-2.1.3-20240506-110223-flash.zip
### 8. WR1300 V2/R23 2.4.4
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B d1a994766bfaf5fa60a6b8ef0515382b73f527fc23df934f5fd71ee590f4ffb7
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: WR1300 V2/R23 2.4.4 :: WR1300B-R23-2.4.4-20250507-170413-flash.zip; WR1300 V2/R23 2.5.25 :: WR1300B-R23-2.5.25-20260805-113408-flash.zip; TR1200/R46 2.5.25 :: TR1200-R46-2.5.25-20260805-112208-flash.zip
### 9. WR1300 V2/R23 2.2.6
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B 64c82a9182dc9ac503989529b74de427b876e366152591ec17ba5748dc0bac38
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: WR1300 V2/R23 2.2.6 :: WR1300B-R23-2.2.6-20240815-095128-flash.zip; WR1300 V2/R23 2.3.9 :: WR1300B-R23-2.3.9-20250208-115514-flash.zip
### 10. TR1200/R46 2.2.7
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B 1e07bfc026259127cf697a29ef32dcc52be7b34c11426d311048984f58149096
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: TR1200/R46 2.2.7 :: TR1200-R46-2.2.7-20241011-103924-flash.zip; TR1200/R46 2.3.7 :: TR1200-R46-2.3.7-20250113-115854-flash.zip
### 11. TR1200/R46 1.16.3
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B e114d03296e4d5482fbe57f00beeb2c2736f6b0a198279376b723a3d34e2739b
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: TR1200/R46 1.16.3 :: TR1200-R46-1.16.3-20230804-164635-flash.zip; TR1200/R46 2.1.3 :: TR1200-R46-2.1.3-20240428-102143-flash.zip
### 12. LT500 V2 / LT500D V2/R25 1.15.28
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B b49ada75f82b646a2e9593594038c0d5c4527b38bdbcd2e59002dfb17af410f3
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: LT500 V2 / LT500D V2/R25 1.15.28 :: LT500V2-R25-1.15.28-20230410-094349-flash.zip; LT450/LT500/LT500D V2/R25 2.1.1 :: LT450-LT500-LT500DV2-R25-2.1.1-20240419-090237-flash.zip
### 13. WR1300 V2/R23 2.0.4
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B 6114d831f9cb2f8f88948a21c281a05428a0745d00693eaf1b8d2e095dad8ccf
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: WR1300 V2/R23 2.0.4 :: WR1300B-R23-2.0.4-20240206-090502-flash_1.zip
### 14. LT400/R6 1.15.27
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B f4bf7ed3e62b68172c747ea0b35ac7d78fb5e89980422b6522b88b294b7ff005
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: LT400/R6 1.15.27 :: LT400A-R6-1.15.27-20230404-114529-flash.zip; LT400/R6 2.1.9 :: LT400A-R6-2.1.9-20240522-111245-flash.zip
### 15. LT400E/R61 2.1.10
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B 93cadfb567c3ec7553d8fc22c8534ed28000c005147b5412f7fd10ae6403eec6
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: LT400E/R61 2.1.10 :: LT400E-R61-2.1.10-20240527-092607-flash.zip
### 16. LT400V/R75 2.2.2
- ZT SHA-256: `c4b43b43ca8baaa5a53d036530c42dc93b4ec5bde68cd0c65c135d9f4d56cf0c`
- ELF: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, no section header
- Attributes: 
- NEEDED: libminiupnpc.so.17, libnatpmp.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so
- libminiupnpc.so.17: ADD_FROM_DONOR libminiupnpc.so.2.2.1 37279 B 508a149567c14c397195e47943904470d2510c3155f9be88f4c5296d8610d34e
- libnatpmp.so.1: ADD_FROM_DONOR libnatpmp.so.20150609 8331 B 7176915a35874f1b7e35f4927c4b3b599ecabe3c1c259fb6e0182f301e8cbefb
- libstdc++.so.6: ADD_FROM_DONOR libstdc++.so.6.0.21 1303867 B d68eba2b328e22be6385384ee61f6e456183ee4df01c132112d314ab5170eed4
- libgcc_s.so.1: R26_PRESENT  0 B 5aa27aa0175e69dcd3feba71d91b5d97c1de84ce758282ec94136c6029b0caa2
- libc.so: R26_PRESENT  0 B 8c3c5cbefef736e4aa9e068bdf41a502824a759d1f02027189811d5e63cc76db
- Provenance: LT400V/R75 2.2.2 :: LT400V-R75-2.2.2-20240729-091345-flash.zip
