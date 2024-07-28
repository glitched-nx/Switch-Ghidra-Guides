import re
import sys
import argparse
import logging
import os
import struct
from PIL import Image

import modules

SPLASH_SCREEN_WIDTH  = 1280
SPLASH_SCREEN_HEIGHT = 720

SPLASH_SCREEN_STRIDE = 768

# 308 * 350 * 4
# 210 * 172 * 4


def extract_firmware_logo():
    logger_interface.info('Extracting ROMFS BootImagePackage from provided firmware files.')
    os.system(f'{modules.hactoolnet} --keyset {args.prod_keys} --intype switchfs --raw {args.firmware} --title 010000000000002D --exefsdir titleid/010000000000002D/exefs/')
    os.system(f'{modules.hactool} --keyset {args.prod_keys} --intype nso0 --raw titleid/010000000000002D/exefs/main --uncompressed titleid/010000000000002D/exefs/uncompressed_vi.nso0')

    with open('titleid/010000000000002D/exefs/uncompressed_vi.nso0', 'rb') as fi:
        read_data = fi.read()
        vi_build_id = modules.get_build_id(fi)
        logger_interface.info('VI build ID %s', vi_build_id)
        if not re.search(b'\x4E\x53\x4F\x30', read_data):
            logger_interface.error('nso0 magic not found! - Script needs to be fixed, VI is not correct!')
            sys.exit(0)

        zb = 4
        logo_pattern = re.compile(b'\x00'*zb+b'\x00\x00\x00\xFF\x00\x00\x00\xFF')
        start_offset = logo_pattern.search(read_data).start() + 0x1*zb
        logger_interface.info('Offset: %s', start_offset)
        end_offset = start_offset + (308 * 350 * 4)
        with open('logo.data', 'wb') as logo_object:
            logo_object.write(read_data[start_offset:end_offset])
        out_img = Image.frombytes("RGBA", (308, 350), read_data[start_offset:end_offset])
        out_img.save(args.out_image)


def extract_inc_logo():
    with open(args.raw_file, 'r') as fi:
        read_data = fi.read()
        logo_pattern = re.compile(r'\=\s\{0xFF000000.*\}\;')
        raw_line = logo_pattern.search(read_data).group().lstrip('= {').rstrip('};').replace(' ', '').replace('0x', '')
        hex_list = [i[::-1] for i in raw_line.split(',')]
        result = ''.join(hex_list)
        print(len(bytes.fromhex(result)))
        with open('logo-inc.data', 'wb') as logo_object:
            logo_object.write(bytes.fromhex(result))
    out_img = Image.frombytes("RGBA", (210, 172), bytes.fromhex(result))
    out_img.save(args.out_image)


def extract_spash_bin():
    with open(args.raw_file, 'rb') as splash_object:
        out_img = Image.new('RGBA', (SPLASH_SCREEN_WIDTH, SPLASH_SCREEN_HEIGHT), (255, 255, 255, 255))
        out_img = out_img.transpose(Image.ROTATE_90)
        for row in range(SPLASH_SCREEN_WIDTH):
            for col in range(SPLASH_SCREEN_HEIGHT):
                b, g, r, a = struct.unpack('<BBBB', splash_object.read(4))
                out_img.putpixel((col, row), (r, g, b, a))
            splash_object.seek(splash_object.tell() + ((SPLASH_SCREEN_STRIDE - SPLASH_SCREEN_HEIGHT) * 4))
        out_img.save(args.out_image)


def main():
    ext_type = {
        'firmware': extract_firmware_logo,
        'inc': extract_inc_logo,
        'bin': extract_spash_bin
    }
    logger_interface.info('Selected %s', args.ext_type)
    ext_type[args.ext_type]()
    logger_interface.info('Extracting is success: %s', args.out_image)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--firmware", help="firmware folder", dest="firmware", type=str, default="./firmware")
    argParser.add_argument("-k", "--keys", help="keyfile to use", dest="prod_keys", type=str, default="./prod.keys")
    argParser.add_argument("-t", "--type", help="source type", dest="ext_type", type=str, choices=['firmware', 'inc', 'bin'], required=True)
    argParser.add_argument("-r", "--raw", help="file", dest="raw_file", type=str)
    argParser.add_argument("-i", "--image", help="output image", dest="out_image", type=str, default="./out.png")

    args = argParser.parse_args()

    logger_interface = logging.getLogger('extract image')
    modules.logging_configuration(logger_interface)
    sys.exit(main())