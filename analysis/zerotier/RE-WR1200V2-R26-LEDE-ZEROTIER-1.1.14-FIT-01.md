# WR1200 V2 / R26 + LEDE ZeroTier 1.1.14-4 fit 01

- Candidate: LEDE/OpenWrt 17.01 packages, mipsel_24kc
- zerotier-one: 666,967 B
- SHA-256: 815303c7ae79d1c5296ad16b4498b993e7e9fe4d2d2914d852f66a6d0086aaf0
- NEEDED: libc.so, libgcc_s.so.1
- Stock SquashFS bytes_used: 5,242,960 B

| Block | SquashFS bytes_used | Delta vs stock | End | Headroom | Fits? |
|---|---:|---:|---|---:|---|
| 256k | 5,503,810 | +260,850 | 0x7b6641 | -222,785 | NO |
| 512k | 5,400,482 | +157,522 | 0x79d2a1 | -119,457 | NO |
| 1m | 5,302,842 | +59,882 | 0x785539 | -21,817 | NO |
