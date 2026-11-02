"""Read back full Apple installer payload and OS version from a converted ISO."""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--sevenzip', type=Path, required=True)
p.add_argument('--iso', type=Path, required=True)
p.add_argument('--package-sha256', required=True)
p.add_argument('--version', required=True)
p.add_argument('--build', required=True)
p.add_argument('--receipt', type=Path, required=True)
a = p.parse_args()
if a.receipt.exists():
    p.error('Refusing to overwrite receipt')
root = 'Install macOS Tahoe\\'
def command(member):
    return [str(a.sevenzip), 'x', '-so', '-bd', str(a.iso), root + member]
version = plistlib.loads(subprocess.check_output(command('System\\Library\\CoreServices\\SystemVersion.plist')))
if (version['ProductVersion'], version['ProductBuildVersion']) != (a.version, a.build):
    raise SystemExit('Unexpected OS version: ' + repr(version))
process = subprocess.Popen(command('Install macOS Tahoe.app\\Contents\\SharedSupport\\SharedSupport.dmg'),
                           stdout=subprocess.PIPE)
sha = hashlib.sha256()
total = 0
while True:
    data = process.stdout.read(8 * 1024 * 1024)
    if not data:
        break
    total += len(data)
    sha.update(data)
if process.wait() != 0 or total == 0 or sha.hexdigest().lower() != a.package_sha256.lower():
    raise SystemExit('ISO payload readback FAILED: ' + str(total) + ' bytes, SHA256 ' + sha.hexdigest())
result = {'iso': a.iso.name, 'version': version['ProductVersion'],
          'build': version['ProductBuildVersion'], 'shared_support_bytes': total,
          'shared_support_sha256': sha.hexdigest(),
          'verification': 'PASS: full ISO payload equals signature-verified original Apple package',
          'boot_test': 'separate runtime test required'}
with a.receipt.open('x', encoding='utf-8') as output:
    json.dump(result, output, indent=2)
print(json.dumps(result))
