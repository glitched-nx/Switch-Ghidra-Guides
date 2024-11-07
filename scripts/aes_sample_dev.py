import aes128
import argparse

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


# various sources:
keyblob_mac_key_source              = bytes([0x59, 0xC7, 0xFB, 0x6F, 0xBE, 0x9B, 0xBE, 0x87, 0x65, 0x6B, 0x15, 0xC0, 0x53, 0x73, 0x36, 0xA5])
per_console_key_source              = bytes([0x4F, 0x02, 0x5F, 0x0E, 0xB6, 0x6D, 0x11, 0x0E, 0xDC, 0x32, 0x7D, 0x41, 0x86, 0xC2, 0xF4, 0x78])
retail_specific_aes_key_source      = bytes([0xE2, 0xD6, 0xB8, 0x7A, 0x11, 0x9C, 0xB8, 0x80, 0xE8, 0x22, 0x88, 0x8A, 0x46, 0xFB, 0xA1, 0x95])
header_kek_source                   = bytes([0x1F, 0x12, 0x91, 0x3A, 0x4A, 0xCB, 0xF0, 0x0D, 0x4C, 0xDE, 0x3A, 0xF6, 0xD5, 0x23, 0x88, 0x2A])
header_key_source                   = bytes([0x5A, 0x3E, 0xD8, 0x4F, 0xDE, 0xC0, 0xD8, 0x26, 0x31, 0xF7, 0xE2, 0x5D, 0x19, 0x7B, 0xF5, 0xD0, 0x1C, 0x9B, 0x7B, 0xFA, 0xF6, 0x28, 0x18, 0x3D, 0x71, 0xF6, 0x4D, 0x73, 0xF1, 0x50, 0xB9, 0xD2])
save_mac_kek_source                 = bytes([0xD8, 0x9C, 0x23, 0x6E, 0xC9, 0x12, 0x4E, 0x43, 0xC8, 0x2B, 0x03, 0x87, 0x43, 0xF9, 0xCF, 0x1B])
save_mac_key_source_00              = bytes([0xE4, 0xCD, 0x3D, 0x4A, 0xD5, 0x0F, 0x74, 0x28, 0x45, 0xA4, 0x87, 0xE5, 0xA0, 0x63, 0xEA, 0x1F])
save_mac_key_source_01              = bytes([0xEC, 0x24, 0x98, 0x95, 0x65, 0x6A, 0xDF, 0x4A, 0xA0, 0x66, 0xB9, 0x88, 0x0A, 0xC8, 0x2C, 0x4C])
save_mac_sd_card_kek_source         = bytes([0x04, 0x89, 0xEF, 0x5D, 0x32, 0x6E, 0x1A, 0x59, 0xC4, 0xB7, 0xAB, 0x8C, 0x36, 0x7A, 0xAB, 0x17])
save_mac_sd_card_key_source         = bytes([0x6F, 0x64, 0x59, 0x47, 0xC5, 0x61, 0x46, 0xF9, 0xFF, 0xA0, 0x45, 0xD5, 0x95, 0x33, 0x29, 0x18])
sd_card_kek_source                  = bytes([0x88, 0x35, 0x8D, 0x9C, 0x62, 0x9B, 0xA1, 0xA0, 0x01, 0x47, 0xDB, 0xE0, 0x62, 0x1B, 0x54, 0x32])
keyblob_mac_key_source              = bytes([0x59, 0xC7, 0xFB, 0x6F, 0xBE, 0x9B, 0xBE, 0x87, 0x65, 0x6B, 0x15, 0xC0, 0x53, 0x73, 0x36, 0xA5])
bis_kek_source                      = bytes([0x34, 0xC1, 0xA0, 0xC4, 0x82, 0x58, 0xF8, 0xB4, 0xFA, 0x9E, 0x5E, 0x6A, 0xDA, 0xFC, 0x7E, 0x4F])
tsec_auth_signature_00              = bytes([0xA7, 0x7B, 0x86, 0x58, 0x6A, 0xE1, 0xB0, 0x3D, 0x4F, 0xFB, 0xA3, 0xAD, 0xA8, 0xF8, 0xDE, 0x32])
tsec_auth_signature_01              = bytes([0xA3, 0xFF, 0xB0, 0xF6, 0xBC, 0x49, 0xA0, 0x6D, 0xF2, 0xFC, 0x79, 0x16, 0x97, 0xD8, 0x1D, 0x32])
tsec_auth_signature_02              = bytes([0x0B, 0x55, 0xCC, 0x08, 0x20, 0xE6, 0x30, 0x7F, 0xD0, 0x87, 0x47, 0x9E, 0xAA, 0x2E, 0x7F, 0x98])
tsec_root_key_02                    = bytes([0xCA, 0x99, 0x73, 0xE3, 0x82, 0x75, 0xB8, 0x81, 0x46, 0x25, 0x16, 0xAC, 0x18, 0xCB, 0x1D, 0xF2])
header_key                          = bytes([0xCB, 0x9A, 0x93, 0x9F, 0x82, 0x72, 0x54, 0x4A, 0x74, 0x5D, 0x28, 0x46, 0x9D, 0xCC, 0x38, 0x12, 0x06, 0x31, 0x27, 0x06, 0xAE, 0x62, 0x56, 0x8C, 0x5B, 0x7E, 0xE6, 0x9F, 0x7E, 0x01, 0x02, 0x24])
keyblob_mac_key_source              = bytes([0x59, 0xC7, 0xFB, 0x6F, 0xBE, 0x9B, 0xBE, 0x87, 0x65, 0x6B, 0x15, 0xC0, 0x53, 0x73, 0x36, 0xA5])
master_key_source                   = bytes([0xD8, 0xA2, 0x41, 0x0A, 0xC6, 0xC5, 0x90, 0x01, 0xC6, 0x1D, 0x6A, 0x26, 0x7C, 0x51, 0x3F, 0x3C]) # https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L44
package2_key_source                 = bytes([0xFB, 0x8B, 0x6A, 0x9C, 0x79, 0x00, 0xC8, 0x49, 0xEF, 0xD2, 0x4D, 0x85, 0x4D, 0x30, 0xA0, 0xC7]) # https://github.com/Atmosphere-NX/Atmosphere/blob/9f8d17b9e6079eb421e194b81bed8a3de357c10d/exosphere/program/source/boot/secmon_boot_key_data.s#L76
key_area_key_application_source     = bytes([0x7F, 0x59, 0x97, 0x1E, 0x62, 0x9F, 0x36, 0xA1, 0x30, 0x98, 0x06, 0x6F, 0x21, 0x44, 0xC3, 0x0D]) # https://github.com/Atmosphere-NX/Atmosphere/blob/master/libraries/libstratosphere/source/fssrv/fssrv_nca_crypto_configuration.cpp#L110
key_area_key_ocean_source           = bytes([0x32, 0x7D, 0x36, 0x08, 0x5A, 0xD1, 0x75, 0x8D, 0xAB, 0x4E, 0x6F, 0xBA, 0xA5, 0x55, 0xD8, 0x82]) # https://github.com/Atmosphere-NX/Atmosphere/blob/master/libraries/libstratosphere/source/fssrv/fssrv_nca_crypto_configuration.cpp#L113
key_area_key_system_source          = bytes([0x87, 0x45, 0xF1, 0xBB, 0xA6, 0xBE, 0x79, 0x64, 0x7D, 0x04, 0x8B, 0xA6, 0x7B, 0x5F, 0xDA, 0x4A]) # https://github.com/Atmosphere-NX/Atmosphere/blob/master/libraries/libstratosphere/source/fssrv/fssrv_nca_crypto_configuration.cpp#L116
aes_kek_generation_source           = bytes([0x4D, 0x87, 0x09, 0x86, 0xC4, 0x5D, 0x20, 0x72, 0x2F, 0xBA, 0x10, 0x53, 0xDA, 0x92, 0xE8, 0xA9]) # https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L224
aes_key_generation_source           = bytes([0x89, 0x61, 0x5E, 0xE0, 0x5C, 0x31, 0xB6, 0x80, 0x5F, 0xE5, 0x8F, 0x3D, 0xA2, 0x4F, 0x7A, 0xA8]) # https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L228
titlekek_source                     = bytes([0x1E, 0xDC, 0x7B, 0x3B, 0x60, 0xE6, 0xB4, 0xD8, 0x78, 0xB8, 0x17, 0x15, 0x98, 0x5E, 0x62, 0x9B]) # https://github.com/Atmosphere-NX/Atmosphere/blob/master/exosphere/program/source/smc/secmon_smc_aes.cpp#L162


