def repeating_key_xor(text,key):
    xored = []
    for i in range(len(text)):
        xored.append(text[i]^key[i%len(key)])
    return bytes(xored)


if __name__ == "__main__":
    txt1 = b"Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
    key = b"ICE"
    print(repeating_key_xor(txt1,key).hex())