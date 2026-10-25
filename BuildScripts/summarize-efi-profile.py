"""Summarize only whitelisted non-identifying fields from a saved EFI plist."""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--config', type=Path, required=True)
parser.add_argument('--reconstruct-software-cursor', action='store_true')
parser.add_argument('--expected-sha256')
args = parser.parse_args()
data = args.config.read_bytes()
config = plistlib.loads(data)
guid = '7C436110-AB2A-4BBB-A880-FE41995C9F82'
nvram = config['NVRAM']['Add'][guid]
if args.reconstruct_software_cursor:
    assert '-hvgfxfbswcursor' not in nvram['boot-args'].split()
    nvram['boot-args'] += ' -hvgfxfbswcursor'
    data = plistlib.dumps(config, sort_keys=False)
digest = hashlib.sha256(data).hexdigest()
if args.expected_sha256:
    assert digest == args.expected_sha256
allowed_args = {'-v', 'keepsyms=1', 'debug=0x12a', 'serial=5', 'msgbuf=1048576',
                '-hvstordbg', '-hvstormsgdbg', '-hvvmbusdbg', '-hvvmbusdebdbg',
                '-hvctrldbg', '-hvgfxdbg', '-hvgfxfbdbg', '-nobsdmgroot',
                '-hvgfxfbswcursor'}
allowed_bundles = {'MacHyperVSupport.kext', 'MacHyperVSupportMonterey.kext',
                   'MacHyperVFramebuffer.kext', 'Lilu.kext', 'VirtualSMC.kext'}
allowed_acpi = {'SSDT-HV-VMBUS.aml', 'SSDT-HV-DEV.aml', 'SSDT-HV-PLUG.aml'}
quirks = ['ProvideCurrentCpuInfo', 'AppleXcpmCfgLock', 'AppleCpuPmCfgLock',
          'DisableIoMapper', 'PanicNoKextDump', 'PowerTimeoutKernelPanic']
result = {
    'scope': 'Saved audited configuration; not a live disk read',
    'software_cursor_reconstructed_from_recorded_single_change': args.reconstruct_software_cursor,
    'config_sha256': digest,
    'boot_arguments': [v for v in nvram['boot-args'].split() if v in allowed_args],
    'unlisted_boot_argument_count': sum(v not in allowed_args for v in nvram['boot-args'].split()),
    'sip_csr_active_config_hex': nvram.get('csr-active-config', b'').hex(),
    'kernel_quirks': {key: config['Kernel']['Quirks'].get(key) for key in quirks},
    'cpuid_data_hex': config['Kernel']['Emulate'].get('Cpuid1Data', b'').hex(),
    'cpuid_mask_hex': config['Kernel']['Emulate'].get('Cpuid1Mask', b'').hex(),
    'acpi': [{'path': v['Path'], 'enabled': v['Enabled']} for v in config['ACPI']['Add']
             if v.get('Path') in allowed_acpi],
    'kexts': [{'bundle': v['BundlePath'], 'enabled': v['Enabled'],
               'minimum_kernel': v.get('MinKernel', ''), 'maximum_kernel': v.get('MaxKernel', '')}
              for v in config['Kernel']['Add'] if v.get('BundlePath') in allowed_bundles],
    'privacy': 'Full configuration, platform identity, serials, device paths and other NVRAM omitted',
}
print(json.dumps(result, indent=2))
