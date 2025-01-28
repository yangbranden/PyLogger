import zlib
import base64
import string
import sys

# Number of times to go through obfuscation loop
ITERATIONS = 41

def deobfuscate(file_content):
    deobfuscated_bytes = file_content
    
    # print(deobfuscated_bytes)

    # remove the lambda
    deobfuscated_bytes = deobfuscated_bytes.split(b"_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'")[1]
    deobfuscated_bytes = deobfuscated_bytes.split(b"'))")[0]
    

    for i in range(ITERATIONS):
        # print(f"ITERATION {i} START: {deobfuscated_bytes}")
        # strip exec lambda function bytes
        deobfuscated_bytes = deobfuscated_bytes[::-1] # reverse bytes
        deobfuscated_bytes = base64.b64decode(deobfuscated_bytes) # b64 decode
        deobfuscated_bytes = zlib.decompress(deobfuscated_bytes) # zlib decompress
        if i != ITERATIONS-1:
            deobfuscated_bytes = deobfuscated_bytes.split(b"exec((_)(b'")[1]
            deobfuscated_bytes = deobfuscated_bytes.split(b"'))")[0]
        # print(f"ITERATION {i} END: {deobfuscated_bytes}")
    
    return deobfuscated_bytes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 deobfuscate.py [file to deobfuscate]")
        sys.exit()
    try:
        with open(sys.argv[1], 'rb') as f:
            file_content = f.read()
            deobfuscated = deobfuscate(file_content)
            print("Deobfuscated content:", deobfuscated)
            new_file = open(f"deobfuscated_{sys.argv[1].lstrip("obfuscated_")}", 'wb+')
            new_file.write(deobfuscated)

    except Exception as e:
        print(e)