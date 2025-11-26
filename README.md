# QRCode Encrypted Backup

## Use
The main uses for this script is to encrypt bitcoin.
This is useful for bitcoin paper backup when storing the 12-words phrase.
This is more secure because your 12-word phrase isn't in plain text.


## Features
- Encrypt sentences with password
- Sends encrypted sentences to a qrcode
- Can decrypt qrcode sentences with password


## Build
```
git clone https://github.com/gun4qmm7h/QRCode-Backup.git
cd QRCode-Backup
pip3 install -r requirement.txt
```
Once you run all the commands, run main.py

## Use for quick testing
`"python3 main.py -e -w 'this is a test' -p password"`

`"python3 main.py -de -p password"`


## Inspiration

This script was inspired by sunknudsen project: [qr-backup](https://github.com/sunknudsen/qr-backup)
