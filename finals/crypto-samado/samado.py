#!/usr/local/bin/python3

from random import *
from Crypto.Util.number import *
from gensafeprime import *
import sys
from secret import aux_blackbox, FLAG

def gen_key(nbit):
    g, p, q = 2, generate(nbit), generate(nbit)
    while True:
        if {pow(g, (p - 1) // 2, p), pow(g, (q - 1) // 2, q)} == {p - 1, q - 1}:
            break
        else:
            g += 1
    return g, p, q

def encrypt(coef, flag, pubkey):
    m1, m2 = coef
    g, n = pubkey
    y = pow(g, flag, n)
    c1, c2 = pow(m1, 65537, n), pow(m2, 65537, n)
    c = m1 * m2 * pow(g, c1, n) * pow(y, c2, n) % n
    return (c1, c2, c)

def main():
    border = "|"
    pr(border*72)
    pr(border, " Welcome to SAMADO Cryptography task, your mission is solve a modern", border)
    pr(border, " DLP problem in artificial - NOT REAL - mysterious crypto world!    ", border)
    pr(border*72)
    nbit = 512
    flag = bytes_to_long(FLAG)
    g, p, q = gen_key(nbit)
    n = p * q
    assert flag <= (p - 1) * (q - 1) // 2

    while True:
        pr("| Options: \n|\t[E]ncrypted flag! \n|\t[P]ublic parameters \n|\t[Q]uit")
        ans = sc().lower()
        if ans == 'e':
            try:
                pr(border, 'Send coefficients like m1, m2:')
                _coef = [int(_) for _ in sc().split(',')]
            except:
                die(border, 'Given coefficients are invalid!')
            COEFS = [_coef]
            try:
                COEFS.append(aux_blackbox(_coef, flag, p, q)) # Black-Box function imported from secret
            except:
                pass
            for _ in COEFS:
                enc = encrypt(_, flag, (g, n))
                pr(border, f'enc = {enc}')
        elif ans == 'p':
            pr(border, f'g = {g}')
            pr(border, f'n = {n}')
            pr(border, f'c = {encrypt((1*p + 3*q, 3*p - 7*q), 186313517718920421010947985890084109860212960834061115512313701935025645375, (g, n))}')
        elif ans == 'q':
            die(border, "Quitting ...")
        else:
            die(border, "Bye ...")

def die(*args):
    pr(*args)
    quit()

def pr(*args):
    s = " ".join(map(str, args))
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

def sc():
    return sys.stdin.readline().strip()

if __name__ == '__main__':
    main()
