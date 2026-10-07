# WR1200 V2 / R26 upgrade-chain audit 01

## Stock image

- SHA-256: b9842ca6d6b54d4d2b8bb4d13457ee674ba2d13540443af1cf1ce82708ea02cd
- Size: 7930011 B (0x79009b)
- Firmware/uImage absolute start: 0x50000
- SquashFS absolute start: 0x276aff
- uImage end equals SquashFS start: YES
- uImage header CRC: PASS
- uImage data CRC: PASS
- uImage name: R26

## Bytes at current rootfs_data boundary 0x780000

deadc0deffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

## Bytes at 0x790000 trailer

deadc0de00000000000000007b202022737570706f727465645f64657669636573223a5b22523236225d2c202276657273696f6e223a207b202264697374223a20224c454445222c202276657273696f6e223a202231372e30312e35222c20227265766973696f6e223a2022322e342e3233222c2022626f617264223a202272616d69707322207d207d0a46577830097183110100000000000097

## platform.sh relevant lines

    platform_check_image() {
    		oem-check -b "$board" -o 0x80000 -f "$1"
    		oem-check -b "$board" -o 0x30000 -f "$1"
    platform_do_upgrade() {
    	if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    			get_image "$1" | dd bs=2k count="$dd_count" conv=sync 2>/dev/null | mtd write - "${BOOT_NAME:-u-boot}" >>$SYSUPGRADE_LOG_FILE 2>&1
    		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    			get_image "$1" | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    			get_image "$1" | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1

## sysupgrade relevant lines

    export SAVE_CONFIG=1
    export CONF_BACKUP_LIST=0
    export CONF_BACKUP=
    export FORCE=0
    export OEM_UPGRADE_BOOT=1
    export OEM_CHECK_IMAGE=
    		-n) export SAVE_CONFIG=0;;
    		-b|--create-backup) export CONF_BACKUP="$2" NEED_IMAGE=1; shift;;
    		-l|--list-backup) export CONF_BACKUP_LIST=1; break;;
    		-e) export OEM_CHECK_IMAGE="$2" NEED_IMAGE=1; shift;;
    		-F|--force) export FORCE=1;;
    	-F | --force
    [ "$CONF_BACKUP" = "-" ] && export VERBOSE=0
    sysupgrade_image_check="fwtool_check_image platform_check_image"
    	type platform_check_image >/dev/null 2>/dev/null || {
    if [ $CONF_BACKUP_LIST -eq 1 ]; then
    if [ -n "$CONF_BACKUP" ]; then
    	do_save_conffiles "$CONF_BACKUP"
    if [ -n "$OEM_CHECK_IMAGE" ]; then
    type platform_check_image >/dev/null 2>/dev/null || {
    		if [ $FORCE -eq 1 ]; then
    			echo "Image check '$check' failed but --force given - will update anyway!"
    			OEM_UPGRADE_BOOT=0
    			OEM_UPGRADE_BOOT=0
    	export SAVE_CONFIG=1
    elif ask_bool $SAVE_CONFIG "Keep config files over reflash"; then
    	export SAVE_CONFIG=1
    	export SAVE_CONFIG=0