# keyblob_key_sources
Keyblob_Key_Sources = [
	bytes([0xDF, 0x20, 0x6F, 0x59, 0x44, 0x54, 0xEF, 0xDC, 0x70, 0x74, 0x48, 0x3B, 0x0D, 0xED, 0x9F, 0xD3]),
	bytes([0x0C, 0x25, 0x61, 0x5D, 0x68, 0x4C, 0xEB, 0x42, 0x1C, 0x23, 0x79, 0xEA, 0x82, 0x25, 0x12, 0xAC]),
	bytes([0x33, 0x76, 0x85, 0xEE, 0x88, 0x4A, 0xAE, 0x0A, 0xC2, 0x8A, 0xFD, 0x7D, 0x63, 0xC0, 0x43, 0x3B]),
	bytes([0x2D, 0x1F, 0x48, 0x80, 0xED, 0xEC, 0xED, 0x3E, 0x3C, 0xF2, 0x48, 0xB5, 0x65, 0x7D, 0xF7, 0xBE]),
	bytes([0xBB, 0x5A, 0x01, 0xF9, 0x88, 0xAF, 0xF5, 0xFC, 0x6C, 0xFF, 0x07, 0x9E, 0x13, 0x3C, 0x39, 0x80]),
	bytes([0xD8, 0xCC, 0xE1, 0x26, 0x6A, 0x35, 0x3F, 0xCC, 0x20, 0xF3, 0x2D, 0x3B, 0x51, 0x7D, 0xE9, 0xC0])

]

