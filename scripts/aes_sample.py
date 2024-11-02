import aes128

def decrypt(key, decryption_key):
	crypto = aes128.AESECB(decryption_key)
	return crypto.decrypt(key)

mariko_kek = bytes.fromhex("FILL-IN-MARIKO_KEK") # substitute with mariko_kek, sha256 string: 53be3a736bdb7ff26868ce73e9e5b8ad3b652039be75dfce89a91d11a4c69866
mariko_master_kek_source = bytes.fromhex("31BE25FBDBB4EE495C7705C2369F3480") # _12 / 19.0.0
master_key_source = bytes.fromhex("D8A2410AC6C59001C61D6A267C513F3C") # persistent from 1.0.0

# generate master_kek_%% from mariko_master_kek_source using mariko_kek as key
decrypt_master_kek_source = decrypt(mariko_master_kek_source, mariko_kek)
decrypt_master_kek_source_hex = decrypt_master_kek_source.hex().upper()
print(decrypt_master_kek_source_hex)

# generate master_key_%% from master_key_source using master_kek_%% as key
decrypt_master_key = decrypt(master_key_source, decrypt_master_kek_source)
decrypt_master_key_hex = decrypt_master_key.hex().upper()
print(decrypt_master_key_hex)