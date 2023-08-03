import string
from nostril import nonsense
import re

def evaluate_random(text):
    valid_list = string.ascii_letters+"'\" ?.\n-:#$_"+"0123456789"
    for c in text:
        if c not in valid_list:
            return True
    try:
        return nonsense(text)
    except:
        return True
        
def decrypt_xor(cipher_text):

    likely_texts = {}
    for k in range(256):
        deciphered_text = ''.join(chr(a ^ k) for a in cipher_text)
        random = evaluate_random(deciphered_text)
        if not random:
            likely_texts[k]=deciphered_text
    return likely_texts

if __name__ == "__main__":
    raw_hex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    cipher_text = bytes.fromhex(raw_hex)
    print(decrypt_xor(cipher_text=cipher_text))
