import pwn

from enum import Enum
import json
import itertools

from typing import Optional


class Color(Enum):
    BLACK = "⬛"
    YELLOW = "🟨"
    GREEN = "🟩"

    def __str__(self):
        return str(self.value)


def oracle(iv: bytearray, ciphertext: bytearray) -> list[Color]:
    oracle.count += 1
    data = {"iv": iv.hex(), "ciphertext": ciphertext.hex()}
    conn.sendline(json.dumps(data).encode())
    line = conn.recvline().strip().decode("utf8")
    return [Color(c) for c in line]


oracle.count = 0


# Get answer length
n = 0
while True:
    n += 16
    conn = pwn.process("cbc-dle.py")
    try:
        result = oracle(bytearray(16), bytearray(n))
    except ValueError:
        conn.close()
        continue
    break
print(f"length = {n}")


# Find green and black chars for the first 16 positions
black_values = tuple([] for _ in range(16))
green_value = [0] * n

iv = bytearray(16)
ct = bytearray(n)
for byte_idx in range(16):
    found_green = False
    for val in range(256):
        iv[byte_idx] = val
        res = oracle(iv, ct)
        if res[byte_idx] == Color.BLACK:
            black_values[byte_idx].append(val)
        elif res[byte_idx] == Color.GREEN:
            green_value[byte_idx] = val
            found_green = True
    assert found_green
    assert black_values[byte_idx]
    iv[byte_idx] = black_values[byte_idx][0]


# Find green chars for the other positions
for byte_idx in range(16, n):
    iv = bytearray(16)
    ct = bytearray(n)

    for val in range(256):
        if val in black_values[byte_idx % 16]:
            continue

        ct[byte_idx - 16] = val
        res = oracle(iv, ct)
        if res[byte_idx] == Color.GREEN:
            green_value[byte_idx] = val
            break
    else:
        assert False, byte_idx


# Correlate green chars for the first 16 positions
diff = [0] * 16
for byte_idx in range(1, 16):
    iv = bytearray(black_values[i][0] for i in range(16))
    ct = bytearray(n)
    yellow = list(
        set(range(256)) - set(black_values[byte_idx]) - {green_value[byte_idx]}
    )
    for val in yellow:
        iv[byte_idx] = val
        for val0 in range(256):
            if val0 in black_values[0]:
                continue
            iv[0] = val0
            res = oracle(iv, ct)
            if res[byte_idx] == Color.BLACK:
                diff[byte_idx] = val ^ val0
                break
        else:
            continue
        break
    else:
        assert False, byte_idx
print(f"block ^ (block[0]*16) = {diff}")


# Recover answer ^ first byte
candidates = []
for val0 in range(256):
    candidates.append(
        bytes(
            green_value[byte_idx] ^ val0 ^ diff[byte_idx % 16] for byte_idx in range(n)
        )
    )
print([candidate for candidate in candidates if candidate.startswith(b"EPFL")])

print(f"oracle count = {oracle.count}")
