from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad


block_size = AES.block_size
key = b"sudarshandevkota"
iv = b"randombytes14444"

def fixed_xor(first_string,second_string):
    if len(first_string) != len(second_string):
        return "Unequal Length !!"
    xor_string = [a^b for a,b in zip(first_string,second_string)]
    return bytes(xor_string)

def pad(data, block_size=16):
    if len(data)%block_size == 0:
        return data
    pad_length = block_size - (len(data) % block_size)
    padding = bytes([pad_length] * pad_length)
    return data + padding

def wrap_userdata(data):
    pre = b"comment1=cooking%20MCs;userdata="
    post = b";comment2=%20like%20a%20pound%20of%20bacon"
    data = data.replace(b";",b"%3B").replace(b"=",b"%3D")
    combined = pre+data+post
    print(f"pre: {len(pre)} post: {len(post)} combined: {len(combined)}")
    cipher = AES.new(key,AES.MODE_CBC,iv)
    return cipher.encrypt(pad(combined))


def decrypt_and_check(ciphertext):
    global key
    cipher = AES.new(key,AES.MODE_CBC,iv)
    decrypted_text = cipher.decrypt(ciphertext)
    print(decrypted_text)
    
    return b";admin=true;" in decrypted_text

"""
The goal of the challenge is to make a user profile with admin=true
    - The blocks are all of 16 bytes which are encrypted individually then used to encrypted next block.
    - In this decryption of 1 blocks depends upon two blocks, so our input should be of two blocks
    - The prefix `comment1=cooking%20MCs;userdata=` is 32 which is exactly 2 blocks
    - Crafted input should be of 32 bytes (block 3rd and 4th) as well so we can modify 1 block in such way 
        that it decrypts next block with our payload in it.
"""
def challenge():
    userinput = b'A'*32
    encryppted_text = wrap_userdata(userinput)
    encrypted_blocks = [encryppted_text[i:i+block_size] for i in range(0,len(encryppted_text),block_size)]
    print("\nEncrypted text blocks with 32 As userinput: ")
    for block in encrypted_blocks:
        print(block)
    # We change the third block with XOR of 16As and our payload `;admin=true`.
    # As the 4th block decrypts to 16 As and is XORed with the 3rd block of Cipher text, The resulting plaintext is
    # user profile with admin=true due to property of XOR
    malicious_3rd_block = fixed_xor(userinput[:16],b'B'*5+b";admin=true")
    malicious_3rd_block = fixed_xor(encrypted_blocks[2],malicious_3rd_block)
    print(f"\nMalicious block: {malicious_3rd_block} => {len(malicious_3rd_block)}")
    final_crafted = b''
    for i in range(len(encrypted_blocks)):
        if i == 2:
            final_crafted+=malicious_3rd_block
        else:
            final_crafted+=encrypted_blocks[i]
    # print(f"\nFinal crafted payload: {final_crafted}")
    print(decrypt_and_check(final_crafted))
challenge()