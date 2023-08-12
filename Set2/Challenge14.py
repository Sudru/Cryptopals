import os
import base64
from Crypto.Cipher import AES

target_bytes = base64.b64decode("Q3J5cHRvcGFscyBzZXQgMiBjb21wbGV0ZWQgI0hBQ0tFUgo=")

def encryption_oracle(input_data, key):
    prefix = b"SUBMARINE"
    plaintext = prefix + input_data + target_bytes
    padded_plaintext = pad(plaintext, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

def pad(data, block_size=16):
    if len(data)%block_size == 0:
        return data
    pad_length = block_size - (len(data) % block_size)
    padding = bytes([pad_length] * pad_length)
    return data + padding

def get_block_size(key):
    initial_length = len(encryption_oracle(pad(b'',AES.block_size),key))
    i = 1
    while True:
        length = len(encryption_oracle(pad(b'A' * i,AES.block_size),key))
        if length != initial_length:
            return length - initial_length
        i += 1

def find_prefix_length(oracle,key):
    for a in range(16):
        enc = oracle(b'A'*(32+a),key)
        blocks = [enc[i:i+16] for i in range(0,len(enc),16)]
        for b in range(1,len(blocks)-1):
            if blocks[b] == blocks[b+1]:
                return 16-a
    
def find_suffix_length(oracle,key,prefix_length):
    ref_length = len(oracle(b'',key))
    for i in range(1,17):
        length = len(oracle(b'A'*i,key))
        if length != ref_length:
            return ref_length - prefix_length - (i-1)




def decrypt_hidden_suffix(pre_len, suffix_length, oracle,key):
    n, suffix = 0, b''
    while len(suffix) < suffix_length:
        suffix = decrypt_block(n, suffix, pre_len, suffix_length, oracle,key)
        n += 1
    return suffix


def decrypt_block(n, suffix, pre_len, length, oracle,key):
    for i in range(16):
        if len(suffix) == length:
            return suffix

        inp = b'A' * (16 - pre_len%16) + b'A' * (15 - i)

        # Build dictionary and find next byte in the suffix.
        inp_len = pre_len + len(inp + suffix) + 1
        inputs = {
            oracle(inp + suffix + bytes([j]),key)[:inp_len]:(inp + suffix + bytes([j]))
            for j in range(256)
        }
        suffix += bytes([inputs[oracle(inp,key)[:inp_len]][-1]])
    return suffix

if __name__ == "__main__":
    key = os.urandom(16)
    oracle = lambda input_data, key: encryption_oracle(input_data, key)
    # Find the block size
    block_size = get_block_size(key)
    print("Block size:", block_size)

    # Find the length of the prefix
    prefix_length = find_prefix_length(oracle, key)
    print("Prefix length:", prefix_length)
    
    suffix_length = find_suffix_length(oracle,key,prefix_length)
    print("Suffix Length: ",suffix_length)

    # Break the ECB encryption with random prefix
    decrypted_data = decrypt_hidden_suffix(prefix_length,suffix_length,oracle,key)
    print("Decrypted data:", decrypted_data)

