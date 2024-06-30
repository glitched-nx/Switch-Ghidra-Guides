import re
import subprocess
import os
import sys
import hashlib
import logging
import argparse
import shutil

_HACTOOLNET = 'hactoolnet'

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
            key, value = line.strip().split('=')
            result[key] = value

    for p_key, p_value in ns_keys.items():
        if 'package1_key_' not in p_key:
            logger_interface.error('package1_key_<> is missing in keys file, we cannot proceed with keygen as package1 cannot be opened for the purpose of obtaining master_kek_source. Exiting.')
            break
        if 'tsec_root_key_' not in check_key:
            logger_interface.error('tsec_root_key_<> is missing in keys file, we cannot derive a new master_kek from the new master_kek_source, keygen will not yield new keys. Exiting.')
            break
    else:
        result = False

    for p_key, p_value_hash in valid_hashes.items():
        t_hash = hashlib.md5(ns_keys[p_key].encode()).hexdigest()
        if p_value_hash != t_hash:
            logger_interface.error('hash is not valid for %s value', p_key)
            break
    else:
        result = False

    return result


def main():
    if not check_key_file():
        shutil.rmtree('0100000000000819')

    logger_interface.info('Extracting ROMFS BootImagePackage from provided firmware files.')
    subprocess.run(f'{_HACTOOLNET} --keyset {args.prod_keys} -t switchfs {args.firmware} --title 0100000000000819 --romfsdir 0100000000000819/romfs/', stdout=subprocess.DEVNULL)
    logger_interface.info('Extracting Package1 from ROMFS')
    subprocess.run(f'{_HACTOOLNET} --keyset {args.prod_keys} -t pk11 0100000000000819/romfs/nx/package1 --outdir 0100000000000819/romfs/nx/pkg1', stdout=subprocess.DEVNULL)
    logger_interface.info('Checking if a new master_kek_source is found in Package1.')

    with open('0100000000000819/romfs/nx/pkg1/Decrypted.bin', 'rb') as decrypted_bin:
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

    os.rename(args.prod_keys, 'temp.keys')
    with open('temp.keys', 'a') as temp_keys:
        temp_keys.write(f'\n')
        temp_keys.write(master_kek_source+'\n')

    with open(args.prod_keys, 'w') as new_prod_keys:
        if args.dev_env:
            subprocess.run(f'{_HACTOOLNET} --dev --keyset temp.keys -t keygen', stdout=new_prod_keys)
            print(f'You just generated a dev keyset, which are only useful for developer ncas written with nnsdk keyset, and they have been output to {prod_keys}')
        elif not args.dev_env:
            subprocess.run(f'{_HACTOOLNET} --keyset "temp.keys" -t keygen', stdout=new_prod_keys)
        logger_interface.info('# Keygen completed and output to %s, exiting.', args.prod_keys)

    os.remove('temp.keys')
    shutil.rmtree('0100000000000819')


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--firmware", help="firmware folder", dest="firmware", type=str, default="./firmware")
    argParser.add_argument("-k", "--keys", help="keyfile to use", dest="prod_keys", type=str, default="./prod.keys")
    argParser.add_argument("-d", "--dev", help="Initiates dev keyset keygen", dest="dev_env", type=bool, action='store_true')
    argParser.add_argument("-r", "--revision", help="Revision name", dest="rev_name", type=str, choice=['mariko', 'erista'], required=True)
    args = argParser.parse_args()

    logger_interface = logging.getLogger('keygen')
    modules.logging_configuration(logger_interface)
    sys.exit(main())
