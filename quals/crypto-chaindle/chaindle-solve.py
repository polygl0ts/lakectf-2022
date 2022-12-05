#!/usr/bin/python3
"""
Remote: $ ./chaindle-solve.py --connection-info "nc 127.0.0.1 5000"
Local: $ ./chaindle-solve.py
"""

from Crypto.Cipher import AES
import pwn

from enum import Enum
from hashlib import sha256
import itertools
import json
import string
import sys


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
    # print(conn.recvline().strip())
    # print(conn.recvline().strip())
    line = conn.recvline().strip().decode("utf8")
    return [Color(c) for c in json.loads(line)["result"]]


def print_recovered_positions(green_value):
    is_recovered = "".join("x."[v is not None] for v in green_value)
    for i in range(0, 64, 16):
        print(f"{is_recovered[i:i+8]} {is_recovered[i+8:i+16]}")


oracle.count = 0
n = 64

if len(sys.argv) >= 3 and sys.argv[1] == "--connection-info":
    _, host, port = sys.argv[2].split()
    conn = pwn.remote(host, port)
else:
    conn = pwn.process(["python3", "chaindle.py"])


# Find green and black chars for the first 16 positions
black_values = tuple(set() for _ in range(16))
non_black_values = tuple(set() for _ in range(16))
green_value = [None] * n

iv = bytearray(16)
ct = bytearray(n)
for val in range(128):
    val2 = val + 128
    iv = bytearray([val] * 16)
    ct[16:32] = bytearray([val2] * 16)
    res = oracle(iv, ct)
    for byte_idx in itertools.chain(range(16), range(32, 48)):
        v = val if byte_idx < 16 else val2
        if res[byte_idx] == Color.BLACK:
            black_values[byte_idx % 16].add(v)
        else:
            non_black_values[byte_idx % 16].add(v)
            if res[byte_idx] == Color.GREEN:
                green_value[byte_idx] = v

# print(
#     len([v for v in green_value[:16] if v]),
#     len([v for v in green_value[32: 48] if v]),
# )
base_idx = None
for i in range(16):
    assert black_values[i] | non_black_values[i] == set(range(256)), i
    if len(non_black_values[i]) == n:
        base_idx = i
    print(i, len(non_black_values[i]), green_value[i], green_value[i + 32])
print(f"base_idx = {base_idx}")
assert base_idx is not None


diff = [None] * 16
diff[base_idx] = 0
non_black_values_0 = non_black_values[base_idx]
for byte_idx in range(16):
    if byte_idx == base_idx:
        continue
    if len(non_black_values[byte_idx]) == 1:
        continue
    diff_candidates = []
    for diff_val in range(256):
        mapped_non_black_values = {v ^ diff_val for v in non_black_values[byte_idx]}
        set_diff_size = len(mapped_non_black_values ^ non_black_values_0)
        if mapped_non_black_values.issubset(non_black_values_0):
            diff_candidates.append(diff_val)
            print(byte_idx, diff_val, set_diff_size)
    assert len(diff_candidates) == 1, diff_candidates
    diff[byte_idx] = diff_candidates[0]
print(f"diff = {diff}")
# input()


for val in non_black_values[base_idx]:
    block = bytearray(16)
    for i in range(16):
        block[i] = val
        if diff[i % 16] is not None:
            block[i] ^= diff[i % 16]
    iv = bytearray(16)
    ct = bytearray(n)
    ct[:16] = ct[32:48] = block
    res = oracle(iv, ct)
    for i in itertools.chain(range(16, 32), range(48, 64)):
        if res[i] == Color.GREEN:
            green_value[i] = block[i % 16]
print(f"green_value = {green_value}")
print_recovered_positions(green_value)


chars = set(string.ascii_letters + string.digits + "+/")
good_base_vals = []
for val in range(256):
    candidate = bytearray(n)
    for i in range(n):
        if green_value[i] is not None and diff[i % 16] is not None:
            candidate[i] = green_value[i] ^ diff[i % 16] ^ val
    non_zero_chars = set(chr(b) for b in candidate if b)
    # print(val, non_zero_chars)
    if non_zero_chars.issubset(chars):
        good_base_vals.append(val)
        print(val, len(non_zero_chars), candidate)
assert len(good_base_vals) == 1, good_base_vals
e0_block = [None if v is None else v ^ good_base_vals[0] for v in diff]
print(f"e0_block = {e0_block}")
# input()

remaining_chars = chars - set(
    chr(v ^ e0_block[i % 16])
    for i, v in enumerate(green_value)
    if v is not None and e0_block[i % 16] is not None
)
print(f"remaining chars = {remaining_chars}")
print(f"num remaining chars = {len(remaining_chars)}")
for _, char in zip(range(16), remaining_chars):
    # for val in non_black_values[base_idx]:
    block = bytearray(16)
    for i in range(16):
        block[i] = ord(char)
        if e0_block[i % 16] is not None:
            block[i] ^= e0_block[i % 16]
        # block[i] = val
        # if diff[i % 16] is not None:
        #    block[i] ^= diff[i % 16]
    iv = block
    ct = bytearray(n)
    ct[16:32] = block
    res = oracle(iv, ct)
    for i in itertools.chain(range(16), range(32, 48)):
        # print(i, res[i], res[i] == Color.GREEN)
        if res[i] == Color.GREEN and e0_block[i % 16] is not None:
            green_value[i] = block[i % 16]  # ^ e0_block[i % 16]
print(f"green_value = {green_value}")
print_recovered_positions(green_value)

print(f"oracle.count = {oracle.count}")
while oracle.count < 256:
    oracle(bytearray(16), bytearray(64))

assert oracle.count == 256, oracle.count


flag_enc = eval(conn.recvline())
print(f"flag_enc = {flag_enc}")
print(f"flag_enc = {flag_enc.hex()}")

if True:
    answer = bytearray(n)
    remaining_chars = chars.copy()
    remaining_idx = list(range(n))
    for i, v in enumerate(green_value):
        if v is not None and e0_block[i % 16] is not None:
            val = v ^ e0_block[i % 16]
            answer[i] = val
            remaining_chars.remove(chr(val))
            remaining_idx.remove(i)
    print(f"answer = {answer}")
    print(f"num_remaining_chars = {len(remaining_chars)}")
    print(f"remaining_idx = {remaining_idx}")
    cnt = 0
    for permutation in itertools.permutations(remaining_chars):
        cnt += 1
        if (cnt & 0xFFFF) == 0:
            print(f"checkpont {hex(cnt)}")
        for i, v in zip(remaining_idx, permutation):
            answer[i] = ord(v)
        key = sha256(answer).digest()
        flag = AES.new(key, AES.MODE_ECB).decrypt(flag_enc)
        if flag.startswith(b"EPFL"):
            print(answer)
            print(flag)
            break

    print(f"oracle count = {oracle.count}")
    exit()
