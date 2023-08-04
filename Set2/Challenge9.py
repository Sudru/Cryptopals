# PKCS#7 padding is a method used to pad data to a specified block size. 
# It is commonly used in symmetric encryption algorithms to ensure that the input data is a multiple of the block size. 
# The padding value is the number of bytes added, and each byte of padding has the same value as the number of bytes added.

def pkcs7_padding(data, block_size):
    pad_length = block_size - (len(data) % block_size)
    padding = bytes([pad_length] * pad_length)
    return data + padding


def main():
    text = b"YELLOW SUBMARINE"
    print(pkcs7_padding(text,21))

if __name__ == "__main__":
    main()