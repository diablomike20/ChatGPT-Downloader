# ZeroTier 1.8.6 candidate compression

WR1200 V2 stock inventory exposes BusyBox gzip/gunzip and bunzip2/bzcat, but no xz/unxz symlink.

| Variant | Raw | gzip-9 | bzip2-9 | xz-9e | fits 448 KiB bzip2 | bzip2 headroom |
|---|---:|---:|---:|---:|---|---:|
| clientonly-noportmapper-staticstdcpp-lto | 1485336 | 559051 | 521675 | 394476 | NO | -62923 |
| clientonly-noportmapper-staticstdcpp-lto-nortti | 1485340 | 558661 | 521024 | 394244 | NO | -62272 |
| noportmapper-staticstdcpp-lto | 1799604 | 681608 | 632651 | 480484 | NO | -173899 |
| bundled-staticstdcpp-lto | 1828368 | 696351 | 647368 | 489840 | NO | -188616 |