# bis_key_sources
Bis_Key_Sources = [
	bytes([0xF8, 0x3F, 0x38, 0x6E, 0x2C, 0xD2, 0xCA, 0x32, 0xA8, 0x9A, 0xB9, 0xAA, 0x29, 0xBF, 0xC7, 0x48, 0x7D, 0x92, 0xB0, 0x3A, 0xA8, 0xBF, 0xDE, 0xE1, 0xA7, 0x4C, 0x3B, 0x6E, 0x35, 0xCB, 0x71, 0x06]),
	bytes([0x41, 0x00, 0x30, 0x49, 0xDD, 0xCC, 0xC0, 0x65, 0x64, 0x7A, 0x7E, 0xB4, 0x1E, 0xED, 0x9C, 0x5F, 0x44, 0x42, 0x4E, 0xDA, 0xB4, 0x9D, 0xFC, 0xD9, 0x87, 0x77, 0x24, 0x9A, 0xDC, 0x9F, 0x7C, 0xA4]),
	bytes([0x52, 0xC2, 0xE9, 0xEB, 0x09, 0xE3, 0xEE, 0x29, 0x32, 0xA1, 0x0C, 0x1F, 0xB6, 0xA0, 0x92, 0x6C, 0x4D, 0x12, 0xE1, 0x4B, 0x2A, 0x47, 0x4C, 0x1C, 0x09, 0xCB, 0x03, 0x59, 0xF0, 0x15, 0xF4, 0xE4]),
	bytes([0x52, 0xC2, 0xE9, 0xEB, 0x09, 0xE3, 0xEE, 0x29, 0x32, 0xA1, 0x0C, 0x1F, 0xB6, 0xA0, 0x92, 0x6C, 0x4D, 0x12, 0xE1, 0x4B, 0x2A, 0x47, 0x4C, 0x1C, 0x09, 0xCB, 0x03, 0x59, 0xF0, 0x15, 0xF4, 0xE4])
]

