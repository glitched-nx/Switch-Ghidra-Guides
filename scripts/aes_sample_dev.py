import aes128
import argparse
from base64 import b64decode

argParser = argparse.ArgumentParser()
argParser.add_argument("-k", "--keys", help="Where you want the keys to be saved")
args = argParser.parse_args()
prod_keys = "%s" % args.keys


if prod_keys == "None":
    keys = "dev.keys"
else: 
    keys = prod_keys

def decrypt(key, decryption_key):
	crypto = aes128.AESECB(decryption_key)
	return crypto.decrypt(key)

def generateKek(src, masterKey, kek_seed, key_seed):
	kek = []
	src_kek = []

	crypto = aes128.AESECB(masterKey)
	kek = crypto.decrypt(kek_seed)

	crypto = aes128.AESECB(kek)
	src_kek = crypto.decrypt(src)

	if key_seed is not None:
		crypto = aes128.AESECB(src_kek)
		return crypto.decrypt(key_seed)
	else:
		return src_kek

mariko_kek = bytes.fromhex(b64decode('NDEzMEI4Qjg0MkREN0NEMkVBOEZENTBEM0Q0OEI3N0M=').decode('utf-8'))

# various sources
master_key_source = bytes.fromhex("D8A2410AC6C59001C61D6A267C513F3C") # https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L44
package2_key_source = bytes.fromhex("FB8B6A9C7900C849EFD24D854D30A0C7") # https://github.com/Atmosphere-NX/Atmosphere/blob/9f8d17b9e6079eb421e194b81bed8a3de357c10d/exosphere/program/source/boot/secmon_boot_key_data.s#L76
key_area_key_application_source = bytes.fromhex("7F59971E629F36A13098066F2144C30D") # https://github.com/Atmosphere-NX/Atmosphere/blob/master/libraries/libstratosphere/source/fssrv/fssrv_nca_crypto_configuration.cpp#L110
key_area_key_ocean_source = bytes.fromhex("327D36085AD1758DAB4E6FBAA555D882") # https://github.com/Atmosphere-NX/Atmosphere/blob/master/libraries/libstratosphere/source/fssrv/fssrv_nca_crypto_configuration.cpp#L113
key_area_key_system_source = bytes.fromhex("8745F1BBA6BE79647D048BA67B5FDA4A") # https://github.com/Atmosphere-NX/Atmosphere/blob/master/libraries/libstratosphere/source/fssrv/fssrv_nca_crypto_configuration.cpp#L116
aes_kek_generation_source = bytes.fromhex("4D870986C45D20722FBA1053DA92E8A9") # https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L224
aes_key_generation_source = bytes.fromhex("89615EE05C31B6805FE58F3DA24F7AA8") # https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L228
titlekek_source = bytes.fromhex("1EDC7B3B60E6B4D878B81715985E629B") # https://github.com/Atmosphere-NX/Atmosphere/blob/master/exosphere/program/source/smc/secmon_smc_aes.cpp#L162

