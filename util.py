from enum import Enum
from Crypto.Cipher import ARC4, AES
from cryptography.fernet import Fernet
import sys

class Mode(Enum):
    NETWORK = 0
    EMAIL = 1

class EncScheme(Enum):
    RC4 = 0
    FERNET = 1
    AES = 2
    XOR = 3

class Encryption:
    def __init__(self, key, enc_scheme):
        self.key = key
        self.enc_scheme = enc_scheme
        match self.enc_scheme:
            case EncScheme.RC4:
                try:
                    self.cipher = ARC4.new(key)
                except Exception as e:
                    print(e)
                    sys.exit()
            case EncScheme.FERNET:
                try:
                    self.cipher = Fernet(key)
                except Exception as e:
                    print(e)
                    sys.exit()
            case EncScheme.AES:
                try:
                    self.cipher = AES.new(key, AES.MODE_EAX, nonce=b'value_to_be_leaked')
                except Exception as e:
                    print(e)
                    sys.exit()
            case _:
                self.cipher = None 

    def encrypt(self, data: bytes):
        """Encrypts data bytes using the configured encryption scheme.

        Args:
            data (bytes): The unencrypted data as Python bytes.

        Returns:
            str: The encrypted hex bytes data in string format (converted using .hex()).
        """
        match self.enc_scheme:
            case EncScheme.RC4 | EncScheme.FERNET | EncScheme.AES:
                encrypted = self.cipher.encrypt(data)
                encrypted = encrypted.hex()
            case EncScheme.XOR:
                key_repeated = (self.key * (len(data) // len(self.key) + 1))[:len(data)]
                encrypted = bytes(a ^ b for a, b in zip(data, key_repeated))
                encrypted = encrypted.hex()
            case _:
                encrypted = None
        return encrypted
    
    def decrypt(self, data: bytes):
        """Decrypts data bytes using the configured encryption scheme.

        Args:
            data (bytes): The encrypted data as a hex bytestring.

        Returns:
            str: The decrypted data in string format.
        """
        match self.enc_scheme:
            case EncScheme.RC4 | EncScheme.FERNET | EncScheme.AES:
                decrypted = self.cipher.decrypt(data)
                decrypted = decrypted.decode()
            case EncScheme.XOR:
                key_repeated = (self.key * (len(data) // len(self.key) + 1))[:len(data)]
                decrypted = bytes(a ^ b for a, b in zip(data, key_repeated))
            case _:
                decrypted = None
        return decrypted