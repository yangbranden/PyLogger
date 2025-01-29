# Python Keylogger

This is a Python code Keylogger created for educational purposes, with several capabilities/features beyond a simple Python script running on a machine. 

## Disclaimer

I do NOT promote or encourage any illegal activities with this code. This repository is provided solely for educational purposes and exploration of technical capabilities.

## Installation

Standard installation for any Python project.

```
git clone https://github.com/yangbranden/PyLogger.git
python -m venv venv/
source venv/Scripts/activate
pip install -r requirements.txt
```

## Compilation

The compilation process can be somewhat complicated, so I added a `compile.sh` script. It will compile into a Windows executable using PyInstaller.  

```
# Edit the settings in keylogger.py and compile.sh (and other files if necessary)
./compile.sh 
# Now you should have keylogger executable (named whatever the compile script specifies; default is Keylogger.exe)
```

## Features

### Network and Email

The keylogger has capability to send logs both using email using `smtplib` as well as over network communication via the `Flask` and `requests` libraries. Specify which to use in the main `keylogger.py` script by changing the `MODE` value to either `Mode.EMAIL` or `Mode.NETWORK`. 

If you're using email, I'll leave how to figure out the SMTP server to you.

If you're sending over network, make sure the 2 machines have network connectivity (obviously), then specify the IP address of the receiver, and as long as the `receiver.py` script is running and the encoding scheme (specified by `ENC_SCHEME` in both files) is the same, you should see folders/files containing the logs being generated.

### Obfuscation

The `obfuscate.py` file contains a slightly enhanced version of the Python obfuscating method seen [here](https://freecodingtools.org/tools/obfuscator/python) (essentially just an iterative version of this).

The operations are essentially just:
1. Zlib compress
2. Base64 encode
3. Reverse the bytes
4. Run it through a lambda so it still executes

If you're curious about how to undo the obfuscator, take a look at the `deobfuscate.py` script.

## Dependency Versions

Since idk how frequently versions of dependencies change, this is the last tested configuration of dependencies & versions that I successfully compiled on.

```
Python 3.12.1

Package                   Version
------------------------- ----------
altgraph                  0.17.4
blinker                   1.9.0
certifi                   2024.12.14
cffi                      1.17.1
charset-normalizer        3.4.1
click                     8.1.8
colorama                  0.4.6
cryptography              44.0.0
Flask                     3.1.0
idna                      3.10
itsdangerous              2.2.0
Jinja2                    3.1.5
MarkupSafe                3.0.2
packaging                 24.2
pefile                    2023.2.7
pillow                    11.1.0
pip                       25.0
pycparser                 2.22
pycryptodome              3.21.0
pyinstaller               6.11.1
pyinstaller-hooks-contrib 2025.0
pynput                    1.7.7
pywin32-ctypes            0.2.3
requests                  2.32.3
setuptools                75.8.0
six                       1.17.0
urllib3                   2.3.0
Werkzeug                  3.1.3
```
