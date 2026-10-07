# ZeroTier 1.8.6 MIPS size lab 01

Upstream source commit: `4a2c75a60941e75f36ed1961458a42fbd12ea4ac`
Target toolchain: LEDE 17.01.5 ramips/mt7628, GCC 5.4.0, musl 1.1.16.
R26 baseline payload: 2,140,557 B logical / 779,813 B gzip-9 / 566,556 B XZ-9e.

| Rank | Variant | Binary | NEEDED | R26 payload | gzip-9 | XZ-9e | Δ gzip vs R25 | Δ XZ vs R25 |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | clientonly-noportmapper-staticstdcpp-lto-hidden-micro-nothreadsafe | 1428000 | libgcc_s.so.1, libc.so | 1428000 | 547452 | 385064 | 232361 | 181492 |
| 2 | clientonly-noportmapper-staticstdcpp-lto-hidden | 1427992 | libgcc_s.so.1, libc.so | 1427992 | 547513 | 385068 | 232300 | 181488 |
| 3 | clientonly-noportmapper-staticstdcpp-lto-hidden-micro | 1428000 | libgcc_s.so.1, libc.so | 1428000 | 547481 | 387844 | 232332 | 178712 |
| 4 | clientonly-noportmapper-staticstdcpp-lto-nortti | 1485340 | libgcc_s.so.1, libc.so | 1485340 | 558769 | 394204 | 221044 | 172352 |
| 5 | clientonly-noportmapper-staticstdcpp-lto | 1485336 | libgcc_s.so.1, libc.so | 1485336 | 559166 | 394584 | 220647 | 171972 |
| 6 | noportmapper-staticstdcpp-lto | 1799604 | libgcc_s.so.1, libc.so | 1799604 | 681696 | 478212 | 98117 | 88344 |
| 7 | noportmapper-staticstdcpp-lto-nortti | 1791448 | libgcc_s.so.1, libc.so | 1791448 | 681620 | 480596 | 98193 | 85960 |
| 8 | bundled-staticstdcpp-lto | 1828368 | libgcc_s.so.1, libc.so | 1828368 | 696418 | 489760 | 83395 | 76796 |
| 9 | noportmapper-staticstdcpp | 2168800 | libgcc_s.so.1, libc.so | 2168800 | 769210 | 534588 | 10603 | 31968 |
| 10 | bundled-staticstdcpp | 2205916 | libgcc_s.so.1, libc.so | 2205916 | 788473 | 546496 | -8660 | 20060 |
| 11 | bundled-dynamic | 1662096 | libstdc++.so.6, libgcc_s.so.1, libc.so | 2965963 | 971496 | 672108 | -191683 | -105552 |
| 12 | fullstatic | BUILD FAIL | | | | | | |
