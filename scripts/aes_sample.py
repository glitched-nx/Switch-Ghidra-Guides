import aes128

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

mariko_kek = bytes.fromhex("FILL-IN-MARIKO_KEK") # substitute with mariko_kek, sha256 string: 53be3a736bdb7ff26868ce73e9e5b8ad3b652039be75dfce89a91d11a4c69866

# various sources
master_key_source = bytes.fromhex("D8A2410AC6C59001C61D6A267C513F3C") # persistent from 1.0.0
package2_key_source = bytes.fromhex("FB8B6A9C7900C849EFD24D854D30A0C7") # persistent from 1.0.0
key_area_key_application_source = bytes.fromhex("7F59971E629F36A13098066F2144C30D") # persistent from 1.0.0
key_area_key_ocean_source = bytes.fromhex("327D36085AD1758DAB4E6FBAA555D882") # persistent from 1.0.0
key_area_key_system_source = bytes.fromhex("8745F1BBA6BE79647D048BA67B5FDA4A") # persistent from 1.0.0
aes_kek_generation_source = bytes.fromhex("4D870986C45D20722FBA1053DA92E8A9") # persistent from 1.0.0
aes_key_generation_source = bytes.fromhex("89615EE05C31B6805FE58F3DA24F7AA8") # persistent from 1.0.0
package2_key_source = bytes.fromhex("FB8B6A9C7900C849EFD24D854D30A0C7") # persistent from 1.0.0
titlekek_source= bytes.fromhex("1EDC7B3B60E6B4D878B81715985E629B") # persistent from 1.0.0

# mariko master_kek_sources
mariko_master_kek_source_05 = bytes.fromhex("77605AD2EE6EF83C3F72E2599DAC5E56")
mariko_master_kek_source_06 = bytes.fromhex("1E80B8173EC060AA11BE1A4AA66FE4AE")
mariko_master_kek_source_07 = bytes.fromhex("940867BD0A00388411D31ADBDD8DF18A")
mariko_master_kek_source_08 = bytes.fromhex("5C24E3B8B4F700C23CFD0ACE13C3DC23")
mariko_master_kek_source_09 = bytes.fromhex("8669F00987C805AEB57B4874DE62A613")
mariko_master_kek_source_0a = bytes.fromhex("0E440CEDB436C03FAA1DAEBF62B10982")
mariko_master_kek_source_0b = bytes.fromhex("E541ACECD1A7D1ABED0377F127CAF8F1")
mariko_master_kek_source_0c = bytes.fromhex("52719BDFA78B61D8D58511E48E4F74C6")
mariko_master_kek_source_0d = bytes.fromhex("D268C6539D94F9A8A5A8A7C88F534B7A")
mariko_master_kek_source_0e = bytes.fromhex("EC61BC821E0F5AC32B643F9DD619222D")
mariko_master_kek_source_0f = bytes.fromhex("A5EC16391A3016082ECF096F5E7CEEA9")
mariko_master_kek_source_10 = bytes.fromhex("8DEE9E11363A9B0A6AC7BBE9D103F780")
mariko_master_kek_source_11 = bytes.fromhex("4F413C3BFB6A012A689F83E953BD16D2")
mariko_master_kek_source_12 = bytes.fromhex("31BE25FBDBB4EE495C7705C2369F3480")

mariko_master_kek_sources = [
	mariko_master_kek_source_05, mariko_master_kek_source_06, mariko_master_kek_source_07,
	mariko_master_kek_source_08, mariko_master_kek_source_09, mariko_master_kek_source_0a,
	mariko_master_kek_source_0b, mariko_master_kek_source_0c, mariko_master_kek_source_0d,
	mariko_master_kek_source_0e, mariko_master_kek_source_0f, mariko_master_kek_source_10,
	mariko_master_kek_source_11, mariko_master_kek_source_12
]

# generate master_kek_%% from all provided mariko_master_kek_sources
master_keks = [decrypt(i, mariko_kek) for i in mariko_master_kek_sources]
count = 0x4
for i in master_keks:
	count = count + 0x1
	print(f'master_kek_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper()))

# generate master_key_%% from all provided master_kek_%% using master_key_source
master_keys = [decrypt(master_key_source, i) for i in master_keks]
count = 0x4
for i in master_keys:
	count = count + 0x1
	print(f'master_key_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper()))

# generate package2_key_%% from all provided master_key_%% using package2_key_source
package2_key = [decrypt(package2_key_source, i) for i in master_keys]
count = 0x4
for i in package2_key:
	count = count + 0x1
	print(f'package2_key_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper()))

# generate title_kek_%% from all provided master_key_%% using titlekek_source
titlekek = [decrypt(titlekek_source, i) for i in master_keys]
count = 0x4
for i in titlekek:
	count = count + 0x1
	print(f'titlekek_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper()))

# generate key_area_key_application_%% from all provided master_key_%% using key_area_key_application_source
key_area_key_application = [generateKek(key_area_key_application_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
count = 0x4
for i in key_area_key_application:
	count = count +0x1
	print(f'key_area_key_application_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper()))

# generate key_area_key_ocean_%% from all provided master_key_%% using key_area_key_ocean_source
key_area_key_ocean = [generateKek(key_area_key_ocean_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
count = 0x4
for i in key_area_key_ocean:
	count = count +0x1
	print(f'key_area_key_ocean_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper()))

# generate key_area_key_system_%% from all provided master_key_%% using key_area_key_system_source
key_area_key_system = [generateKek(key_area_key_system_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
count = 0x4
for i in key_area_key_system:
	count = count +0x1
	print(f'key_area_key_system_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper()))