# master key sources
Master_Key_Sources = [
	#bytes([0x46, 0x22, 0xB4, 0x51, 0x9A, 0x7E, 0xA7, 0x7F, 0x62, 0xA1, 0x1F, 0x8F, 0xC5, 0x3A, 0xDB, 0xFE]), # /* Zeroes encrypted with Master Key 00. */
	bytes([0x39, 0x33, 0xF9, 0x31, 0xBA, 0xE4, 0xA7, 0x21, 0x2C, 0xDD, 0xB7, 0xD8, 0xB4, 0x4E, 0x37, 0x23]), # /* Master key 00 encrypted with Master key 01. */
	bytes([0x97, 0x29, 0xB0, 0x32, 0x43, 0x14, 0x8C, 0xA6, 0x85, 0xE9, 0x5A, 0x94, 0x99, 0x39, 0xAC, 0x5D]), # /* Master key 01 encrypted with Master key 02. */
	bytes([0x2C, 0xCA, 0x9C, 0x31, 0x1E, 0x07, 0xB0, 0x02, 0x97, 0x0A, 0xD8, 0x03, 0xA2, 0x76, 0x3F, 0xA3]), # /* Master key 02 encrypted with Master key 03. */
	bytes([0x9B, 0x84, 0x76, 0x14, 0x72, 0x94, 0x52, 0xCB, 0x54, 0x92, 0x9B, 0xC4, 0x8C, 0x5B, 0x0F, 0xBA]), # /* Master key 03 encrypted with Master key 04. */
	bytes([0x78, 0xD5, 0xF1, 0x20, 0x3D, 0x16, 0xE9, 0x30, 0x32, 0x27, 0x34, 0x6F, 0xCF, 0xE0, 0x27, 0xDC]), # /* Master key 04 encrypted with Master key 05. */
	bytes([0x6F, 0xD2, 0x84, 0x1D, 0x05, 0xEC, 0x40, 0x94, 0x5F, 0x18, 0xB3, 0x81, 0x09, 0x98, 0x8D, 0x4E]), # /* Master key 05 encrypted with Master key 06. */
	bytes([0x37, 0xAF, 0xAB, 0x35, 0x79, 0x09, 0xD9, 0x48, 0x29, 0xD2, 0xDB, 0xA5, 0xA5, 0xF5, 0x30, 0x19]), # /* Master key 06 encrypted with Master key 07. */
	bytes([0xEC, 0xE1, 0x46, 0x89, 0x37, 0xFD, 0xD2, 0x15, 0x8C, 0x3F, 0x24, 0x82, 0xEF, 0x49, 0x68, 0x04]), # /* Master key 07 encrypted with Master key 08. */
	bytes([0x43, 0x3D, 0xC5, 0x3B, 0xEF, 0x91, 0x02, 0x21, 0x61, 0x54, 0x63, 0x8A, 0x35, 0xE7, 0xCA, 0xEE]), # /* Master key 08 encrypted with Master key 09. */
	bytes([0x6C, 0x2E, 0xCD, 0xB3, 0x34, 0x61, 0x77, 0xF5, 0xF9, 0xB1, 0xDD, 0x61, 0x98, 0x19, 0x3E, 0xD4]), # /* Master key 09 encrypted with Master key 0A. */
	bytes([0x21, 0x88, 0x6B, 0x10, 0x9E, 0x83, 0xD6, 0x52, 0xAB, 0x08, 0xDB, 0x6D, 0x39, 0xFF, 0x1C, 0x9C]), # /* Master key 0A encrypted with Master key 0B. */
	bytes([0x8A, 0xCE, 0xC4, 0x7F, 0xBE, 0x08, 0x61, 0x88, 0xD3, 0x73, 0x64, 0x51, 0xE2, 0xB6, 0x53, 0x15]), # /* Master key 0B encrypted with Master key 0C. */
	bytes([0x08, 0xE0, 0xF4, 0xBE, 0xAA, 0x6E, 0x5A, 0xC3, 0xA6, 0xBC, 0xFE, 0xB9, 0xE2, 0xA3, 0x24, 0x12]), # /* Master key 0C encrypted with Master key 0D. */
	bytes([0xD6, 0x80, 0x98, 0xC0, 0xFA, 0xC7, 0x13, 0xCB, 0x93, 0xD2, 0x0B, 0x82, 0x4C, 0xA1, 0x7B, 0x8D]), # /* Master key 0D encrypted with Master key 0E. */
	bytes([0x78, 0x66, 0x19, 0xBD, 0x86, 0xE7, 0xC1, 0x09, 0x9B, 0x6F, 0x92, 0xB2, 0x58, 0x7D, 0xCF, 0x26]), # /* Master key 0E encrypted with Master key 0F. */
	bytes([0x39, 0x1E, 0x7E, 0xF8, 0x7E, 0x73, 0xEA, 0x6F, 0xAF, 0x00, 0x3A, 0xB4, 0xAA, 0xB8, 0xB7, 0x59]), # /* Master key 0F encrypted with Master key 10. */
	bytes([0x0C, 0x75, 0x39, 0x15, 0x53, 0xEA, 0x81, 0x11, 0xA3, 0xE0, 0xDC, 0x3D, 0x0E, 0x76, 0xC6, 0xB8]), # /* Master key 10 encrypted with Master key 11. */
	bytes([0x90, 0x64, 0xF9, 0x08, 0x29, 0x88, 0xD4, 0xDC, 0x73, 0xA4, 0xA1, 0x13, 0x9E, 0x59, 0x85, 0xA0]), # /* Master key 11 encrypted with Master key 12. */
]
# ^ todo: add latest master_key_sources from https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L138-L158

