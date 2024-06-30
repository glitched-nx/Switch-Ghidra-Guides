import os
import re
import shutil
import subprocess
import sys
import requests
import logging
import zipfile
import hashlib

import modules

_C_LOADERKIP_FILE = "./compressed_loader.kip1"
_D_LOADERKIP_FILE = "./decompressed_loader.kip1"

def main():
    release_info = requests.get('https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases/latest').json()
    atmosphere_asset = list(filter(lambda x: 'atmosphere' in x['name'], release_info['assets']))[0]

    with requests.get(atmosphere_asset['browser_download_url'], stream=True) as r:
        r.raise_for_status()
        with open(atmosphere_asset['name'], 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    logger_interface.info('Atmosphere download is OK')

    atmosphere_archive_name = atmosphere_asset['name']
    atmosphere_version = re.search('[0-9.]{5}', atmosphere_archive_name).group()
    atmosphere_hash = re.search('[0-9A-Fa-f]{6,9}', atmosphere_archive_name).group()
    logger_interface.info('Atifact name: %s', atmosphere_archive_name)
    logger_interface.info('Atmosphere version: %s', atmosphere_version)
    logger_interface.info('Atmosphere hash: %s', atmosphere_hash)

    with zipfile.ZipFile('./'+atmosphere_archive_name, 'r') as amszip:
        logger_interface.info('Open archive OK')
        with amszip.open('atmosphere/package3') as package3:
            logger_interface.info('Open package3 OK')
            package_data = package3.read()

    locate_loader = package_data.find(b'Loader')
    loader_size_start = locate_loader - 0xC
    loader_size_end = locate_loader - 0x9
    size = int.from_bytes(package_data[loader_size_start:loader_size_end], 'little')
    loader_offset_start = locate_loader - 0x10
    loader_offset_end = locate_loader - 0xD
    loader_start = int.from_bytes(package_data[loader_offset_start:loader_offset_end], 'little')
    loader_end = loader_start + size
    logger_interface.info('\nloader locate: %s, %s\nloader size: %s\nloader offset: %s, %s',
                          locate_loader, hex(locate_loader),
                          size, loader_start, hex(loader_start))
    loader_kip = package_data[loader_start:loader_end]
    if not re.compile(b'\x4B\x49\x50\x31\x4C\x6F\x61\x64\x65\x72').search(loader_kip):
        logger_interface.error('KIP1Loader magic not found! - Script needs to be fixed, loader_kip is not correct!')
        sys.exit(0)

    with open(_C_LOADERKIP_FILE, 'wb') as compressed_loader_file:
        compressed_loader_file.write(loader_kip)
    os.system(f'hactoolnet -t kip1 {_C_LOADERKIP_FILE} --uncompressed {_D_LOADERKIP_FILE}')
    logger_interface.info('Uncompressing loader OK')

    with open(_D_LOADERKIP_FILE, 'rb') as decompressed_loader_kip:
        loader_data = decompressed_loader_kip.read()
        result = re.search(b'\x00\x94\x01\xC0\xBE\x12\x1F\x00', loader_data)
        if not result:
            logger_interface.error('Instructions for the patch were not found')
            sys.exit(0)
        hash = hashlib.sha256(loader_kip).hexdigest().upper()

        offset_hex_0x = f'0x{result.end()-0x100:04X}'
        length_hex_0x = f'0x{1:X}'
        decompressed_loader_kip.seek(result.end())
        src_data_hex = decompressed_loader_kip.read(0x1).hex().upper()
        dst_data_hex='00'
        logger_interface.info('\nHEKATE LOADER HASH: %s\nHEKATE LOADER OFFSET: %s',
                              hash[:16], offset_hex_0x)
        with open('./hekate_patches/loader_patches.ini', 'a') as loader_hekate:
            loader_hekate.write('\n')
            loader_hekate.write(f'#Loader Atmosphere-{atmosphere_version}-{atmosphere_hash}\n')
            loader_hekate.write(f'[Loader:{hash[:16]}]\n')
            loader_hekate.write(f'.nosigchk=0:{offset_hex_0x}:{length_hex_0x}:{src_data_hex},{dst_data_hex}\n')
        logger_interface.info('loader_patches.ini OK')


        ips_header = b'PATCH'.hex()
        ips_offset = f'{result.end():06X}'
        ips_data_size = f'{1:04X}'
        ips_data = '00'
        ips_footer = b'EOF'.hex()
        logger_interface.info('\nIPS LOADER HASH: %s\nIPS LOADER OFFSET: %s',
                              hash, ips_offset)
        with open('./patches/atmosphere/kip_patches/loader_patches/%s.ips' % hash, 'wb') as ips_file:
            ips_file.write(bytes.fromhex(ips_header + ips_offset + ips_data_size + ips_data + ips_footer))
        logger_interface.info('%s.ips OK', hash)

    with open('./patches/bootloader/patches.ini', 'wb') as outfile:
        for filename in ['./hekate_patches/header.ini', './hekate_patches/fs_patches.ini', './hekate_patches/loader_patches.ini']:
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outfile)
    shutil.make_archive('patches', 'zip', 'patches')
    logger_interface.info('SigPatches OK')

    os.remove(_C_LOADERKIP_FILE)
    os.remove(_D_LOADERKIP_FILE)
    os.remove('./'+atmosphere_archive_name)


if __name__ == "__main__":
    logger_interface = logging.getLogger('loader')
    modules.logging_configuration(logger_interface)
    sys.exit(main())
