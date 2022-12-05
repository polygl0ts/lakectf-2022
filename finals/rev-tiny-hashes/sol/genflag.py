#!/usr/bin/env python
import json
import random
import pprint

KR1 = 0
KR2 = 1
DJB = 2
from kr1 import kr1
from kr2 import kr2
from djb import djb

flag = "EPFL{9O774_lOvE_7hO5e_CU7E_H45He2}"

hashes = []

hashes.extend([[KR1, i, *v] for i,v in enumerate(kr1)])
hashes.extend([[KR2, i, *v] for i,v in enumerate(kr2)])
hashes.extend([[DJB, i, *v] for i,v in enumerate(djb)])

random.seed(1337)
entries = []
for c in flag:
    random.shuffle(hashes)
    found = False
    for hid, i, h, v, ch in hashes:
        if c == ch:
            found = True
            entries.append((hid, i, h, v, ch))
            break
    assert found, f"Cannot find {c}"

# pprint.pprint(entries)

for hid, idx, _, _, _ in entries:
    print(f"{{{hid}, {idx}}},")
