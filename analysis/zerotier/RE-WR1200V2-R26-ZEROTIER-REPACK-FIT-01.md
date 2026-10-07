# WR1200 V2 / R26 ZeroTier SquashFS repack fit 01

Analysis-only repack. This does not claim Cudy image acceptance or target boot verification.

- Stock firmware SHA-256: b9842ca6d6b54d4d2b8bb4d13457ee674ba2d13540443af1cf1ce82708ea02cd
- SquashFS start: 0x276aff
- Stock SquashFS bytes_used: 5,242,960 B
- Stock end: 0x776b4f
- rootfs_data boundary: 0x780000
- Stock headroom: 38,065 B

| Variant | SquashFS bytes_used | delta vs stock | delta vs control | End | Headroom | Fits? |
|---|---:|---:|---:|---|---:|---|
| control | 5,263,134 | +20,174 | +0 | 0x77ba1d | +17,891 | YES |
| client | 5,683,570 | +440,610 | +420,436 | 0x7e2471 | -402,545 | NO |
| controller | 5,779,642 | +536,682 | +516,508 | 0x7f9bb9 | -498,617 | NO |

## Interpretation

- control quantifies mksquashfs reproducibility/tool-version delta.
- client adds only the upstream client-only/no-PortMapper/static-libstdc++/LTO ZeroTier binary.
- controller keeps the local controller but removes PortMapper and statically links libstdc++.
- Existing target overlay integration is intentionally not duplicated into ROM in this fit test.
