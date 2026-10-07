# WR1200 V2 / R26 config-preserve audit 01

## lib/upgrade/platform.sh

    0025: 	[ "$?" -eq 0 ] && return 0
    0026: 
    0027: 	return 1
    0028: }
    0029: 
    0030: platform_do_upgrade() {
    0031: 	local board_flash=$(oem_board_flash)
    0032: 	local save_config_str=""
    0033: 	local dd_count=96
    0034: 	local dd_skip=160
    0035: 
    0036: 	if [ "$board_flash" = "nand" ]; then
    0037: 		dd_count=128

    0027: 	return 1
    0028: }
    0029: 
    0030: platform_do_upgrade() {
    0031: 	local board_flash=$(oem_board_flash)
    0032: 	local save_config_str=""
    0033: 	local dd_count=96
    0034: 	local dd_skip=160
    0035: 
    0036: 	if [ "$board_flash" = "nand" ]; then
    0037: 		dd_count=128
    0038: 		dd_skip=640
    0039: 		rm -rf /tmp/persistent/sysupgrade.tgz

    0037: 		dd_count=128
    0038: 		dd_skip=640
    0039: 		rm -rf /tmp/persistent/sysupgrade.tgz
    0040: 	fi
    0041: 
    0042: 	if [ "$SAVE_CONFIG" -eq 1 ]; then
    0043: 		save_config_str="-j $CONF_TAR"
    0044: 	fi
    0045: 
    0046: 	if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0047: 		local img_boot_ver="$(get_oem_boot_version "$1")"
    0048: 		local local_boot_ver="$(oem_boot_version)"
    0049: 

    0038: 		dd_skip=640
    0039: 		rm -rf /tmp/persistent/sysupgrade.tgz
    0040: 	fi
    0041: 
    0042: 	if [ "$SAVE_CONFIG" -eq 1 ]; then
    0043: 		save_config_str="-j $CONF_TAR"
    0044: 	fi
    0045: 
    0046: 	if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0047: 		local img_boot_ver="$(get_oem_boot_version "$1")"
    0048: 		local local_boot_ver="$(oem_boot_version)"
    0049: 
    0050: 		if [[ "$img_boot_ver" -gt "$local_boot_ver" ]]; then

    0041: 
    0042: 	if [ "$SAVE_CONFIG" -eq 1 ]; then
    0043: 		save_config_str="-j $CONF_TAR"
    0044: 	fi
    0045: 
    0046: 	if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0047: 		local img_boot_ver="$(get_oem_boot_version "$1")"
    0048: 		local local_boot_ver="$(oem_boot_version)"
    0049: 
    0050: 		if [[ "$img_boot_ver" -gt "$local_boot_ver" ]]; then
    0051: 			sysupgrade_log "sysupgrade uboot"
    0052: 			get_image "$1" | dd bs=2k count="$dd_count" conv=sync 2>/dev/null | mtd write - "${BOOT_NAME:-u-boot}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0053: 			sysupgrade_log_end "sysupgrade uboot ok"

    0047: 		local img_boot_ver="$(get_oem_boot_version "$1")"
    0048: 		local local_boot_ver="$(oem_boot_version)"
    0049: 
    0050: 		if [[ "$img_boot_ver" -gt "$local_boot_ver" ]]; then
    0051: 			sysupgrade_log "sysupgrade uboot"
    0052: 			get_image "$1" | dd bs=2k count="$dd_count" conv=sync 2>/dev/null | mtd write - "${BOOT_NAME:-u-boot}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0053: 			sysupgrade_log_end "sysupgrade uboot ok"
    0054: 		fi
    0055: 	fi
    0056: 
    0057: 	if [ "$board_flash" = "nand" ]; then
    0058: 		sysupgrade_log "sysupgrade firmware2"
    0059: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then

    0054: 		fi
    0055: 	fi
    0056: 
    0057: 	if [ "$board_flash" = "nand" ]; then
    0058: 		sysupgrade_log "sysupgrade firmware2"
    0059: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0060: 			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    0061: 		else
    0062: 			get_image "$1" | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    0063: 		fi
    0064: 		sysupgrade_log_end "sysupgrade firmware2 ok"
    0065: 	else
    0066: 		sysupgrade_log "sysupgrade firmware"

    0055: 	fi
    0056: 
    0057: 	if [ "$board_flash" = "nand" ]; then
    0058: 		sysupgrade_log "sysupgrade firmware2"
    0059: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0060: 			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    0061: 		else
    0062: 			get_image "$1" | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    0063: 		fi
    0064: 		sysupgrade_log_end "sysupgrade firmware2 ok"
    0065: 	else
    0066: 		sysupgrade_log "sysupgrade firmware"
    0067: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then

    0057: 	if [ "$board_flash" = "nand" ]; then
    0058: 		sysupgrade_log "sysupgrade firmware2"
    0059: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0060: 			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    0061: 		else
    0062: 			get_image "$1" | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    0063: 		fi
    0064: 		sysupgrade_log_end "sysupgrade firmware2 ok"
    0065: 	else
    0066: 		sysupgrade_log "sysupgrade firmware"
    0067: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0068: 			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0069: 		else

    0062: 			get_image "$1" | mtd write - firmware2 >>$SYSUPGRADE_LOG_FILE 2>&1
    0063: 		fi
    0064: 		sysupgrade_log_end "sysupgrade firmware2 ok"
    0065: 	else
    0066: 		sysupgrade_log "sysupgrade firmware"
    0067: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0068: 			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0069: 		else
    0070: 			get_image "$1" | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0071: 		fi
    0072: 		sysupgrade_log_end "sysupgrade firmware ok"
    0073: 	fi
    0074: 

    0063: 		fi
    0064: 		sysupgrade_log_end "sysupgrade firmware2 ok"
    0065: 	else
    0066: 		sysupgrade_log "sysupgrade firmware"
    0067: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0068: 			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0069: 		else
    0070: 			get_image "$1" | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0071: 		fi
    0072: 		sysupgrade_log_end "sysupgrade firmware ok"
    0073: 	fi
    0074: 
    0075: 	if [ "$SAVE_CONFIG" -eq 1 -a "$board_flash" = "nand" ]; then

    0065: 	else
    0066: 		sysupgrade_log "sysupgrade firmware"
    0067: 		if [ "$OEM_UPGRADE_BOOT" -eq 1 ]; then
    0068: 			get_image "$1" | dd bs=2k skip="$dd_skip" conv=sync 2>/dev/null | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0069: 		else
    0070: 			get_image "$1" | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0071: 		fi
    0072: 		sysupgrade_log_end "sysupgrade firmware ok"
    0073: 	fi
    0074: 
    0075: 	if [ "$SAVE_CONFIG" -eq 1 -a "$board_flash" = "nand" ]; then
    0076: 		sysupgrade_log "restore config"
    0077: 		mv "$CONF_TAR" "/tmp/persistent/sysupgrade.tgz" 

    0070: 			get_image "$1" | mtd $save_config_str write - "${PART_NAME:-firmware}" >>$SYSUPGRADE_LOG_FILE 2>&1
    0071: 		fi
    0072: 		sysupgrade_log_end "sysupgrade firmware ok"
    0073: 	fi
    0074: 
    0075: 	if [ "$SAVE_CONFIG" -eq 1 -a "$board_flash" = "nand" ]; then
    0076: 		sysupgrade_log "restore config"
    0077: 		mv "$CONF_TAR" "/tmp/persistent/sysupgrade.tgz" 
    0078: 		sysupgrade_log_end "restore config ok"
    0079: 	fi
    0080: }
    0081: 
    0082: blink_led() {

    0072: 		sysupgrade_log_end "sysupgrade firmware ok"
    0073: 	fi
    0074: 
    0075: 	if [ "$SAVE_CONFIG" -eq 1 -a "$board_flash" = "nand" ]; then
    0076: 		sysupgrade_log "restore config"
    0077: 		mv "$CONF_TAR" "/tmp/persistent/sysupgrade.tgz" 
    0078: 		sysupgrade_log_end "restore config ok"
    0079: 	fi
    0080: }
    0081: 
    0082: blink_led() {
    0083: 	. /etc/diag.sh; set_state upgrade
    0084: }

