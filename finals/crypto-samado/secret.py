from Crypto.Util.number import *
from random import *

FLAG = b'\\.....:::::::::::::::::::: the flag is: EPFL{l1n3Ar_C0m8iN47Ion_iN_EXP_1Z_cLu3??!} ::::::::::::::::::::...../'

def aux_blackbox(coef, m, p, q):
    m1, m2 = coef
    c1, c2 = pow(m1, 65537, p*q), pow(m2, 65537, p*q)
    # c1 + c2*m ≡ r + s*m (mod phi)
    # s = (c1 + c2*m - r) / m
    phi = (p - 1) * (q - 1)
    d = pow(65537, -1, phi)
    r = randint(1, phi)
    s = (pow(m, -1, phi) * (c1 - r) + c2) % phi
    assert (c1 + c2 * m) % phi == (r + s * m) % phi
    return (pow(r, d, p*q), pow(s, d, p*q))
