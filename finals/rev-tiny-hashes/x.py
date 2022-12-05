#!/usr/bin/env python
import sys
import os
from pwn import *
from struct import pack

context.update(arch='aarch64', os='linux')

### CONVENIENCE FUNCTIONS ###
convert = lambda x                  :x if type(x)==bytes else str(x).encode()
s       = lambda data               :io.send(convert(data))
sl      = lambda data               :io.sendline(convert(data))
sla     = lambda delim,data         :io.sendlineafter(convert(delim), convert(data), timeout=context.timeout)
ru      = lambda delims, drop=True  :io.recvuntil(delims, drop, timeout=context.timeout)
uu32    = lambda data               :u32(data.ljust(4, b'\x00'))
uu64    = lambda data               :u64(data.ljust(8, b'\x00'))

### SETUP ###
RHOST = "127.0.0.1"
RPORT = 2020

context.terminal = ['tmux', 'splitw', '-h']

### SPLOIT ###

def main():
    # import ipdb; ipdb.set_trace()
    kr1 = 3*asm("nop") + asm("add     w0, w1, w0")
    assert(len(kr1) == 4*4)
    s(kr1)

    log.info(ru(b"CLEARED\n"))

    kr2 = asm("""
    mov     w2, w0
    lsl     w0, w0, #5
    sub     w0, w0, w2
    add     w0, w1, w0
    """)
    assert(len(kr2) == 4*4)
    s(kr2)
    log.info(ru(b"CLEARED\n"))

    djb = asm("""
    mov w2, w0
    lsl w0, w0, #5
    add w0, w0, w2
    add w0, w0, w1
    """)
    assert(len(djb) == 4*4)
    s(djb)
    log.info(ru(b"CLEARED\n"))

    io.interactive()


if __name__ == "__main__":
    args.NOPTRACE = True
    io = remote(RHOST, RPORT)
    main()