## sbin/sysupgrade

    0006: RAMFS_COPY_BIN=""	# extra programs for temporary ramfs root
    0007: RAMFS_COPY_DATA=""	# extra data files
    0008: export MTD_CONFIG_ARGS=""
    0009: export INTERACTIVE=0
    0010: export VERBOSE=1
    0011: export SAVE_CONFIG=1
    0012: export SAVE_OVERLAY=0
    0013: export SAVE_PARTITIONS=1
    0014: export DELAY=
    0015: export CONF_IMAGE=
    0016: export CONF_BACKUP_LIST=0
    0017: export CONF_BACKUP=
    0018: export CONF_RESTORE=

    0018: export CONF_RESTORE=
    0019: export NEED_IMAGE=
    0020: export HELP=0
    0021: export FORCE=0
    0022: export TEST=0
    0023: export OEM_UPGRADE_BOOT=1
    0024: export OEM_CHECK_IMAGE=
    0025: export REQUIRE_IMAGE_METADATA=1
    0026: 
    0027: # parse options
    0028: while [ -n "$1" ]; do
    0029: 	case "$1" in
    0030: 		-i) export INTERACTIVE=1;;

    0029: 	case "$1" in
    0030: 		-i) export INTERACTIVE=1;;
    0031: 		-d) export DELAY="$2"; shift;;
    0032: 		-v) export VERBOSE="$(($VERBOSE + 1))";;
    0033: 		-q) export VERBOSE="$(($VERBOSE - 1))";;
    0034: 		-n) export SAVE_CONFIG=0;;
    0035: 		-c) export SAVE_OVERLAY=1;;
    0036: 		-p) export SAVE_PARTITIONS=0;;
    0037: 		-b|--create-backup) export CONF_BACKUP="$2" NEED_IMAGE=1; shift;;
    0038: 		-r|--restore-backup) export CONF_RESTORE="$2" NEED_IMAGE=1; shift;;
    0039: 		-l|--list-backup) export CONF_BACKUP_LIST=1; break;;
    0040: 		-e) export OEM_CHECK_IMAGE="$2" NEED_IMAGE=1; shift;;
    0041: 		-f) export CONF_IMAGE="$2"; shift;;

    0050: 	esac
    0051: 	shift;
    0052: done
    0053: 
    0054: export CONFFILES=/tmp/sysupgrade.conffiles
    0055: export CONF_TAR=/tmp/sysupgrade.tgz
    0056: 
    0057: export ARGV="$*"
    0058: export ARGC="$#"
    0059: 
    0060: [ -z "$ARGV" -a -z "$NEED_IMAGE" -o $HELP -gt 0 ] && {
    0061: 	cat <<EOF
    0062: Usage: $0 [<upgrade-option>...] <image file or URL>

    0163: include /lib/upgrade
    0164: 
    0165: [ "$1" = "nand" ] && nand_upgrade_stage2 $@
    0166: 
    0167: do_save_conffiles() {
    0168: 	local conf_tar="${1:-$CONF_TAR}"
    0169: 	local rversion=$(cat /etc/rom_version)
    0170: 
    0171: 	[ -z "$(rootfs_type)" ] && {
    0172: 		echo "Cannot save config while running from ramdisk."
    0173: 		ask_bool 0 "Abort" && exit
    0174: 		return 0
    0175: 	}

    0237: 
    0238: for check in $sysupgrade_image_check; do
    0239: 	( eval "$check \"\$ARGV\"" ) || {
    0240: 		if [ $FORCE -eq 1 ]; then
    0241: 			echo "Image check '$check' failed but --force given - will update anyway!"
    0242: 			OEM_UPGRADE_BOOT=0
    0243: 			break
    0244: 		else
    0245: 			echo "Image check '$check' failed."
    0246: 			OEM_UPGRADE_BOOT=0
    0247: 			exit 1
    0248: 		fi
    0249: 	}

    0241: 			echo "Image check '$check' failed but --force given - will update anyway!"
    0242: 			OEM_UPGRADE_BOOT=0
    0243: 			break
    0244: 		else
    0245: 			echo "Image check '$check' failed."
    0246: 			OEM_UPGRADE_BOOT=0
    0247: 			exit 1
    0248: 		fi
    0249: 	}
    0250: done
    0251: 
    0252: if [ -n "$CONF_IMAGE" ]; then
    0253: 	case "$(get_magic_word $CONF_IMAGE cat)" in

    0256: 		*)
    0257: 			echo "Invalid config file. Please use only .tar.gz files"
    0258: 			exit 1
    0259: 		;;
    0260: 	esac
    0261: 	get_image "$CONF_IMAGE" "cat" > "$CONF_TAR"
    0262: 	export SAVE_CONFIG=1
    0263: elif ask_bool $SAVE_CONFIG "Keep config files over reflash"; then
    0264: 	[ $TEST -eq 1 ] || do_save_conffiles
    0265: 	export SAVE_CONFIG=1
    0266: else
    0267: 	export SAVE_CONFIG=0
    0268: fi

    0257: 			echo "Invalid config file. Please use only .tar.gz files"
    0258: 			exit 1
    0259: 		;;
    0260: 	esac
    0261: 	get_image "$CONF_IMAGE" "cat" > "$CONF_TAR"
    0262: 	export SAVE_CONFIG=1
    0263: elif ask_bool $SAVE_CONFIG "Keep config files over reflash"; then
    0264: 	[ $TEST -eq 1 ] || do_save_conffiles
    0265: 	export SAVE_CONFIG=1
    0266: else
    0267: 	export SAVE_CONFIG=0
    0268: fi
    0269: 

    0258: 			exit 1
    0259: 		;;
    0260: 	esac
    0261: 	get_image "$CONF_IMAGE" "cat" > "$CONF_TAR"
    0262: 	export SAVE_CONFIG=1
    0263: elif ask_bool $SAVE_CONFIG "Keep config files over reflash"; then
    0264: 	[ $TEST -eq 1 ] || do_save_conffiles
    0265: 	export SAVE_CONFIG=1
    0266: else
    0267: 	export SAVE_CONFIG=0
    0268: fi
    0269: 
    0270: if [ $TEST -eq 1 ]; then

    0260: 	esac
    0261: 	get_image "$CONF_IMAGE" "cat" > "$CONF_TAR"
    0262: 	export SAVE_CONFIG=1
    0263: elif ask_bool $SAVE_CONFIG "Keep config files over reflash"; then
    0264: 	[ $TEST -eq 1 ] || do_save_conffiles
    0265: 	export SAVE_CONFIG=1
    0266: else
    0267: 	export SAVE_CONFIG=0
    0268: fi
    0269: 
    0270: if [ $TEST -eq 1 ]; then
    0271: 	exit 0
    0272: fi

    0262: 	export SAVE_CONFIG=1
    0263: elif ask_bool $SAVE_CONFIG "Keep config files over reflash"; then
    0264: 	[ $TEST -eq 1 ] || do_save_conffiles
    0265: 	export SAVE_CONFIG=1
    0266: else
    0267: 	export SAVE_CONFIG=0
    0268: fi
    0269: 
    0270: if [ $TEST -eq 1 ]; then
    0271: 	exit 0
    0272: fi
    0273: 
    0274: run_hooks "" $sysupgrade_pre_upgrade

    0293: 
    0294: trap '' SIGINT SIGHUP SIGTERM SIGPIPE SIGQUIT SIGUSR1 SIGUSR2 SIGABRT SIGTSTP SIGCONT
    0295: 
    0296: if [ -n "$(rootfs_type)" ]; then
    0297: 	v "Switching to ramdisk..."
    0298: 	(run_ramfs '. /lib/functions.sh; include /lib/upgrade; do_upgrade') &
    0299: else
    0300: 	(do_upgrade) &
    0301: fi

    0295: 
    0296: if [ -n "$(rootfs_type)" ]; then
    0297: 	v "Switching to ramdisk..."
    0298: 	(run_ramfs '. /lib/functions.sh; include /lib/upgrade; do_upgrade') &
    0299: else
    0300: 	(do_upgrade) &
    0301: fi

