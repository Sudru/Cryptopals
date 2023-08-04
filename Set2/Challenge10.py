"""
CBC (Cipher Block Chaining) is a block cipher mode of operation commonly used to provide confidentiality
and data integrity when encrypting data. In CBC mode, each plaintext block is XORed with the previous
ciphertext block before encryption. This process creates a dependency between blocks, making it more
secure than ECB mode.
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def fixed_xor(first_string,second_string):
    if len(first_string) != len(second_string):
        return "Unequal Length !!"
    xor_string = [a^b for a,b in zip(first_string,second_string)]
    return bytes(xor_string)

def padding(data, block_size):
    pad_length = block_size - (len(data) % block_size)
    padding = bytes([pad_length] * pad_length)
    return data + padding

def unpadding(padded_text, block_size):
    pad_length = padded_text[-1]
    return bytes([a for a in padded_text if a!=pad_length])


"""
The basic steps of CBC encryption are as follows:

- Divide the plaintext into fixed-size blocks.
- XOR the first plaintext block with an Initialization Vector (IV).
- Encrypt the result of the XOR operation using the block cipher.
- Take the resulting ciphertext and XOR it with the next plaintext block.
- Repeat steps 3 and 4 for each subsequent block.
"""

def encrypt_cbc(plaintext,key,iv):
    block_size = 16
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = padding(plaintext,block_size)
    previous_block = iv
    cipher_text = b''
    for i in range(0,len(plaintext),block_size):
        block = plaintext[i:i+block_size]
        xor = fixed_xor(block,previous_block) # xor with the previous encrypted block
        encrypted_block = cipher.encrypt(xor) #encrypt the result 
        cipher_text += encrypted_block #add to the cipher text
        previous_block = encrypted_block #set current block as the previous block
    return cipher_text


"""
During decryption, the same steps are followed in reverse:

- Divide the ciphertext into fixed-size blocks.
- Decrypt the ciphertext block using the block cipher.
- XOR the result of decryption with the previous ciphertext block to obtain the plaintext.
"""
def decrypt_cbc(ciphertext,key,iv):
    block_size = 16
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = b''
    previous_block = iv
    for i in range(0, len(ciphertext), block_size):
        encrypted_block = ciphertext[i:i + block_size]
        decrypted_block = cipher.decrypt(encrypted_block)
        plaintext_block = fixed_xor(decrypted_block, previous_block)
        plaintext += plaintext_block
        previous_block = encrypted_block

    
    plaintext = unpadding(plaintext, block_size)
    print(plaintext)

plaintext = b"I am Sudru and I am testing my CBC implementation!!"
key = b"1234567891234567"
iv = b"YELLOW SUBMARINE"
encrypted = encrypt_cbc(plaintext,key,iv)
print(encrypted)
decrypt_cbc(encrypted,key,iv)