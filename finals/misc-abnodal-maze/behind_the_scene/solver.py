#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 9999
from pwn import *
import re
import random as rand

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = 'python'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'chall.polygl0ts.ch'#'localhost'
port = int(args.PORT or 5600)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, shell=True,  *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return process(['python', 'run.py', '20', '1', 'flag_lv0.txt'])#start()

    else:
        return start_remote(argv, *a, **kw)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def generate_routing(path:list[int]):
    for i,n in enumerate(path):
        if n not in relays and i < len(path)-1:
            #log.info(f"n {n} i {i} path {path}")
            # src + x = dst <=> x = dst - src
            if routing[n] == 0:
                routing[n] =(path[(i+1)] - path[(i-1)])%num_nodes
            else:
                assert routing[n] ==(path[(i+1)] - path[(i-1)])%num_nodes


#io = process(['python', 'run.py', '20', '1', 'flag_lv0.txt'])#start()
io = start()
num=2
first = io.recvline()
#print(first)
num_nodes = int(re.findall(rb'\b\d+\b',first)[0])
routing = [0]*num_nodes
#log.info(f"")
log.info(f"num_nodes {num_nodes}" )
second = io.recvline()
relays =  [int(e) for e in re.findall(rb'\b\d+\b',second)]
#print(second) 
#log.info(f"relays {relays}")
src = relays[0]

def generate_explore_args():
    unknowns = [i for i,x in enumerate(routing) if x==0 and i not in relays]
    if len(unknowns)< len(relays):
        return unknowns + [unknowns[0]] * (len(relays) - len(unknowns))
    else:
        return unknowns[:len(relays)]

def unknowns_exist():
    unknowns = [i for i,x in enumerate(routing) if x==0 and i not in relays]
    return len(unknowns)!=0

def find_path(visited = {src}, frm = src, args = []) -> list[int]| None:
    """Find direction to create full path"""
    
    #log.info(f"v {visited}, frm {frm}, args {args}")
    for i in range(num_nodes):
        if i in visited:
            pass
        exp = explore_until_relay(frm, i, visited)
        if exp != None:
            # Got to relay
            dst, v = exp
            # dst next relay, v is visited
            if dst == src:
                if len(v) >= num_nodes:
                    # if we have gotten to src, are we finished
                    #log.info(f"v {v},dst {dst} args {args} i {i}")
                    return args + [i]
            elif dst in v:
                # we have already passed by non source relay
                pass
            else:
                c = v.copy()
                c.add(dst)
                path = find_path(c, dst, args + [i])
                if path != None:
                    return path

    return None


def explore_until_relay(frm:int, to:int, visited:set[int]):
    """"""
    assert frm in relays
    dst = to 
    v = visited.copy()
    while dst not in v and dst not in relays:
        v.add(dst)
        frm, dst = dst, (routing[dst] + frm) % len(routing)

    if dst in relays:
        return dst, v
    else:
        return None


"""
def compute_path_len(directions)->int:
    res = [sources[0]]
    visited = {sources[0]}
    dst = tos[0]
    src = sources[0]
    while dst not in visited:
        visited.add(dst)
        #src = dst
        if dst in sources:
            src, dst = dst, tos[sources.index(dst)]
        else:
            src, dst = dst, (routing[dst] + src) % len(routing)
        res.append(src)
    res.append(dst)
    return len(res)
"""

def args_to_str(args: list[int]) -> bytes:
    return " ".join([str(i) for i in args]).encode()

def send(num=3):
    if unknowns_exist():
        args = generate_explore_args()
        if num==3:
            io.sendline(args_to_str(args))
        return False
    else:
        #log.info(f"routing {routing}")
        args = find_path()
        #log.info(f"path found {args}")
        if args == None:
            raise ValueError
        if num == 3:
            log.info(f"path {args}")
            io.sendline(args_to_str(args))
        log.info(f"Tries: {tries}")
        #io.interactive()
        return True
        
        
        
    # find arguments
    # is there a path to flag?
    # if no explore as much as possible
    
tries = 0
while True:
    tries += 1
    io.recvuntil(b"Next hops: ")
    if send():
        break
    
    path = io.recvline()
    #print(path)
    #print(path[:5] == b"path:")
    path = [int(i.strip()) for i in path[5:].split(b",")]
    #log.info(f"path {path}")
    generate_routing(path)
    """
    if num==2:
        #pylance being a pain, see https://github.com/microsoft/python-type-stubs/issues/203

        io.sendline(b"23 23 23")

    # shellcode = asm(shellcraft.sh())
    # payload = fit({
    #     32: 0xdeadbeef,
    #     'iaaa': [1, 2, 'Hello', 3]
    # }, length=128)
    # io.send(payload)
    # flag = io.recv(...)
    # log.success(flag)
    """
    log.info(f"Tries: {tries}")
#all_tries.append(tries)
io.interactive()

#print(f"all tries {all_tries}")
