# WR1200 V2 / R26 ZeroTier + TR-069 removal fit 01

Project policy: TR-069/CWMP is permanently excluded.
rootfs_data is modeled as the 64 KiB-aligned squashfs-split remainder of the rootfs partition.

- erase size: **65,536 B**
- rootfs partition end: **0x7f0000**
- current target overlay used: **249,856 B (244 KiB)**
- explicit CWMP/TR069 paths removed: **30**

## Removed explicit TR-069/CWMP paths

- usr/lib/lua/luci/model/cbi/cwmp.lua
- usr/lib/lua/luci/controller/cwmp.lua
- etc/hotplug.d/iface/96-cwmp_hotplug
- usr/share/cwmp/firewall.include
- usr/bin/tr069/cwmp-portfwd
- usr/bin/tr069/cwmp-upgrd
- usr/bin/tr069/cwmp-nat
- usr/bin/tr069/cwmp-restore
- usr/bin/tr069/cwmp-ppp
- usr/bin/tr069/gen_hosts
- usr/bin/tr069/cwmp-qos
- usr/bin/tr069/cwmp_external_func
- usr/bin/tr069/cwmp-ddns
- usr/bin/tr069/gen_meshlist
- usr/bin/tr069/verify_pms
- usr/bin/tr069/cwmp-user
- usr/bin/tr069/cwmp-ntp
- usr/bin/tr069/gen_ethernet_port_info
- usr/bin/tr069/cwmp-route
- usr/bin/tr069/diagnose
- usr/bin/tr069/cwmp-bkup
- etc/config/cwmp
- etc/rc.d/S99cwmp
- etc/init.d/cwmp
- etc/uci-defaults/98-cwmp
- usr/share/cwmp
- usr/lib/libcwmp.so
- usr/bin/tr069
- usr/bin/cwmp_cli
- usr/bin/cwmp

| Variant | SquashFS bytes_used | Delta vs stock | End | rootfs_data start | rootfs_data | Headroom vs current 244 KiB used |
|---|---:|---:|---|---|---:|---:|
| client | 5,456,026 | +213,066 | 0x7aab99 | 0x7b0000 | 256 KiB | +12,288 B |
| persist | 5,354,842 | +111,882 | 0x792059 | 0x7a0000 | 320 KiB | +77,824 B |
| final | 5,356,538 | +113,578 | 0x7926f9 | 0x7a0000 | 320 KiB | +77,824 B |

- persist = upstream client + TR-069 removal, while keeping the already-persistent target ZeroTier integration in overlay (no ROM duplication).
- final = persist plus the lightweight R25 ZeroTier integration embedded into ROM for factory-clean reconstruction.
- Neither variant copies the old R25 zerotier-one, libstdc++, miniupnpc or natpmp payloads.
