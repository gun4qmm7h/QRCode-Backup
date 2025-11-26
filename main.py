"""
Jawad Taj
"""
import cv2
import sys
import base64
import qrcode
from argparse import ArgumentParser, Namespace
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
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
        print(f"The Qrcode is saved in {sys.path[0]}/QRCode.png")
        img.save("QRCode.png")

    # Read's qrcode and decrypt the message
    def decrypt(self):
        f = Fernet(self.key)
        img = cv2.imread("QRCode.png")
        # Checks if file exist
        if img is None:
            print("File 'QRCode.png' can't be found")
            return

        detector = cv2.QRCodeDetector()
        message, points, _ = detector.detectAndDecode(img) # Grabs the data from the qrcode

        # Checks if password is right
        try:
            decrypt_message = f.decrypt(message.encode())
            print(decrypt_message.decode())
        except InvalidToken:
            raise ValueError("Invalid Password")


if sys.stdout.isatty(): # check if you are running from terminal (debugging)
    if __name__ == '__main__':
        parser = ArgumentParser()

        parser.add_argument("-w", "--Word", help="Message that will get encrypted")
        parser.add_argument("-p", "--Password", required=True, help="Password to encrypted message")
        parser.add_argument('-e', '--Encrypted', action='store_true', help="Encrypted the info you give")
        parser.add_argument('-de', '--DeEncrypted', action='store_true', help="DeEncrypted the info you give")

        args: Namespace = parser.parse_args()

        if args.Encrypted:
            if args.Word is None:
                raise ValueError("Word are what is being Encrypting, Don't leave blank")
            enc = EncryptQr(args.Word, args.Password)
            enc.encrypt()
        elif args.DeEncrypted:
            enc = EncryptQr('none', args.Password)
            enc.decrypt()

else:
    if __name__ == '__main__':
        num = ""
        while num != '0' and num != '1':
            num = input("Do you what to encrypt[0] or decrypt[1]: ")

        if num == "0":
            word = input("Enter The Word That You What Encrypt: ")
            password = input("Please Note If You Lose The Password The Data Can't Be Recovered\nPassword: ")
            enc = EncryptQr(word, password)
            enc.encrypt()
        elif num == "1":
            password = input("Password: ")
            enc = EncryptQr('none', password)
            enc.decrypt()


