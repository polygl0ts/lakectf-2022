from pwn import *
from player import *

context.log_level = 'ERROR'

rounds = 4 + 4

p = Player(4)

test = False
REMOTE = True
HOST = "chall.polygl0ts.ch"
PORT = 4800


def interact(proc, readround, writeround, inp):
    res = ""
    for i in range (1, rounds):
        if readround==i:
            res = proc.recvuntil(("\nround " + str(i)+" input :\n").encode())[:-len("\nround " + str(i)+" input :\n")]
        else:
            proc.recvuntil(("\nround " + str(i)+" input :\n").encode())
        if(writeround == i):
            proc.sendline(inp.encode())
        else:
            proc.sendline("".encode())
    return(res)

def flag(proc, writeround, inp, voteround, vote, flaground, flagstr):
    res = ""
    for i in range (1, rounds):
        proc.recvuntil(("\nround " + str(i)+" input :\n").encode())
        if(writeround == i):
            proc.sendline(inp.encode())
        elif(voteround == i):
            proc.sendline(vote.encode())
        elif(flaground == i):
            proc.sendline(flagstr.encode())
        else:
            proc.sendline("".encode())
    res = proc.recv().decode()
    return(res)


#get message with 1 foreign signature
if REMOTE:
    p1 = remote(HOST,PORT)
else: 
    p1 = process(["python3", "server.py"])
m = interact(p1,2,0,"").decode()
ml = 129+482
m1 = m[(-ml):]

if(test):
    print("message 1")
    print(m1)

m1 = p.send_to_all(m1)

#get message with 2 foreign signatures
if REMOTE:
    p2 = remote(HOST,PORT)
else: 
    p2 = process(["python3", "server.py"])
m = interact(p2,3,1,m1).decode()
ml = 129+129+482
m2 = m[-2*ml:-ml]

if(test):
    print("message 2")
    print(m2)

m2 = p.send_to_all(m2)

#get message with 3 foreign signatures
if REMOTE:
    p3 = remote(HOST,PORT)
else: 
    p3 = process(["python3", "server.py"])
m = interact(p3,4,2,m2).decode()
ml = 129+129+129+482
m3 = m[-3*ml:-2*ml]

if(test):
    print("message 3")
    print(m3)

def get_length(l):
    ls = str(l)
    while (len(ls)<4):
        ls = "0"+ls
    return(ls)

#get flag
m = m3 + "4"
s = hexlify(sign(m,p.privkey)).decode()
msg = m + s
msg = get_length(len(msg))+"000000000000"+ msg
v = "40"
s2 = hexlify(sign(v,p.privkey)).decode()
vote = v + s2
vote = p.send_to_all(vote)
f = "flag"
s3 = hexlify(sign(f,p.privkey)).decode()
flagstr = f+s3
flagstr = p.send_to_all(flagstr)

if REMOTE:
    p4 = remote(HOST,PORT)
else: 
    p4 = process(["python3", "server.py"])
m = flag(p4,4,msg,5,vote,6,flagstr)
foundflag = m[1:-1]+p.flag
assert(foundflag == "EPFL{D0l3v-5tR0ng_Bu7_reP1ay3d?_0r_84d_v07E5?_Wh0_know5_!t?}")
print(foundflag)



