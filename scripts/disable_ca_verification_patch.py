import re
import sys
import argparse
import logging
import os

import modules


def main():
    logger_interface.info('Extracting ROMFS BootImagePackage from provided firmware files.')
    os.system(f'{modules.hactoolnet} --keyset {args.prod_keys} --intype switchfs --raw {args.firmware} --title 0100000000000024 --exefsdir titleid/0100000000000024/exefs/')
    os.system(f'{modules.hactool} --keyset {args.prod_keys} --intype nso0 --raw titleid/0100000000000024/exefs/main --uncompressed titleid/0100000000000024/exefs/uncompressed_ssl.nso0')

    with open('titleid/0100000000000024/exefs/uncompressed_ssl.nso0', 'rb') as fi:
        read_data = fi.read()
        result1 = re.search(rb'\x6a\x00\x80\xd2', read_data)
        result23 = re.search(rb'\x24\x09\x43\x7a\xa0\x00\x00\x54', read_data)
        result4 = re.search(rb'\x88\x16\x00\x12', read_data)
        ips_patch1 = '%08X%s%s' % (result1.start(), '0001', '0A')
        ips_patch2 = '%08X%s%s' % (result23.end() - 4, '0002', '1000')
        ips_patch3 = '%08X%s%s' % (result23.end() - 1, '0001', '14')
        ips_patch4 = '%08X%s%s' % (result4.end(), '0004', '08008052')

        ips_hash = modules.get_build_id(fi)
        logger_interface.info('IPS patch hash %s',ips_hash )
        with open (f'./patches/atmosphere/exefs_patches/disable_ca_verification/{ips_hash}.ips', 'wb') as text_file:
            text_file.write(bytes.fromhex(modules.IPS32_HEADER + ips_patch1 + ips_patch2 + ips_patch3 + ips_patch4 + modules.IPS32_FOOTER))
        logger_interface.info('Disable CA Verification patch done!')

    shutil.rmtree('titleid')


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--firmware", help="firmware folder", dest="firmware", type=str, default="./firmware")
    argParser.add_argument("-k", "--keys", help="keyfile to use", dest="prod_keys", type=str, default="./prod.keys")
    args = argParser.parse_args()

    logger_interface = logging.getLogger('keygen')
    modules.logging_configuration(logger_interface)
    sys.exit(main())
