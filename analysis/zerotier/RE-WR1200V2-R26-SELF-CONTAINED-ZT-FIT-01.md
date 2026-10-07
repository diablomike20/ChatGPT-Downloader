# WR1200 V2 / R26 self-contained ZeroTier fit 01

- SquashFS logical end: 0x785cf9
- SquashFS padded end: 0x786aff
- Dynamic rootfs_data start: 0x790000
- Fits before 0x790000: True
- Padding remaining: 38145 B
- Resulting rootfs_data: 384 KiB

Included in ROM: ZeroTier 1.1.14-4 binary, cli/idtool symlinks, native R25 wrapper/init/default config/uci-defaults and Cudy LuCI ZeroTier files, plus S90zerotier boot enable symlink.
