"""Extract signed XAR TOC and certificates; this alone does not establish trust."""
import argparse
import base64
import hashlib
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zlib

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('package', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
a.output.mkdir(exist_ok=False)
with a.package.open('rb') as source:
    magic, size, version, compressed_size, expanded_size, algo = struct.unpack('>4sHHQQI', source.read(28))
    assert magic == b'xar!' and size == 28 and version == 1 and algo == 1
    compressed = source.read(compressed_size)
    toc = zlib.decompress(compressed)
    assert len(toc) == expanded_size
    root = ET.fromstring(toc)
    checksum = root.find('toc/checksum')
    assert checksum.attrib['style'] == 'sha1'
    source.seek(size + compressed_size + int(checksum.findtext('offset')))
    assert source.read(int(checksum.findtext('size'))) == hashlib.sha1(compressed).digest()
    signature = root.find('toc/signature')
    assert signature.attrib['style'] == 'RSA'
    source.seek(size + compressed_size + int(signature.findtext('offset')))
    (a.output / 'signature.bin').write_bytes(source.read(int(signature.findtext('size'))))
    (a.output / 'toc.compressed').write_bytes(compressed)
    for n, cert in enumerate(signature.findall('.//{http://www.w3.org/2000/09/xmldsig#}X509Certificate')):
        der = base64.b64decode(cert.text)
        text = base64.b64encode(der).decode()
        (a.output / f'cert{n}.pem').write_text('-----BEGIN CERTIFICATE-----\n' + '\n'.join(text[i:i+64] for i in range(0,len(text),64)) + '\n-----END CERTIFICATE-----\n', encoding='ascii')
print('TOC SHA1:', hashlib.sha1(compressed).hexdigest())
