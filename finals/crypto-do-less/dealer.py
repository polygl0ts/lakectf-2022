from binascii import hexlify
from player import sign
from Crypto.PublicKey import ECC

privkey = ECC.import_key(open('0/privkey.pem').read())

def deal():
    flagkey = ECC.generate(curve='P-256')
    flagpub = flagkey.public_key()
    flagexp = flagpub.export_key(format='PEM')
    flaghex = hexlify(flagexp.encode()).decode()
    message = flaghex + hexlify(sign(flaghex, privkey)).decode()
    return(message)
