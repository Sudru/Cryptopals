def detect_ecb(lines):
    likely_ecb = {}
    for line in lines:
            raw = bytes.fromhex(line)
            blocks = [raw[i:i+16] for i in range(0,len(raw),16)]
            repeating_block = {}
            for b in blocks:
                count = blocks.count(b)
                if count >1:
                    repeating_block[b]=blocks.count(b)
            if(len(repeating_block)>0):
                likely_ecb[line]=len(repeating_block)
    return likely_ecb

def main():
    with open("challenge8.txt","r") as f:
        lines = f.readlines()
        print(detect_ecb(lines))

if __name__ == "__main__":
    main()