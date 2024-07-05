import logging
import platform
import hashlib
import shutil


IPS_HEADER = b'PATCH'.hex()
IPS_FOOTER = b'EOF'.hex()
IPS32_HEADER  = b'IPS32'.hex()
IPS32_FOOTER  = b'EEOF'.hex()
ES_PATCH_DIR = 'patches/atmosphere/exefs_patches/es_patches/'
NIFM_CTEST_PATCH_DIR = 'patches/atmosphere/exefs_patches/nifm_ctest/'
NIM_PATCH_DIR = 'patches/atmosphere/exefs_patches/ams_blanker_fix/'

HEKATE_FS_FILE = 'hekate_patches/fs_patches.ini'
HEKATE_LOADER_FILE = 'hekate_patches/loader_patches.ini'
HEKATE_HEADER_FILE = 'hekate_patches/header.ini'
HEKATE_PATCH_FILE = 'patches/bootloader/patches.ini'


def logging_configuration(logger):
    sh_formatter = logging.Formatter(fmt='%(asctime)s %(process)d %(name)s %(levelname)s %(funcName)s %(message)s',
                                     datefmt='%d-%b-%y %H:%M:%S')
    sh = logging.StreamHandler()
    sh.setLevel(level=logging.INFO)
    sh.setFormatter(sh_formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)


def get_build_id(file_object):
    file_object.seek(0x40)
    return(file_object.read(0x14).hex().upper())


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


def pack_hekate_patch():
    with open(HEKATE_PATCH_FILE, 'wb') as outfile:
        for filename in [HEKATE_HEADER_FILE, HEKATE_FS_FILE, HEKATE_LOADER_FILE]:
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outfile)



if platform.system() == "Windows":
    hactoolnet = "./tools/hactoolnet-windows.exe"
    hactool = "./tools/hactool-windows.exe"
elif platform.system() == "Linux":
    hactoolnet = "./tools/hactoolnet-linux"
    hactool = "./tools/hactool-linux"
elif platform.system() == "MacOS":
    hactoolnet = "./tools/hactoolnet-macos"
    hactool = "./tools/hactool-macos"
else:
    logger_interface.warning(f"Unknown Platform: {platform.system()}, proide your own hactoolnet")
    hactoolnet = "hactoolnet"
    hactool = "hactool"
