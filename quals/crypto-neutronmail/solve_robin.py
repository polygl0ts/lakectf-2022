import pgpy # pip install pgpy
from pgpy.packet.types import MPI
import subprocess, requests, copy
from math import gcd

def fetch_key(addr):
    subprocess.check_output(f"gpg2 --locate-keys --auto-key-locate clear,nodefault,wkd {addr}", shell=True)
    return subprocess.check_output(f"gpg2 --armor --export {addr}", shell=True)

k1 = list((K1 := pgpy.PGPKey.from_blob(fetch_key("epfl-ctf-admin2@protonmail.com"))[0]).subkeys.values())[0]
k2 = list(pgpy.PGPKey.from_blob(fetch_key("epfl-ctf-admin@protonmail.com"))[0].subkeys.values())[0]
n = k1._key.keymaterial.n
e = k1._key.keymaterial.e
p = gcd(n, k2._key.keymaterial.n)
q = n // p
d = pow(e, -1, (p - 1) * (q - 1))

k = pgpy.PGPKey.new(pgpy.constants.PubKeyAlgorithm.RSAEncryptOrSign, 2048, k1.created)
k._key.keymaterial.__dict__ |= {
        "n": MPI(n),
        "e": MPI(e),
        "p": MPI(p),
        "q": MPI(q),
        "d": MPI(d),
        "u": MPI(pow(p, -1, q)),
        }
k._key.keymaterial._compute_chksum()
k._key.update_hlen()
k.add_uid(K1.userids[0])
msg = pgpy.PGPMessage.from_file("challenge/flag.eml")
try:
    print(k.decrypt(msg).message)
except:
    print("No decrypt")
