"""Render a local Hyper-V RGB565 thumbnail for read-only VM observation."""
import argparse
from pathlib import Path
import struct
import zlib


def chunk(kind, body):
    return (struct.pack('>I', len(body)) + kind + body
            + struct.pack('>I', zlib.crc32(kind + body) & 0xffffffff))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--width', type=int, default=1024)
    parser.add_argument('--height', type=int, default=768)
    args = parser.parse_args()
    data = args.input.read_bytes()
    expected = args.width * args.height * 2
    # This host's thumbnail result prefixes the pixel data with four bytes.
    if len(data) == expected + 4:
        data = data[4:]
    if len(data) != expected:
        raise ValueError('Unexpected thumbnail dimensions/byte count')
    pixels = bytearray()
    for row in range(args.height):
        pixels.append(0)
        for x in range(args.width):
            value = struct.unpack_from('<H', data, (row * args.width + x) * 2)[0]
            pixels.extend((((value >> 11) & 31) * 255 // 31,
                           ((value >> 5) & 63) * 255 // 63,
                           (value & 31) * 255 // 31))
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', args.width, args.height, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b''))
    destination = args.input.with_suffix('.png')
    with destination.open('xb') as output:
        output.write(png)
    print(destination)


if __name__ == '__main__':
    main()
