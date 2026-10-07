# WR1200 V2 / R26 dynamic rootfs_data fit 01

Status: ANALYSIS ONLY - not flash/boot verified.

## Result

- Candidate SquashFS logical end: 0x785539
- Candidate SquashFS padded end: 0x785aff
- Eraseblock-rounded rootfs_data start: 0x790000
- New rootfs_data size: 384 KiB
- Overlay capacity lost: 64 KiB
- Padding before new split: 42241 B
- Modeled free overlay at current 244 KiB usage: 140 KiB

## Candidate

- ZeroTier: official LEDE/OpenWrt 17.01 mipsel_24kc 1.1.14-4
- ZeroTier SHA-256: 815303c7ae79d1c5296ad16b4498b993e7e9fe4d2d2914d852f66a6d0086aaf0
- Analysis image SHA-256: 0d4d71ac45583f70340507add010ee8818d33ec33deaa61f4572e0e48149c3f8

## Preservation

- Prefix before SquashFS: PRESERVED
- Tail/trailer at and after 0x790000: PRESERVED byte-for-byte
- Trailer size: 155 B

## Limitation

Moving rootfs_data from 0x780000 to 0x790000 changes the JFFS2 layout. A real upgrade therefore needs explicit overlay/config migration or clean-overlay rebuild. This is not TARGET_VERIFIED and must not be flashed solely from this analysis.