# master key dev sources https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L138-L157
#master_key_source_dev_00 = bytes.fromhex("4622B4519A7EA77F62A11F8FC53ADBFE") # Zeroes encrypted with Master Key 00. */
master_key_source_dev_01 = bytes.fromhex("3933F931BAE4A7212CDDB7D8B44E3723") # Master key 00 encrypted with Master key 01. */
master_key_source_dev_02 = bytes.fromhex("9729B03243148CA685E95A949939AC5D") # Master key 01 encrypted with Master key 02. */
master_key_source_dev_03 = bytes.fromhex("2CCA9C311E07B002970AD803A2763FA3") # Master key 02 encrypted with Master key 03. */
master_key_source_dev_04 = bytes.fromhex("9B847614729452CB54929BC48C5B0FBA") # Master key 03 encrypted with Master key 04. */
master_key_source_dev_05 = bytes.fromhex("78D5F1203D16E9303227346FCFE027DC") # Master key 04 encrypted with Master key 05. */
master_key_source_dev_06 = bytes.fromhex("6FD2841D05EC40945F18B38109988D4E") # Master key 05 encrypted with Master key 06. */
master_key_source_dev_07 = bytes.fromhex("37AFAB357909D94829D2DBA5A5F53019") # Master key 06 encrypted with Master key 07. */
master_key_source_dev_08 = bytes.fromhex("ECE1468937FDD2158C3F2482EF496804") # Master key 07 encrypted with Master key 08. */
master_key_source_dev_09 = bytes.fromhex("433DC53BEF9102216154638A35E7CAEE") # Master key 08 encrypted with Master key 09. */
master_key_source_dev_0a = bytes.fromhex("6C2ECDB3346177F5F9B1DD6198193ED4") # Master key 09 encrypted with Master key 0A. */
master_key_source_dev_0b = bytes.fromhex("21886B109E83D652AB08DB6D39FF1C9C") # Master key 0A encrypted with Master key 0B. */
master_key_source_dev_0c = bytes.fromhex("8ACEC47FBE086188D3736451E2B65315") # Master key 0B encrypted with Master key 0C. */
master_key_source_dev_0d = bytes.fromhex("08E0F4BEAA6E5AC3A6BCFEB9E2A32412") # Master key 0C encrypted with Master key 0D. */
master_key_source_dev_0e = bytes.fromhex("D68098C0FAC713CB93D20B824CA17B8D") # Master key 0D encrypted with Master key 0E. */
master_key_source_dev_0f = bytes.fromhex("786619BD86E7C1099B6F92B2587DCF26") # Master key 0E encrypted with Master key 0F. */
master_key_source_dev_10 = bytes.fromhex("391E7EF87E73EA6FAF003AB4AAB8B759") # Master key 0F encrypted with Master key 10. */
master_key_source_dev_11 = bytes.fromhex("0C75391553EA8111A3E0DC3D0E76C6B8") # Master key 10 encrypted with Master key 11. */
master_key_source_dev_12 = bytes.fromhex("9064F9082988D4DC73A4A1139E5985A0") # Master key 11 encrypted with Master key 12. */

# mariko master_kek_sources
mariko_master_kek_source_dev = bytes.fromhex("657B11460EC2225DB9F1F500F93E1F70") # https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L31
key_revision = "12"

