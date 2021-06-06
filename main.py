"""
Jawad Taj
2021-06-06
This script put's an encrypted text on a qrcode that can be decrypted with a password
This is useful for bitcoin paper backup when storing the 12-words
This script was inspired by sunknudsen qr-backup: https://github.com/sunknudsen/qr-backup
"""
import sys
import base64
import qrcode
import cv2
from pyzbar.pyzbar import decode
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptQr:
    def __init__(self, message, passwd):
        salt = b'\xfd\xf1\xc4\xb0\xa9\x05*U\xda{wPj\x94d\x90'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        self.passwd = passwd
        self.message = message.encode()
        self.key = base64.urlsafe_b64encode(kdf.derive(self.passwd.encode()))

    # Encrypts messages and put's it in a qrcode
    def encrypt(self):
        f = Fernet(self.key)
        encrypt_message = f.encrypt(self.message)
        img = qrcode.make(encrypt_message)
        img.save("QRCode.png")

    # Read's qrcode and decrypt the message
    def decrypt(self):
        f = Fernet(self.key)
        img = cv2.imread("QRCode.png")
        # Checks if file exist
        if img is None:
            print("File 'QRCode.png' can't be found")
            return

        message = decode(img)[0][0].decode()  # Grabs the data from the qrcode
        # Checks if password is right
        try:
            decrypt_message = f.decrypt(message.encode())
            print(decrypt_message.decode())
        except InvalidToken:
            print("Invalid Password")


if __name__ == '__main__':
    num = ""
    while num != '0' and num != '1':
        num = input("Do you what to encrypt[0] or decrypt[1]: ")

    if num == "0":
        word = input("Enter The Word That You What Encrypt: ")
        password = input("Password: ")
        enc = EncryptQr(word, password)
        enc.encrypt()
        print(f"The Qrcode is saved in {sys.path[0]}\QRCode.png")
    elif num == "1":
        password = input("Password: ")
        enc = EncryptQr('none', password)
        enc.decrypt()
