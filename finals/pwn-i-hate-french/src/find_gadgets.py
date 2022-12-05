from pwn import *

context.arch = "amd64"
for reg in ["rax" ,"rbx" ,"rcx" ,"rdx" ,"rsi" ,"rdi" ,"rbp" ,"rsp" ,"r8 " ,"r9 " ,"r10" ,"r11" ,"r12" ,"r13" ,"r14" ,"r15"]:
    string = "pop " + reg + "; ret"
    print(string)
    code = asm(string) + b"\x83"
    print(enhex(code))
    # print(code.decode('utf-8'))
    open("out", "wb").write(code)
    os.system("cat out")
    print()