master_kek_sources = [
	bytes([0x37, 0x4B, 0x77, 0x29, 0x59, 0xB4, 0x04, 0x30, 0x81, 0xF6, 0xE5, 0x8C, 0x6D, 0x36, 0x17, 0x9A]),
	bytes([0x9A, 0x3E, 0xA9, 0xAB, 0xFD, 0x56, 0x46, 0x1C, 0x9B, 0xF6, 0x48, 0x7F, 0x5C, 0xFA, 0x09, 0x5C]),
	bytes([0xDE, 0xDC, 0xE3, 0x39, 0x30, 0x88, 0x16, 0xF8, 0xAE, 0x97, 0xAD, 0xEC, 0x64, 0x2D, 0x41, 0x41]),
	bytes([0x1A, 0xEC, 0x11, 0x82, 0x2B, 0x32, 0x38, 0x7A, 0x2B, 0xED, 0xBA, 0x01, 0x47, 0x7E, 0x3B, 0x67]),
	bytes([0x30, 0x3F, 0x02, 0x7E, 0xD8, 0x38, 0xEC, 0xD7, 0x93, 0x25, 0x34, 0xB5, 0x30, 0xEB, 0xCA, 0x7A]),
	bytes([0x84, 0x67, 0xB6, 0x7F, 0x13, 0x11, 0xAE, 0xE6, 0x58, 0x9B, 0x19, 0xAF, 0x13, 0x6C, 0x80, 0x7A]),
	bytes([0x68, 0x3B, 0xCA, 0x54, 0xB8, 0x6F, 0x92, 0x48, 0xC3, 0x05, 0x76, 0x87, 0x88, 0x70, 0x79, 0x23]),
	bytes([0xF0, 0x13, 0x37, 0x9A, 0xD5, 0x63, 0x51, 0xC3, 0xB4, 0x96, 0x35, 0xBC, 0x9C, 0xE8, 0x76, 0x81]),
	bytes([0x6E, 0x77, 0x86, 0xAC, 0x83, 0x0A, 0x8D, 0x3E, 0x7D, 0xB7, 0x66, 0xA0, 0x22, 0xB7, 0x6E, 0x67]),
	bytes([0x99, 0x22, 0x09, 0x57, 0xA7, 0xF9, 0x5E, 0x94, 0xFE, 0x78, 0x7F, 0x41, 0xD6, 0xE7, 0x56, 0xE6]),
	bytes([0x71, 0xB9, 0xA6, 0xC0, 0xFF, 0x97, 0x6B, 0x0C, 0xB4, 0x40, 0xB9, 0xD5, 0x81, 0x5D, 0x81, 0x90]),
	bytes([0x00, 0x04, 0x5D, 0xF0, 0x4D, 0xCD, 0x14, 0xA3, 0x1C, 0xBF, 0xDE, 0x48, 0x55, 0xBA, 0x35, 0xC1]),
	bytes([0xD7, 0x63, 0x74, 0x46, 0x4E, 0xBA, 0x78, 0x0A, 0x7C, 0x9D, 0xB3, 0xE8, 0x7A, 0x3D, 0x71, 0xE3]),
]
# ^ todo: add latest master_kek_source from https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L36

