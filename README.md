# ChatGPT-Downloader

Dedicated download/archive/analysis repository used by ChatGPT-assisted OpenCudy work.

## Branch policy

- **main** — public, normal, stable firmware only.
- **cudy-beta** — beta/test/RC firmware.
- **cudy-dev-support** — development, internal, unlisted and support-private firmware.
- **cudy-openwrt-intermediate** — Cudy → OpenWrt intermediary/bridge and related recovery images.
- **cudy-cellular-modem** — cellular/modem/baseband and CellularUpgrade firmware; oversized images may use GitHub Release assets.
- **cudy-dev-beta** — legacy FU7 history/tooling archive only; superseded for active firmware storage.

The older `diablomike20/Website-downloader` repository remains a **website downloader/crawler**. Firmware collection and firmware-analysis workflows are moved here.

## Main branch scope

```
firmware/cudy/stable/    Official public stable Cudy firmware packages + manifests
scripts/                 Stable firmware download/extract/audit helpers
analysis/zerotier/       Stable ZeroTier donor research
.github/workflows/       Stable firmware synchronization and analysis
```

## WR1200 ZeroTier project

Target:
- Cudy WR1200 V2 / R26
- LEDE 17.01.5 / Cudy 2.4.23
- MT7628 / mipsel_24kc
- 8 MiB NOR / 64 MiB RAM

Known working runtime donor:
- LT500D V2 / R25 ZeroTier stack
- runtime proven on WR1200 V2
- current research target: smaller public/stable Cudy ZeroTier runtime/dependency footprint

## Evidence rule

Static donor compatibility is not target-runtime proof. A firmware package stored here is donor/evidence material and is not automatically safe to flash on another board.
