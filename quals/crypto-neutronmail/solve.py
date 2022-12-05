#!/usr/bin/env python3

# pip install PyCryptodome pgpdump
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Util.number import GCD
import pgpdump
import requests
import os

def get_public_key(email):
    data = requests.get("https://api.protonmail.ch/pks/lookup",
        params={"op": "get", "search": email}
    ).content
    dump = pgpdump.AsciiData(data)
    packets = list(dump.packets())
    pk = packets[0]
    sub_pk = packets[3] # message is encrypted with the subkey
    return sub_pk.modulus, sub_pk.exponent

n, e = get_public_key("epfl-ctf-admin2@protonmail.com")
n2, e2 = get_public_key("epfl-ctf-admin@protonmail.com")
# Compare keys
assert n != n2 and GCD(n, n2) != 1, "No common factor"

p=GCD(n, n2)
q=n//p

phi = (p-1)*(q-1)
d = pow(e, -1, phi)

# Get Encrypted Session Key
with open('challenge/flag.eml', 'rb') as file:
    content = file.read()

pgp_message = content[content.find(b'-----BEGIN PGP MESSAGE-----'):]
data = pgpdump.AsciiData(pgp_message)
# Remove the first 12 bytes (2B length + 1B version + 8B keyId + 1B PK algo)
c = data.packets().__next__().data[12:]

key = RSA.construct((n, e, d, p, q))
cipher = PKCS1_v1_5.new(key)

m = cipher.decrypt(c, None)
# First byte to specify the algorithm
# Last 2 bytes are for checksum
# Bytes in between are for the key of the symmetric cipher

print("Algorithm:", m[0]) 
# https://www.iana.org/assignments/pgp-parameters/pgp-parameters.xhtml#pgp-parameters-13
# 9 => AES256

sym_key = m[1:-2]
print("Symmetric key:", sym_key.hex())

# Now we can use gpg to decrypt the symmetric cipher
os.system(f"gpg --override-session-key '{m[0]}:{sym_key.hex()}' --decrypt challenge/flag.eml")
