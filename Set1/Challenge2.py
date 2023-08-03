def fixed_xor(first_string,second_string):
    if len(first_string) != len(second_string):
        return "Unequal Length !!"
    xor_string = [a^b for a,b in zip(first_string,second_string)]
    return bytes(xor_string)
def main():
    s1 = bytes.fromhex(input("String 1: \n"))
    s2 = bytes.fromhex(input("String 2: \n"))
    print(fixed_xor(s1,s2))
if __name__== "__main__":
    main()
