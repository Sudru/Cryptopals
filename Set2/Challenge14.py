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




def break_ecb_with_prefix(oracle, key, block_size, prefix_length, suffix_length):
    total_length = len(oracle(b'', key))

    unknown_length = total_length - prefix_length - suffix_length

    target_start_block = (prefix_length + block_size - 1) // block_size
    decrypted_data = b''

    # Iterate over the blocks containing the target bytes
    for block_index in range(target_start_block, total_length//16):
        # Initialize the current block
        current_block = b''

        # Iterate over the bytes within the block
        for byte_index in range(block_size):
            # Craft the input data to target the current byte within the block
            input_data = b'A' * (block_size - byte_index - 1 + prefix_length % block_size)
            target_block = oracle(input_data, key)[block_index * block_size: (block_index + 1) * block_size]

            # Try all possible bytes to find the correct byte for the current position
            for i in range(256):
                test_input_data = input_data + current_block + bytes([i])
                test_block = oracle(test_input_data, key)[block_index * block_size: (block_index + 1) * block_size]
                if test_block == target_block:
                    # Found the correct byte, add it to the current block
                    current_block += bytes([i])
                    break

        # Append the decrypted bytes of the current block to the final decrypted data
        decrypted_data += current_block

    # Remove padding
    # decrypted_data = unpad(decrypted_data)

    return decrypted_data

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
    decrypted_data = break_ecb_with_prefix(oracle, key, block_size, prefix_length,suffix_length)
    print("Decrypted data:", decrypted_data)

