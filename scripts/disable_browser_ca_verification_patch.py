import re
import sys
import argparse
import logging
import os
import lz4.block
import io

import modules


def main():
    logger_interface.info('Extracting ROMFS BootImagePackage from provided firmware files.')
    os.system(f'{modules.hactoolnet} --keyset {args.prod_keys} --intype switchfs --raw {args.firmware} --title 0100000000000803 --romfsdir 0100000000000803/romfs/')

    with open('0100000000000803/romfs/nro/netfront/core_2/default/cfi_enabled/webkit_wkc.nro.lz4', 'rb') as file:
        input_data = file.read()
        decompressed = lz4.block.decompress(input_data)

    with open('0100000000000803/romfs/uncompressed_browser_ssl.nro', 'wb') as decompressed_browser_file:
        decompressed_browser_file.write(decompressed)

    result = re.search(rb'\x72\x48\x00\x80\x52\xe2\x13\x88\x1a', decompressed)
    ips_patch1 = '%08X%s%s' % (result.start() + 0x1, '0004', 'E8031F2A')
    ips_patch2 = '%08X%s%s' % (result.end(), '0001', '1F')

    ips_header = b'IPS32'.hex()
    ips_footer = b'EEOF'.hex()
    ips_hash = modules.get_build_id(io.BytesIO(decompressed))
    logger_interface.info('IPS patch hash %s',ips_hash )

    with open(f'./patches/atmosphere/nro_patches/disable_browser_ca_verification/{ips_hash}.ips', 'wb') as text_file:
        text_file.write(bytes.fromhex(ips_header + ips_patch1 + ips_patch2 + ips_footer))
    logger_interface.info('Disable CA Verification patch done!')

    shutil.rmtree('0100000000000024')


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--firmware", help="firmware folder", dest="firmware", type=str, default="./firmware")
    argParser.add_argument("-k", "--keys", help="keyfile to use", dest="prod_keys", type=str, default="./prod.keys")
    args = argParser.parse_args()

    logger_interface = logging.getLogger('keygen')
    modules.logging_configuration(logger_interface)
    sys.exit(main())
