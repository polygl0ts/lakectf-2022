#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *
from math import gcd
io = process(['python', '-u', 'samado.py'])

io.sendline(b"p")
io.recvuntil(b"g = ")
g = int(io.recvline())
io.recvuntil(b"n = ")
n = int(io.recvline())
io.recvuntil(b"c = ")
cheat = eval(io.recvline())

io.sendline(b"e\n1, 1")
io.recvuntil(b"enc = ")
e1 = eval(io.recvline())
io.recvuntil(b"enc = ")
e2 = eval(io.recvline())

io.sendline(b"q")
io.close()

p = gcd(n, pow(7, 65537, n) * cheat[0] + pow(3, 65537, n) * cheat[1])
q = n // p

phi = (p - 1) * (q - 1)
d = pow(65537, -1, phi)
m1 = pow(e2[0], d, n)
m2 = pow(e2[1], d, n)
assert (e2[2] * pow(m1 * m2, -1, n)) % n == e1[2]
# c1 + c2 * flag = c11 + c21 * flag
# flag = (c1 - 1) / (c2 - 1)
phi //= 4 # Hack to get around lack of invertibility, lol
print(long_to_bytes((1 - e2[0]) * pow(e2[1] - 1, -1, phi) % phi).decode())