mariko_master_kek_sources = [
	bytes([0x32, 0xC0, 0x97, 0x6B, 0x63, 0x6D, 0x44, 0x64, 0xF2, 0x3A, 0xA5, 0xC0, 0xDE, 0x46, 0xCC, 0xE9]),
	bytes([0xCC, 0x97, 0x4C, 0x46, 0x2A, 0x0C, 0xB0, 0xA6, 0xC9, 0xC0, 0xB7, 0xBE, 0x30, 0x2E, 0xC3, 0x68]),
	bytes([0x86, 0xBD, 0x1D, 0x76, 0x50, 0xDF, 0x6D, 0xFA, 0x2C, 0x7D, 0x33, 0x22, 0xAB, 0xF1, 0x82, 0x18]),
	bytes([0xA3, 0xB1, 0xE0, 0xA9, 0x58, 0xA2, 0x26, 0x7F, 0x40, 0xBF, 0x5B, 0xBB, 0x87, 0x33, 0x0B, 0x66]),
	bytes([0x82, 0x72, 0x91, 0x65, 0x40, 0x3B, 0x9D, 0x66, 0x60, 0xD0, 0x1B, 0x3D, 0x4D, 0xA5, 0x70, 0xE1]),
	bytes([0xF9, 0x37, 0xCF, 0x9A, 0xBD, 0x86, 0xBB, 0xA9, 0x9C, 0x9E, 0x03, 0xC4, 0xFC, 0xBC, 0x3B, 0xCE]),
	bytes([0x75, 0x2D, 0x2E, 0xF3, 0x2F, 0x3F, 0xFE, 0x65, 0xF4, 0xA9, 0x83, 0xB4, 0xED, 0x42, 0x63, 0xBA]),
	bytes([0x4D, 0x5A, 0xB2, 0xC9, 0xE9, 0xE4, 0x4E, 0xA4, 0xD3, 0xBF, 0x94, 0x12, 0x36, 0x30, 0xD0, 0x7F]),
	bytes([0xEC, 0x5E, 0xB5, 0x11, 0xD5, 0x43, 0x1E, 0x6A, 0x4E, 0x54, 0x6F, 0xD4, 0xD3, 0x22, 0xCE, 0x87]),
	bytes([0x18, 0xA5, 0x6F, 0xEF, 0x72, 0x11, 0x62, 0xC5, 0x1A, 0x14, 0xF1, 0x8C, 0x21, 0x83, 0x27, 0xB7]),
	bytes([0x3A, 0x9C, 0xF0, 0x39, 0x70, 0x23, 0xF6, 0xAF, 0x71, 0x44, 0x60, 0xF4, 0x6D, 0xED, 0xA1, 0xD6]),
	bytes([0x43, 0xDB, 0x9D, 0x88, 0xDB, 0x38, 0xE9, 0xBF, 0x3D, 0xD7, 0x83, 0x39, 0xEF, 0xB1, 0x4F, 0xA7]),
	bytes([0xE4, 0x45, 0xD0, 0x14, 0xA0, 0xE5, 0xE9, 0x4B, 0xFE, 0x76, 0xF4, 0x29, 0x41, 0xBB, 0x64, 0xED]),
	bytes([0x65, 0x7B, 0x11, 0x46, 0x0E, 0xC2, 0x22, 0x5D, 0xB9, 0xF1, 0xF5, 0x00, 0xF9, 0x3E, 0x1F, 0x70])
]
# ^ todo: add latest mariko_master_kek_source from https://github.com/Atmosphere-NX/Atmosphere/blob/master/fusee/program/source/fusee_key_derivation.cpp#L31

