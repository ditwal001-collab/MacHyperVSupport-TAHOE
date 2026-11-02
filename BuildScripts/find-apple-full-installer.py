"""Select an exact full installer from Apple's original software-update catalog."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import plistlib
import re
import urllib.parse
import urllib.request

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--catalog', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--version', default='26.7.1')
parser.add_argument('--build', default='25G241')
args = parser.parse_args()
catalog = plistlib.loads(args.catalog.read_bytes())


def apple_url(url):
    url = url.replace('http://', 'https://', 1)
    parts = urllib.parse.urlparse(url)
    assert parts.scheme == 'https' and parts.hostname.endswith('.apple.com')
    return url


def inspect(item):
    pid, product = item
    packages = [v for v in product.get('Packages', [])
                if urllib.parse.urlparse(v['URL']).path.endswith('/InstallAssistant.pkg')]
    if not packages:
        return None
    distributions = product.get('Distributions', {})
    url = distributions.get('English', distributions.get('en'))
    if not url:
        return None
    with urllib.request.urlopen(apple_url(url), timeout=60) as response:
        text = response.read().decode('utf-8')
    def value(keys):
        for key in keys:
            match = re.search(r'<key>' + key + r'</key>\s*<string>(.*?)</string>', text)
            if match:
                return match[1]
        return None
    version = value(['macOSProductVersion', 'VERSION'])
    build = value(['macOSProductBuildVersion', 'BUILD'])
    return pid, product, packages, version, build, text, url


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    products = [v for v in pool.map(inspect, catalog['Products'].items()) if v]
matches = [v for v in products if v[3:5] == (args.version, args.build)]
if len(matches) != 1:
    raise SystemExit(json.dumps({'matching_products': len(matches),
                                'available': [{'version': v[3], 'build': v[4]} for v in products]}))
pid, product, packages, version, build, distribution, url = matches[0]
assert len(packages) == 1
package = packages[0]
digest = package.get('Digest', '')
if isinstance(digest, bytes):
    digest = digest.hex()
result = {'product': pid, 'version': version, 'build': build,
          'url': apple_url(package['URL']), 'bytes': package['Size'],
          'distribution_url': apple_url(url),
          'catalog_sha256': hashlib.sha256(args.catalog.read_bytes()).hexdigest(),
          'distribution_sha256': hashlib.sha256(distribution.encode()).hexdigest(),
          'catalog_digest_hex': digest,
          'source': 'Apple original catalog and product distribution; not a recovery image'}
with args.output.open('x', encoding='utf-8') as out:
    json.dump(result, out, indent=2)
args.output.with_suffix('.distribution.xml').write_text(distribution, encoding='utf-8')
print(json.dumps(result, indent=2))
