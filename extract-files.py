#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/nokia/NB1',
    'hardware/qcom-caf/msm8998',
    'vendor/nokia/msm8998-common',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    # Load sensors.rangefinder.so from /vendor partition
    'vendor/lib/libmmcamera2_stats_modules.so': blob_fixup()
	.replace_needed('system/lib64/sensors.rangefinder.so', 'vendor/lib64/sensors.rangefinder.so')
	.replace_needed('system/lib/sensors.rangefinder.so', 'vendor/lib/sensors.rangefinder.so'),
    # Patch gx_fpd for VNDK support
    'vendor/bin/gx_fpd': blob_fixup()
	.patchelf_version('0_17_2')
	.remove_needed('libunwind.so')
	.remove_needed('libbacktrace.so')
	.add_needed('liblog.so')
	.add_needed('libshim_binder.so')
	.add_needed('libfakelogprint.so')
	.replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/hw/fingerprint.msm8998.so': blob_fixup()
        .patchelf_version('0_17_2')
        .add_needed('libfakelogprint.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    ('vendor/lib64/libfp_client.so', 'vendor/lib64/libfpservice.so'): blob_fixup()
        .patchelf_version('0_17_2')
	.replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libfpjni.so': blob_fixup()
	.patchelf_version('0_17_2')
	.remove_needed('libandroid_runtime.so')
	.remove_needed('libnativehelper.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    # Hexedit gxfingerprint to load Goodix firmware from /vendor/firmware/
    'vendor/lib64/hw/gxfingerprint.default.so': blob_fixup()
        .patchelf_version('0_17_2')
        .add_needed('libfakelogprint.so')
        .replace_needed('/system/etc/firmware', '/vendor/firmware')
	.replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'NB1',
    'nokia',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'msm8998-common', module.vendor
    )
    utils.run()
