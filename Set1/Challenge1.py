import binascii
import base64
import sys
def hex_to_b64(hex):
    return base64.b64encode(binascii.unhexlify(hex)).decode()

def main():
    if len(sys.argv) == 1:
        hex =  input("Hex value:\n")
    else:
        hex = sys.argv[1]
    
    print(hex_to_b64(hex))


if __name__== "__main__":
    main()
