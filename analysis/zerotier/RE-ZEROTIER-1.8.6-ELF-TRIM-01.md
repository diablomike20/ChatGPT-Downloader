# ZeroTier 1.8.6 ELF trim + QEMU smoke 01

Both original and trimmed binaries must print the same version under qemu-mipsel against the stock R26 rootfs.

| Variant | Original | Trimmed | Raw saving | XZ before | XZ after | XZ saving |
|---|---:|---:|---:|---:|---:|---:|
| clientonly-noportmapper-staticstdcpp-lto | 1,485,336 | 1,483,800 | 1,536 | 394,476 | 393,760 | 716 |
| clientonly-noportmapper-staticstdcpp-lto-nortti | 1,485,340 | 1,483,804 | 1,536 | 394,244 | 396,048 | -1,804 |

## Persist repack with trimmed baseline

- SquashFS bytes_used: **5,354,430 B**
- SquashFS end: **0x791ebd**
- Dynamic rootfs_data start: **0x7a0000**
- Dynamic rootfs_data size: **320 KiB**
- Headroom vs current 244 KiB used: **77,824 B**
