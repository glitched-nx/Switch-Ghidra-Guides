import re
import os
import sys
import hashlib
import logging
import argparse
import shutil
import platform

import modules

def check_key_file(file_path):
    result = True
    valid_hashes = {
        'mariko_bek':'dac25c717109976b8dac45d9184e9c11',
        'mariko_kek': '4a4eea6d1a812ee7aa1dfd9a3f71bc27',
        'master_key_00': 'c069db652c88b7edc4f31127a3331678',
    }
    ns_keys = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.replace(' ', '').rstrip().split('=')
            ns_keys[key] = value

    for p_key in ns_keys.keys():
        if 'package1_key_' in p_key:
            break
    else:
        logger_interface.error('package1_key_<> is missing in keys file, we cannot proceed with keygen as package1 cannot be opened for the purpose of obtaining master_kek_source. Exiting.')
        result = False

    for p_key in ns_keys.keys():
        if 'tsec_root_key_' in p_key:
            break
    else:
        logger_interface.error('tsec_root_key_<> is missing in keys file, we cannot derive a new master_kek from the new master_kek_source, keygen will not yield new keys. Exiting.')
        result = False

    for p_key, p_value_hash in valid_hashes.items():
        t_hash = hashlib.md5(ns_keys[p_key].encode('utf-8')).hexdigest()
        if p_value_hash != t_hash:
            logger_interface.error('hash is not valid for %s value', p_key)
            result = False
            break

    return result


def main():
    raw_path = {
        'erista': 'nx',
        'mariko': 'a'
    }

    if not check_key_file(args.prod_keys):
        logger_interface.error('Keys file is not valid!')
        sys.exit()
    logger_interface.info('Extracting ROMFS BootImagePackage from provided firmware files.')
    os.system(f'{modules.hactoolnet} --keyset {args.prod_keys} --intype switchfs --raw {args.firmware} --title 0100000000000819 --romfsdir 0100000000000819/romfs/')
    logger_interface.info('Extracting Package1 from ROMFS')
    os.system(f'{modules.hactoolnet} --keyset {args.prod_keys} --intype pk11 --outdir 0100000000000819/romfs/{raw_path[args.rev_name]}/pkg1 --raw 0100000000000819/romfs/{raw_path[args.rev_name]}/package1')

    with open('0100000000000819/romfs/a/pkg1/Decrypted.bin', 'rb') as decrypted_bin:
        secmon_data = decrypted_bin.read()
        result = re.search(b'\x4F\x59\x41\x53\x55\x4D\x49', secmon_data)
        if args.rev_name == 'erista':
            byte_alignment = decrypted_bin.seek(result.end() + 0x32)
        elif args.rev_name == 'mariko':
            byte_alignment = decrypted_bin.seek(result.end() + 0x22)
        master_kek_source_key = decrypted_bin.read(0x10).hex().upper()
        if args.rev_name == 'erista':
            byte_alignment = decrypted_bin.seek(0x1e)
        elif args.rev_name == 'mariko':
            byte_alignment = decrypted_bin.seek(0x150)
        revision = decrypted_bin.read(0x01).hex().upper()
        incremented_revision = int(revision) - 0x1
        if args.rev_name == 'erista':
            master_kek_source = f'master_kek_source_{incremented_revision} = {master_kek_source_key}'
        elif args.rev_name == 'mariko':
            master_kek_source = f'mariko_master_kek_source_{incremented_revision} = {master_kek_source_key}'

    os.system(f'{modules.hactoolnet} --keyset "temp.keys" --intype keygen --outdir new-keys/')
    logger_interface.info('Keygen completed!')

    shutil.rmtree('0100000000000819')


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--firmware", help="firmware folder", dest="firmware", type=str, default="./firmware")
    argParser.add_argument("-k", "--keys", help="keyfile to use", dest="prod_keys", type=str, default="./prod.keys")
    argParser.add_argument("-r", "--revision", help="Revision name", dest="rev_name", choices=['mariko', 'erista'], required=True)
    args = argParser.parse_args()

    logger_interface = logging.getLogger('keygen')
    modules.logging_configuration(logger_interface)
    sys.exit(main())
