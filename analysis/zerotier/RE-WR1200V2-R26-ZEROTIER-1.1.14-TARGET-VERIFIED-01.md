# WR1200 V2 / R26 — ZeroTier 1.1.14 TARGET VERIFIED 01

Date: 2026-10-07

## Target

- Device: Cudy WR1200 V2 / R26
- Firmware baseline: Cudy 2.4.23 / LEDE 17.01.5 family
- CPU target: mipsel_24kc / MT7628
- Test candidate: official LEDE 17.01 ZeroTier 1.1.14-4 binary

## Exact binary

- Size: 666,967 bytes
- SHA-256: 815303c7ae79d1c5296ad16b4498b993e7e9fe4d2d2914d852f66a6d0086aaf0
- Version: 1.1.14
- Runtime dependencies observed on target:
  - libc.so
  - libgcc_s.so.1
  - /lib/ld-musl-mipsel-sf.so.1
- No external libstdc++, miniupnpc, or natpmp required by this binary.

## Preliminary parallel runtime test

The 1.1.14 binary was started in parallel with the existing TARGET_VERIFIED 1.8.6 daemon using a separate state directory and separate port.

Observed:
- daemon started successfully
- identity generated successfully
- local API worked
- public ZeroTier root peers became reachable
- status reached ONLINE 1.1.14
- existing 1.8.6 stayed ONLINE during the parallel test

A later test using the current 1.8.6 planet file also reached ONLINE, but importantly 1.1.14 had already reached ONLINE before that copy. Therefore current ZeroTier connectivity does not depend on substituting the newer planet file.

## Hard live switch test

A detached hard-switch script was used because the router was reachable only through ZeroTier.

The script:
1. recorded current 1.8.6 status
2. launched a 360-second rollback watchdog
3. stopped the current ZeroTier service
4. changed /usr/bin/zerotier-one to the 1.1.14 binary under /tmp
5. restarted the native Cudy ZeroTier integration
6. polled status repeatedly
7. wrote a persistent test result file

Result file:

```
TARGET_PASS_1.1.14_ONLINE
```

Timeline:
- 17:35:41 — switch started
- 17:35:45 — ZeroTier 1.1.14 started
- 17:35:50 — first poll: OFFLINE
- polls 1–18 remained OFFLINE
- 17:37:24 — poll 19: ONLINE 1.1.14
- convergence time from daemon start to ONLINE: approximately 99 seconds

## Target runtime evidence

After the hard switch:

- `zerotier-one -v` returned `1.1.14`
- `zerotier-cli info` returned `ONLINE 1.1.14`
- the same production ZeroTier identity was retained
- the configured private network reported `OK PRIVATE`
- a ZeroTier interface was created and UP
- the expected private ZeroTier IPv4 route was present
- remote SSH access over ZeroTier recovered and remained usable
- the native Cudy wrapper/init chain remained active

Private network ID, node identity, MAC addresses, assigned private addresses, and external peer IPs are intentionally redacted from this report.

## Verification classification

**TARGET_VERIFIED**

This is no longer only ABI/static/build evidence. The official LEDE 17.01 ZeroTier 1.1.14-4 binary has been proven on the physical WR1200 V2/R26 with the production Cudy integration, real ZeroTier identity, real private network membership, and remote SSH connectivity.

## Important current limitation

The verified 1.1.14 binary is currently reached through:

```
/usr/bin/zerotier-one -> /tmp/RE-ZT1114/root/usr/bin/zerotier-one
```

Therefore this live state is **NOT reboot persistent**. A reboot would remove the /tmp payload.

Do not call reboot persistence TARGET_VERIFIED yet.

## Firmware-fit result already proven

Separate exact SquashFS repack testing with English-only language policy and stock-compatible 256 KiB XZ geometry showed:

- stock SquashFS bytes_used: 5,242,960 B
- EN-only + original LEDE 1.1.14 binary: 5,206,842 B
- delta vs stock: -36,118 B
- headroom before rootfs_data: +74,183 B
- FIT: YES

The final persistent firmware still needs the native ZeroTier integration files included and measured together, but the heavy runtime binary itself is now both FIT-VERIFIED and TARGET-VERIFIED.

## Next step

Build an exact final static candidate from stock R26:

- English only
- original LEDE ZeroTier 1.1.14-4 binary installed as a real persistent /usr/bin/zerotier-one file
- zerotier-cli -> zerotier-one
- zerotier-idtool -> zerotier-one
- preserve/adapt the already working Cudy ZeroTier UCI/init/wrapper/LuCI integration
- remove obsolete external libstdc++/miniupnpc/natpmp overlay links from the 1.8.6 transplant
- enable ZeroTier at boot in the firmware image
- repack at stock 256 KiB XZ geometry
- measure exact final headroom
- static-verify all paths, symlinks, permissions, dependencies, and init ordering

No flash or reboot without explicit user approval.