with open(keys, 'w') as manual_crypto:	
	manual_crypto.write(f'master_key_source = ' + f'{master_key_source.hex().upper()}\n')
	manual_crypto.write(f'package2_key_source= ' + f'{package2_key_source.hex().upper()}\n')
	manual_crypto.write(f'key_area_key_system_source = ' + f'{key_area_key_system_source.hex().upper()}\n')
	manual_crypto.write(f'key_area_key_application_source = ' + f'{key_area_key_application_source.hex().upper()}\n')
	manual_crypto.write(f'key_area_key_ocean_source = ' + f'{key_area_key_ocean_source.hex().upper()}\n')
	manual_crypto.write(f'aes_kek_generation_sourcee = ' + f'{aes_kek_generation_source.hex().upper()}\n')
	manual_crypto.write(f'aes_key_generation_source = ' + f'{aes_key_generation_source.hex().upper()}\n')
	manual_crypto.write(f'package2_key_source = ' + f'{package2_key_source.hex().upper()}\n')
	manual_crypto.write(f'titlekek_source = ' + f'{titlekek_source.hex().upper()}\n')

	# Write mariko_master_kek_sources
	keys = f'mariko_master_kek_source_dev_{key_revision} = '  + mariko_master_kek_source_dev.hex().upper()
	manual_crypto.write(f'{keys}\n')
	print(keys)

	# generate master_kek_%% from all provided mariko_master_kek_sources
	master_kek = decrypt(mariko_master_kek_source_dev, mariko_kek)
	keys = f'master_kek_dev_{key_revision} = '  + master_kek.hex().upper() 
	manual_crypto.write(f'{keys}\n')
	print(keys)

	# generate master_key_%% from all provided master_kek_%% using master_key_source
	master_key_dev_12 = decrypt(master_key_source, master_kek)
	# generate master_key_00 to master_key_04 with master_key_source_%%
	master_key_dev_11 = decrypt(master_key_source_dev_12, master_key_dev_12)
	master_key_dev_10 = decrypt(master_key_source_dev_11, master_key_dev_11)
	master_key_dev_0f = decrypt(master_key_source_dev_10, master_key_dev_10)
	master_key_dev_0e = decrypt(master_key_source_dev_0f, master_key_dev_0f)
	master_key_dev_0d = decrypt(master_key_source_dev_0e, master_key_dev_0e)
	master_key_dev_0c = decrypt(master_key_source_dev_0d, master_key_dev_0d)
	master_key_dev_0b = decrypt(master_key_source_dev_0c, master_key_dev_0c)
	master_key_dev_0a = decrypt(master_key_source_dev_0b, master_key_dev_0b)
	master_key_dev_09 = decrypt(master_key_source_dev_0a, master_key_dev_0a)
	master_key_dev_08 = decrypt(master_key_source_dev_09, master_key_dev_09)
	master_key_dev_07 = decrypt(master_key_source_dev_08, master_key_dev_08)
	master_key_dev_06 = decrypt(master_key_source_dev_07, master_key_dev_07)
	master_key_dev_05 = decrypt(master_key_source_dev_06, master_key_dev_06)
	master_key_dev_04 = decrypt(master_key_source_dev_05, master_key_dev_05)
	master_key_dev_03 = decrypt(master_key_source_dev_04, master_key_dev_04)
	master_key_dev_02 = decrypt(master_key_source_dev_03, master_key_dev_03)
	master_key_dev_01 = decrypt(master_key_source_dev_02, master_key_dev_02)
	master_key_dev_00 = decrypt(master_key_source_dev_01, master_key_dev_01)

	master_keys = [ 
		master_key_dev_00, master_key_dev_01, master_key_dev_02,
		master_key_dev_03, master_key_dev_04, master_key_dev_05,
		master_key_dev_06, master_key_dev_07, master_key_dev_08,
		master_key_dev_09, master_key_dev_0a, master_key_dev_0b,
		master_key_dev_0c, master_key_dev_0d, master_key_dev_0e,
		master_key_dev_0f, master_key_dev_10, master_key_dev_11,
		master_key_dev_12
	]

	count = -0x1
	for i in master_keys:
		count = count + 0x1
		keys = f'master_key_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')
		print(keys)

	# generate package2_key_%% from all provided master_key_%% using package2_key_source
	package2_key = [decrypt(package2_key_source, i) for i in master_keys]
	count = -0x1
	for i in package2_key:
		count = count + 0x1
		keys = f'package2_key_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')
		print(keys)

	# generate title_kek_%% from all provided master_key_%% using titlekek_source
	titlekek = [decrypt(titlekek_source, i) for i in master_keys]
	count = -0x1
	for i in titlekek:
		count = count + 0x1
		keys = f'titlekek_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')
		print(keys)

	# generate key_area_key_application_%% from all provided master_key_%% using key_area_key_application_source
	key_area_key_application = [generateKek(key_area_key_application_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
	count = -0x1
	for i in key_area_key_application:
		count = count +0x1
		keys = f'key_area_key_application_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')
		print(keys)

	# generate key_area_key_ocean_%% from all provided master_key_%% using key_area_key_ocean_source
	key_area_key_ocean = [generateKek(key_area_key_ocean_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
	count = -0x1
	for i in key_area_key_ocean:
		count = count +0x1
		keys = f'key_area_key_ocean_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')
		print(keys)

	# generate key_area_key_system_%% from all provided master_key_%% using key_area_key_system_source
	key_area_key_system = [generateKek(key_area_key_system_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
	count = -0x1
	for i in key_area_key_system:
		count = count +0x1
		keys = f'key_area_key_system_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')
		print(keys)