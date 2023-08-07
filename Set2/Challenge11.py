from Crypto.Cipher import AES
import random
import string

"""
Determines whether a given cipher text is ecb or cbc based on matching block 
In ECB two blocks with identical text product identical cipher text
"""
def detect_ecb(line):
    blocks = [line[i:i+16] for i in range(0,len(line),16)]
    repeating_block = {}
    for b in blocks:
        count = blocks.count(b)
        if count >1:
            repeating_block[b]=blocks.count(b)       
    return len(repeating_block)>0



def generate_key(key_size):
    key = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(key_size)])
    return key.encode()

def encryption_oracle(plaintext):
    random_key = generate_key(16)
    mode = random.randint(0,1)
    ciphertext = ""
    if mode:
        print("Choosing ECB")
        cipher = AES.new(random_key,AES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext)
    else:
        print("Choosing CBC")
        cipher = AES.new(random_key,AES.MODE_CBC)
        ciphertext = cipher.encrypt(plaintext)
    
    if detect_ecb(ciphertext):
        print("Detected ECB")
    else:
        print("Detected CBC")

def main():
    plaintext = b"YELLOW SUBMARINE sudarshan 1904 YELLOW SUBMARINE"
    encryption_oracle(plaintext)

if __name__ == "__main__":
    main()