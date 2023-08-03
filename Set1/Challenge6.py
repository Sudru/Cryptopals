import base64
from Challenge3 import decrypt_xor
import string

#Repeating Key XOR
def repeating_key_xor(text,key):
    xored = []
    for i in range(len(text)):
        xored.append(text[i]^key[i%len(key)])
    return bytes(xored)


#Evaluate if the given text is random or not
def evaluate_random(text):
    valid_list = string.ascii_letters+"'\" \\x!?.\n-:#$_+,0123456789"
    for c in text:
        if c not in valid_list:
            return True
    return False

def decrypt_xor(cipher_text):

    likely_texts = {}
    for k in range(256):
        deciphered_text = ''.join(chr(a ^ k) for a in cipher_text)
        random = evaluate_random(deciphered_text)
        if not random:
            likely_texts[k] = deciphered_text
    return likely_texts


def hamming_distance(bytes1, bytes2):
    return sum(bin(a ^ b).count('1') for a, b in zip(bytes1, bytes2))


def get_binary_list(str1):
    binary_list = [format(ord(a), '08b') for a in str1]
    return binary_list

def test_hamming_distance():
    s1 = b"this is a test"
    s2 = b"wokka wokka!!!"
    print(hamming_distance(s1,s2))

def determine_likey_key_length(cipher_text):
    min_hamming_distance = float('inf')
    key_length = None
    for keysize in range(2, 41):
        block_list = []
        #get a list of 4 blocks of size equal to keysize
        for i in range(0, keysize * 4, keysize):
            block = cipher_text[i:i + keysize]
            block_list.append(block)
        # get the hamming distance of each block with other block in the list of 4 blocks
        distances = []
        for i in range(4):
            for j in range(i+1,4):
                distances.append(hamming_distance(block_list[i],block_list[j]) / keysize)
        # Average of the every each keysize 
        average_distance = sum(distances)/len(distances)
        if average_distance < min_hamming_distance:
            min_hamming_distance = average_distance
            key_length = keysize
    print(f"Key: {key_length} ==> Distance: {min_hamming_distance}")
    return key_length
def main():
    with open("challenge6.txt", "r") as f:
        encrypted_content = base64.b64decode(f.read())
        key_size = determine_likey_key_length(encrypted_content)
        decryption_key = ""
        #Brute force each byte of the key to get the full key
        for i in range(key_size):
            iterative_block = bytes(encrypted_content[i::key_size])
            decrypted = decrypt_xor(iterative_block)
            decryption_key += (chr(list(decrypted.keys())[0]))
        print("Decryption Key-> "+decryption_key)

        print(repeating_key_xor(encrypted_content,decryption_key.encode()).decode())
            
if __name__=="__main__":
    main()

