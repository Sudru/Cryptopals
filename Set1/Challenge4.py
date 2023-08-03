from Challenge3 import decrypt_xor

with open("./challenge4.txt","r") as f:
    possible = {}
    hex_values = f.readlines()
    for hex in hex_values:
        cipher =  bytes.fromhex(hex)
        decrypted = decrypt_xor(cipher)
        if decrypted:
            possible[hex]=decrypted
    
    print(possible)