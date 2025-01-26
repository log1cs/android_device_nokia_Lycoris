#!/vendor/bin/sh

#+FIH@R3J168: FEATURE_FIH_C_NOKIA_001 (8998), by Pupu
# SH for fih_atl
if [ -f /data/vendor/fih_atl/modem_config/mcfg_sw/oem_ver.txt ]; then
    pre_fihver=`cat /data/vendor/fih_atl/modem_config/mcfg_sw/oem_ver.txt`
else
    pre_fihver=""
fi
cur_fihver=`cat /vendor/firmware_mnt/image/modem_pr/mcfg/configs/mcfg_sw/oem_ver.txt`
if [ ! -f /vendor/firmware_mnt/image/modem_pr/mcfg/configs/mcfg_sw/oem_ver.txt -o "$pre_fihver" != "$cur_fihver" ]; then
    chmod g+w -R /data/vendor/fih_atl/modem_config/*
    rm -rf /data/vendor/fih_atl/modem_config/*
    cp -r /vendor/firmware_mnt/image/modem_pr/mcfg/configs/* /data/vendor/fih_atl/modem_config
    cp /vendor/firmware_mnt/verinfo/ver_info.txt /data/vendor/fih_atl/modem_config/ver_info.txt
    chown -hR system.root /data/vendor/fih_atl/modem_config/*
    chmod -R 770 /data/vendor/fih_atl/modem_config/*
fi
chown -hR system.vendor_rfs /data/vendor/fih_atl

# SH for fih_mcfg
setprop persist.vendor.radio.nokia_fih_mcfg 1
#-FIH@R3J168: FEATURE_FIH_C_NOKIA_001 (8998), by Pupu