## lib/upgrade/common.sh

    0043: 		mtd_name="kpanic"
    0044: 		mtdpart="$(find_mtd_part $mtd_name)"
    0045: 		[ -z "$mtdpart" ] && return 1
    0046: 	}
    0047: 
    0048: 	mtd -q write "$SYSUPGRADE_LOG_FILE" "$mtd_name"
    0049: }
    0050: 
    0051: lede_reboot() {
    0052: 	sysupgrade_log "reboot failed, force reboot"
    0053: 	sysupgrade_log_end
    0054: 	sleep 1
    0055: 

    0382: 			printf "%2d %5d %7d\n" $part $lba $num >> "/tmp/partmap.$filename"
    0383: 		done
    0384: 	fi
    0385: }
    0386: 
    0387: jffs2_copy_config() {
    0388: 	if grep rootfs_data /proc/mtd >/dev/null; then
    0389: 		# squashfs+jffs2
    0390: 		mtd -e rootfs_data jffs2write "$CONF_TAR" rootfs_data
    0391: 	else
    0392: 		# jffs2
    0393: 		mtd jffs2write "$CONF_TAR" rootfs
    0394: 	fi

    0383: 		done
    0384: 	fi
    0385: }
    0386: 
    0387: jffs2_copy_config() {
    0388: 	if grep rootfs_data /proc/mtd >/dev/null; then
    0389: 		# squashfs+jffs2
    0390: 		mtd -e rootfs_data jffs2write "$CONF_TAR" rootfs_data
    0391: 	else
    0392: 		# jffs2
    0393: 		mtd jffs2write "$CONF_TAR" rootfs
    0394: 	fi
    0395: }

    0384: 	fi
    0385: }
    0386: 
    0387: jffs2_copy_config() {
    0388: 	if grep rootfs_data /proc/mtd >/dev/null; then
    0389: 		# squashfs+jffs2
    0390: 		mtd -e rootfs_data jffs2write "$CONF_TAR" rootfs_data
    0391: 	else
    0392: 		# jffs2
    0393: 		mtd jffs2write "$CONF_TAR" rootfs
    0394: 	fi
    0395: }
    0396: 

    0385: }
    0386: 
    0387: jffs2_copy_config() {
    0388: 	if grep rootfs_data /proc/mtd >/dev/null; then
    0389: 		# squashfs+jffs2
    0390: 		mtd -e rootfs_data jffs2write "$CONF_TAR" rootfs_data
    0391: 	else
    0392: 		# jffs2
    0393: 		mtd jffs2write "$CONF_TAR" rootfs
    0394: 	fi
    0395: }
    0396: 
    0397: # Flash firmware to MTD partition

    0387: jffs2_copy_config() {
    0388: 	if grep rootfs_data /proc/mtd >/dev/null; then
    0389: 		# squashfs+jffs2
    0390: 		mtd -e rootfs_data jffs2write "$CONF_TAR" rootfs_data
    0391: 	else
    0392: 		# jffs2
    0393: 		mtd jffs2write "$CONF_TAR" rootfs
    0394: 	fi
    0395: }
    0396: 
    0397: # Flash firmware to MTD partition
    0398: #
    0399: # $(1): path to image

    0388: 	if grep rootfs_data /proc/mtd >/dev/null; then
    0389: 		# squashfs+jffs2
    0390: 		mtd -e rootfs_data jffs2write "$CONF_TAR" rootfs_data
    0391: 	else
    0392: 		# jffs2
    0393: 		mtd jffs2write "$CONF_TAR" rootfs
    0394: 	fi
    0395: }
    0396: 
    0397: # Flash firmware to MTD partition
    0398: #
    0399: # $(1): path to image
    0400: # $(2): (optional) pipe command to extract firmware, e.g. dd bs=n skip=m

    0396: 
    0397: # Flash firmware to MTD partition
    0398: #
    0399: # $(1): path to image
    0400: # $(2): (optional) pipe command to extract firmware, e.g. dd bs=n skip=m
    0401: default_do_upgrade() {
    0402: 	sync
    0403: 	if [ "$SAVE_CONFIG" -eq 1 ]; then
    0404: 		get_image "$1" "$2" | mtd $MTD_CONFIG_ARGS -j "$CONF_TAR" write - "${PART_NAME:-image}"
    0405: 	else
    0406: 		get_image "$1" "$2" | mtd write - "${PART_NAME:-image}"
    0407: 	fi
    0408: }

    0398: #
    0399: # $(1): path to image
    0400: # $(2): (optional) pipe command to extract firmware, e.g. dd bs=n skip=m
    0401: default_do_upgrade() {
    0402: 	sync
    0403: 	if [ "$SAVE_CONFIG" -eq 1 ]; then
    0404: 		get_image "$1" "$2" | mtd $MTD_CONFIG_ARGS -j "$CONF_TAR" write - "${PART_NAME:-image}"
    0405: 	else
    0406: 		get_image "$1" "$2" | mtd write - "${PART_NAME:-image}"
    0407: 	fi
    0408: }
    0409: 
    0410: do_upgrade() {

    0399: # $(1): path to image
    0400: # $(2): (optional) pipe command to extract firmware, e.g. dd bs=n skip=m
    0401: default_do_upgrade() {
    0402: 	sync
    0403: 	if [ "$SAVE_CONFIG" -eq 1 ]; then
    0404: 		get_image "$1" "$2" | mtd $MTD_CONFIG_ARGS -j "$CONF_TAR" write - "${PART_NAME:-image}"
    0405: 	else
    0406: 		get_image "$1" "$2" | mtd write - "${PART_NAME:-image}"
    0407: 	fi
    0408: }
    0409: 
    0410: do_upgrade() {
    0411: 	v "Performing system upgrade..."

    0401: default_do_upgrade() {
    0402: 	sync
    0403: 	if [ "$SAVE_CONFIG" -eq 1 ]; then
    0404: 		get_image "$1" "$2" | mtd $MTD_CONFIG_ARGS -j "$CONF_TAR" write - "${PART_NAME:-image}"
    0405: 	else
    0406: 		get_image "$1" "$2" | mtd write - "${PART_NAME:-image}"
    0407: 	fi
    0408: }
    0409: 
    0410: do_upgrade() {
    0411: 	v "Performing system upgrade..."
    0412: 	sysupgrade_log "Performing system upgrade..."
    0413: 	if type 'platform_do_upgrade' >/dev/null 2>/dev/null; then

    0405: 	else
    0406: 		get_image "$1" "$2" | mtd write - "${PART_NAME:-image}"
    0407: 	fi
    0408: }
    0409: 
    0410: do_upgrade() {
    0411: 	v "Performing system upgrade..."
    0412: 	sysupgrade_log "Performing system upgrade..."
    0413: 	if type 'platform_do_upgrade' >/dev/null 2>/dev/null; then
    0414: 		platform_do_upgrade "$ARGV"
    0415: 	else
    0416: 		default_do_upgrade "$ARGV"
    0417: 	fi

    0408: }
    0409: 
    0410: do_upgrade() {
    0411: 	v "Performing system upgrade..."
    0412: 	sysupgrade_log "Performing system upgrade..."
    0413: 	if type 'platform_do_upgrade' >/dev/null 2>/dev/null; then
    0414: 		platform_do_upgrade "$ARGV"
    0415: 	else
    0416: 		default_do_upgrade "$ARGV"
    0417: 	fi
    0418: 
    0419: 	if [ "$SAVE_CONFIG" -eq 1 ] && type 'platform_copy_config' >/dev/null 2>/dev/null; then
    0420: 		platform_copy_config

    0409: 
    0410: do_upgrade() {
    0411: 	v "Performing system upgrade..."
    0412: 	sysupgrade_log "Performing system upgrade..."
    0413: 	if type 'platform_do_upgrade' >/dev/null 2>/dev/null; then
    0414: 		platform_do_upgrade "$ARGV"
    0415: 	else
    0416: 		default_do_upgrade "$ARGV"
    0417: 	fi
    0418: 
    0419: 	if [ "$SAVE_CONFIG" -eq 1 ] && type 'platform_copy_config' >/dev/null 2>/dev/null; then
    0420: 		platform_copy_config
    0421: 	fi

    0411: 	v "Performing system upgrade..."
    0412: 	sysupgrade_log "Performing system upgrade..."
    0413: 	if type 'platform_do_upgrade' >/dev/null 2>/dev/null; then
    0414: 		platform_do_upgrade "$ARGV"
    0415: 	else
    0416: 		default_do_upgrade "$ARGV"
    0417: 	fi
    0418: 
    0419: 	if [ "$SAVE_CONFIG" -eq 1 ] && type 'platform_copy_config' >/dev/null 2>/dev/null; then
    0420: 		platform_copy_config
    0421: 	fi
    0422: 
    0423: 	v "Upgrade completed"

    0414: 		platform_do_upgrade "$ARGV"
    0415: 	else
    0416: 		default_do_upgrade "$ARGV"
    0417: 	fi
    0418: 
    0419: 	if [ "$SAVE_CONFIG" -eq 1 ] && type 'platform_copy_config' >/dev/null 2>/dev/null; then
    0420: 		platform_copy_config
    0421: 	fi
    0422: 
    0423: 	v "Upgrade completed"
    0424: 	sysupgrade_log "Upgrade completed"
    0425: 	[ -n "$DELAY" ] && sleep "$DELAY"
    0426: 	v "Rebooting system..."

