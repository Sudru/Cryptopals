from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt_aes_ecb(ciphertext,key):
    cipher = AES.new(key,AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(ciphertext),AES.block_size)
    return decrypted_data

def main():
    with open("challenge7.txt","r") as f:
        ciphertext = base64.b64decode(f.read())
        key = b"YELLOW SUBMARINE"
        plaintext = decrypt_aes_ecb(ciphertext,key)
        print(plaintext.decode())

if __name__ == "__main__":
    main()