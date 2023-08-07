from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import binascii
import base64
import string

def get_block_size():
    cipher = AES.new(key,AES.MODE_ECB)
    initial_length = len(cipher.encrypt(pad(b'',AES.block_size)))
    i = 1
    while True:
        length = len(cipher.encrypt(pad(b'A' * i,AES.block_size)))
        # print(f"{i} : {length}")
        if length != initial_length:
            return length - initial_length,i-1
        i += 1

text = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
key = b"qIV9fVWNkP1C6Uvr"
decoded = base64.b64decode(text)
def byte_at_a_time():
    cipher = AES.new(key, AES.MODE_ECB)
    block_size = AES.block_size
    secret_text = b''
    input_block = b'A'*15
    #create a map of encrypted block of 15 A and one byte for checking the actual encrypted byte.
    mapper_dictionary = {}
    for byte in string.printable:
        crafted_input = pad(input_block + byte.encode(), block_size)
        encrypted_text = cipher.encrypt(crafted_input)[:block_size]
        mapper_dictionary[encrypted_text] = byte
    #for each character in the unknown string append with the 15 A and the character
    # and compare with the mapper dictionary
    for i in range(len(decoded)):
        crafted = pad(input_block+bytes([decoded[i]]), block_size)
        encrypted = cipher.encrypt(crafted)[:block_size]
        decrypted_byte = mapper_dictionary.get(encrypted)
        if decrypted_byte:
            secret_text += decrypted_byte.encode()
        else:
            break

    return secret_text

if __name__ == '__main__':
    decrypted_secret = byte_at_a_time()
    print("Decrypted secret:", decrypted_secret.decode())