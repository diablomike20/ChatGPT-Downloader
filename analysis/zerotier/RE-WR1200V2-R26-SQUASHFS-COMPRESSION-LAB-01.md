# WR1200 V2 / R26 SquashFS compression lab 01

- Stock SquashFS bytes_used: **5,242,960 B**
- SquashFS offset: **0x276aff**
- rootfs_data boundary: **0x780000**
- Existing xattr inventory non-empty: **NO**

| Rank | Variant | bytes_used | Delta vs stock | Headroom | Fits? |
|---:|---|---:|---:|---:|---|
| 1 | client-1m-frag-noexports-noxattrs | 5,456,026 | +213,066 | -175,001 | NO |
| 2 | client-1m-noexports-noxattrs | 5,458,386 | +215,426 | -177,361 | NO |
| 3 | client-1m-noexports | 5,458,386 | +215,426 | -177,361 | NO |
| 4 | client-1m | 5,460,486 | +217,526 | -179,461 | NO |
| 5 | client-512k | 5,576,150 | +333,190 | -295,125 | NO |
| 6 | client-256k | 5,683,570 | +440,610 | -402,545 | NO |

Geometry-only 512 KiB / 1 MiB block variants preserve the file tree. no-exports/no-xattrs/fragment variants are size experiments and still require compatibility review before any target use.
