from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
key = b"sudarshandevkota"

def pad(data, block_size):
    if len(data)%block_size == 0:
        return data
    pad_length = block_size - (len(data) % block_size)
    padding = bytes([pad_length] * pad_length)
    return data + padding

# parse "foo=bar&baz=qux&zap=zazzle" to a json or dictionary
def parse_profile(profile):
    profile_dict = {}
    for property in profile.split(b'&'):
        key,value = property.split(b'=')
        profile_dict[key.decode()] = value.decode()
    return profile_dict


def profile_for(email):
    email = email.replace("&","").replace("=","")
    return ("email="+email+"&uid=10&role=user").encode()

#give the encrypted encoded profile for the provided email 
def encrypt(encoded_text):    
    cipher = AES.new(key,AES.MODE_ECB)
    padded = pad(encoded_text,AES.block_size)
    return cipher.encrypt(padded)

#decrypt and parse the given encrypted profile text
def parse_profile_decrypted(ciphertext):
    cipher = AES.new(key,AES.MODE_ECB)
    decrypted_byte = cipher.decrypt(ciphertext)
    unpadded = unpad(decrypted_byte,AES.block_size)
    return parse_profile(unpadded)

"""
The goal of the challenge is to create a encrypted profile
ciphertext which on decryption give a user with role admin 
using profile_for and encrypt function.
"""

def challenge():
    profile = profile_for("test@test.com")
    #This shows the length to be 36 for email=test@test.com&uid=10&role=user i.e 16*2 = 32 + 4(user) 3rd block
    print(f"{profile} : length = {len(profile)}")
    encrypted = encrypt(profile)
    # the length is 48 = 16*3 so third block is user+padding
    print(f"\n{encrypted}: length = {len(encrypted)}")
    encrypted_blocks = [encrypted[i:i+16] for i in range(0,len(encrypted),16)]
    print("\nThe encrypted blocks are:")
    for block in encrypted_blocks:
        print(block)
    
    print("\nThe malicious block which will replace the last block:")
    malicious_block = encrypt(pad(b"admin",AES.block_size))
    print(malicious_block)

    final_crafted = encrypted_blocks[0] + encrypted_blocks[1] + malicious_block
    
    print(parse_profile_decrypted(final_crafted))
    
challenge()