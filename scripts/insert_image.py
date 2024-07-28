import re
import sys
import argparse
import logging
import os
import struct
from PIL import Image

import modules
import modules.insert_splash_screen as iss
import modules.switch_logo_patcher as slp

SPLASH_SCREEN_WIDTH  = 1280
SPLASH_SCREEN_HEIGHT = 720

SPLASH_SCREEN_STRIDE = 768

# 308 * 350 * 4
# 210 * 172 * 4


def insert_firmware_logo():
    slp.create_patch(args.build_id, args.offset, args.input_image, args.original_image)


def insert_inc_logo():
    source_image = Image.open(args.input_image, 'r')
    if source_image.size() != (210, 172):
        logger_interface.error("Image not 210x172, plz resize it")
        sys.exit(1)

    hex_string = source_image.tobytes().hex()
    hex_list = []
    for i in range(0, len(hex_string), 8):
        hex_list.append('0x' + hex_string[i:i + 8][::-1])
    inc_string = 'constexpr u32 SplashScreen[] =  {' + ', '.join(hex_list) + '};'
    with open('./result-inc.txt', 'w') as file_object:
        file_object.write(inc_string)


def insert_spash_bin():
    splash_bin = iss.convert_image(args.input_image)
    with open('./result-splach.bin', 'wb') as file_object:
        file_object.write(splash_bin)


def patch_package3():
    iss.main(3, (args.patch_file, args.input_image))


def main():
    ext_type = {
        'firmware': insert_firmware_logo,
        'inc': insert_inc_logo,
        'bin': insert_spash_bin,
        'package3': patch_package3
    }
    logger_interface.info('Selected %s', args.ext_type)
    ext_type[args.ext_type]()
    logger_interface.info('Extracting is success: %s', args.out_image)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--firmware", help="firmware folder", dest="firmware", type=str, default="./firmware")
    argParser.add_argument("-k", "--keys", help="keyfile to use", dest="prod_keys", type=str, default="./prod.keys")
    argParser.add_argument("-t", "--type", help="source type", dest="ext_type", type=str, choices=['firmware', 'inc', 'bin'], required=True)
    argParser.add_argument("-p", "--patch-file", help="patch file", dest="patch_file", type=str, default="./package3")
    argParser.add_argument("-i", "--image", help="input image", dest="input_image", type=str, default="./source.png")
    argParser.add_argument("-o", "--original-image", help="original image", dest="original_image", type=str)
    argParser.add_argument("--build-id", help="build id", dest="build_id", type=str)
    argParser.add_argument("--offset", help="offset", dest="offset", type=str)

    args = argParser.parse_args()

    logger_interface = logging.getLogger('extract image')
    modules.logging_configuration(logger_interface)
    sys.exit(main())
