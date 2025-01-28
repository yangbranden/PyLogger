import zlib
import base64
import string
import sys
import token
import tokenize

# SETTINGS
ITERATIONS = 199

def obfuscate(file_content):
    obfuscated_bytes = file_content
    
    for i in range(ITERATIONS):
        obfuscated_bytes = zlib.compress(obfuscated_bytes) # zlib compress
        obfuscated_bytes = base64.b64encode(obfuscated_bytes) # b64 encode
        obfuscated_bytes = obfuscated_bytes[::-1] # reverse bytes

        # add the exec lambda function bytes if not last loop
        if i != ITERATIONS-1:
            obfuscated_bytes = b"exec((_)(b'" + obfuscated_bytes + b"'))"
        # print(f"ITERATION {i}: {obfuscated_bytes}")
    
    # add the lambda
    obfuscated_bytes = b"_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'" + obfuscated_bytes + b"'))"
    
    return obfuscated_bytes

def strip_comments(file_content):
    stripped_content = b''

    lines = file_content.split(b'\n')

    # remove comments before we obfuscate
    for line in lines:
        if b'#' in line:
            test = line.strip(b' \t')
            if test.startswith(b'#'):
                continue
        elif len(line) == 0:
            continue
        stripped_content += line

    return stripped_content

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 obfuscate.py [file to obfuscate]")
        sys.exit()
    try:
        with open(sys.argv[1], 'rb') as f:
            file_content = f.read()
            stripped_content = strip_comments(file_content)
            obfuscated = obfuscate(stripped_content)
            print("Obfuscated content:", obfuscated)
            new_file = open(f"obfuscated_{sys.argv[1]}", 'wb+')
            new_file.write(obfuscated)

    except Exception as e:
        print(e)
