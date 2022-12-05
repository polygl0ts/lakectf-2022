#!/bin/python3

import hashlib
from math import gcd

def get_next(signature):
  return int.from_bytes(signature[:256], 'big'), signature[256:]

# function to find largest coprime divisor
def coprime_divisor(x, y):
    while gcd(x, y) != 1:
        x = x // gcd(x, y)
    return x

p = pow(2, 1024) + 643

with open("my-signature", "rb") as f:
  signature = f.read()

  _, signature = get_next(signature)
  r1, signature = get_next(signature)
  s1, signature = get_next(signature)
  _, signature = get_next(signature)
  r2, signature = get_next(signature)
  s2, signature = get_next(signature)

with open("to-sign", "r") as f:
  m = f.read()

SIZE = len(m) // 2

hm1 = int.from_bytes(hashlib.sha256(m[0: SIZE].encode()).digest(), 'big')
hm2 = int.from_bytes(hashlib.sha256(m[SIZE: 2*SIZE].encode()).digest(), 'big')

num = s1 * hm2 - s2 * hm1
denom = s1 * r2 - s2 * r1

m = coprime_divisor(p - 1, denom)
n = (p - 1) // m

xmodm = pow(denom, -1, m) * num % m
for i in range(n):
  newx = xmodm + i * m
  bytes_val = newx.to_bytes(256, 'big')[-32:]
  if bytes_val[:5] == b"EPFL{" and bytes_val[-1] == ord("}"):
    print(bytes_val)