# mariko master_kek_sources
master_kek_source = master_kek_sources[-1]

with open(keys, 'w') as manual_crypto:	
	manual_crypto.write(f'tsec_auth_signature_00 = ' + f'{tsec_auth_signature_00.hex().upper()}\n')
	manual_crypto.write(f'tsec_auth_signature_01 = ' + f'{tsec_auth_signature_00.hex().upper()}\n')
	manual_crypto.write(f'tsec_auth_signature_02 = ' + f'{tsec_auth_signature_00.hex().upper()}\n\n')

	manual_crypto.write(f'tsec_root_key_02 = ' + f'{tsec_root_key_02.hex().upper()}\n\n')

	manual_crypto.write(f'keyblob_mac_key_source = ' + f'{keyblob_mac_key_source.hex().upper()}\n')
	# Write keyblob_key_source_%%
	count = -1
	for i in Keyblob_Key_Sources:
		count = count + 0x1
		keys = f'keyblob_key_source_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')
	# Write master_kek_sources
	count = 0x5
	for i in master_kek_sources:
		count = count + 0x1
		keys = f'master_kek_source_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')

	# Write mariko_master_kek_sources
	count = 0x4
	for i in mariko_master_kek_sources:
		count = count + 0x1
		keys = f'mariko_master_kek_source_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')
	# generate master_kek_%% from all provided mariko_master_kek_sources
	master_keks = [decrypt(i, tsec_root_key_02) for i in master_kek_sources]
	count = 0x5
	for i in master_keks:
		count = count + 0x1
		keys = f'master_kek_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')
	
	manual_crypto.write(f'\n')
	manual_crypto.write(f'master_key_source = ' + f'{master_key_source.hex().upper()}\n\n')

	# generate master_key_%% from all provided master_kek_%% using master_key_source
	current_master_key = decrypt(master_key_source, master_keks[-1])

	current_master_key_revision = len(Master_Key_Sources)
	master_keys = []
	first = True
	for i in reversed(Master_Key_Sources):
		if first:
			first = False
			previous_key = i
			next_master_key = decrypt(previous_key, current_master_key)
			current_master_key_revision = current_master_key_revision -1
			master_keys.append(current_master_key)
			master_keys.append(next_master_key)
		else:
			key = previous_key
			previous_key = i
			next_master_key = decrypt(previous_key, next_master_key)
			current_master_key_revision = current_master_key_revision -1
			master_keys.append(next_master_key)


	# Write master_key_%%
	count = -0x1
	for i in reversed(master_keys):
		count = count + 0x1
		keys = f'master_key_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')
	manual_crypto.write(f'package2_key_source = ' + f'{package2_key_source.hex().upper()}\n\n')

	# generate package2_key_%% from all provided master_key_%% using package2_key_source
	package2_key = [decrypt(package2_key_source, i) for i in master_keys]
	count = -0x1
	for i in package2_key:
		count = count + 0x1
		keys = f'package2_key_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')
	manual_crypto.write(f'bis_kek_source = ' + f'{bis_kek_source.hex().upper()}\n')
	# Write bis_key_source_%%
	count = -1
	for i in Bis_Key_Sources:
		count = count + 0x1
		keys = f'bis_key_source_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')
	manual_crypto.write(f'per_console_key_source = ' + f'{per_console_key_source.hex().upper()}\n')
	manual_crypto.write(f'retail_specific_aes_key_source = ' + f'{retail_specific_aes_key_source.hex().upper()}\n')
	manual_crypto.write(f'aes_kek_generation_source = ' + f'{aes_kek_generation_source.hex().upper()}\n')
	manual_crypto.write(f'aes_key_generation_source = ' + f'{aes_key_generation_source.hex().upper()}\n')
	manual_crypto.write(f'titlekek_source = ' + f'{titlekek_source.hex().upper()}\n\n')

	# generate title_kek_%% from all provided master_key_%% using titlekek_source
	titlekek = [decrypt(titlekek_source, i) for i in master_keys]
	count = -0x1
	for i in titlekek:
		count = count + 0x1
		keys = f'titlekek_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')

	manual_crypto.write(f'header_kek_source = ' + f'{header_kek_source.hex().upper()}\n')
	manual_crypto.write(f'header_key_source = ' + f'{header_key_source.hex().upper()}\n')
	manual_crypto.write(f'header_key = ' + f'{header_key.hex().upper()}\n\n')

	manual_crypto.write(f'key_area_key_system_source = ' + f'{key_area_key_system_source.hex().upper()}\n')
	manual_crypto.write(f'key_area_key_application_source = ' + f'{key_area_key_application_source.hex().upper()}\n')
	manual_crypto.write(f'key_area_key_ocean_source = ' + f'{key_area_key_ocean_source.hex().upper()}\n\n')

	manual_crypto.write(f'save_mac_kek_source = ' + f'{save_mac_kek_source.hex().upper()}\n')
	manual_crypto.write(f'save_mac_key_source_00 = ' + f'{save_mac_key_source_00.hex().upper()}\n')
	manual_crypto.write(f'save_mac_key_source_01 = ' + f'{save_mac_key_source_01.hex().upper()}\n')
	manual_crypto.write(f'save_mac_sd_card_kek_source = ' + f'{save_mac_sd_card_kek_source.hex().upper()}\n')
	manual_crypto.write(f'save_mac_sd_card_key_source = ' + f'{save_mac_sd_card_key_source.hex().upper()}\n')
	manual_crypto.write(f'sd_card_kek_source = ' + f'{sd_card_kek_source.hex().upper()}\n\n')


	# generate key_area_key_application_%% from all provided master_key_%% using key_area_key_application_source
	key_area_key_application = [generateKek(key_area_key_application_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
	count = -0x1
	for i in key_area_key_application:
		count = count +0x1
		keys = f'key_area_key_application_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')

	# generate key_area_key_ocean_%% from all provided master_key_%% using key_area_key_ocean_source
	key_area_key_ocean = [generateKek(key_area_key_ocean_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
	count = -0x1
	for i in key_area_key_ocean:
		count = count +0x1
		keys = f'key_area_key_ocean_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')

	manual_crypto.write(f'\n')

	# generate key_area_key_system_%% from all provided master_key_%% using key_area_key_system_source
	key_area_key_system = [generateKek(key_area_key_system_source, i, aes_kek_generation_source, aes_key_generation_source) for i in master_keys]
	count = -0x1
	for i in key_area_key_system:
		count = count +0x1
		keys = f'key_area_key_system_dev_{hex(count)[2:].zfill(2)} = '  + (i.hex().upper())
		manual_crypto.write(f'{keys}\n')