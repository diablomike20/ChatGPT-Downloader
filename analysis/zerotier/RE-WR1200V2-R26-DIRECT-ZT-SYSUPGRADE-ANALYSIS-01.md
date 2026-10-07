# WR1200 V2 / R26 direct ZeroTier sysupgrade analysis 01

Status: ANALYSIS ONLY - DO NOT FLASH from this report alone.

- Direct image starts with uImage: True
- uImage header CRC: PASS
- uImage data CRC: PASS
- Direct image size: 7602331 B
- Direct image SHA-256: 9e67796bbeb3e59af0d1bbd743fef75b1d846802ba31228779b7a4f23127aa00
- Dynamic rootfs_data start after boot: 0x790000
- Resulting rootfs_data: 384 KiB

The direct image omits the first 0x50000 bytes of the Cudy full-flash image, so it does not contain U-Boot, factory or other pre-firmware flash regions.
