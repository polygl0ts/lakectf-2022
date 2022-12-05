#!/usr/bin/env -S python3.10 -u

import sys
import random as rand
from utils import *
import signal
import time

if len(sys.argv) != 4:
    if len(sys.argv) < 4:
        print("Too few arguments given")
    else:
        print("Too many arguments given")
    print("usage: run.py <node_number> <relays> <flag_path>")
    exit(0)

if not sys.argv[1].isnumeric():
    print(f"{sys.argv[1]} is not a valid node number")
    print("usage: run.py <node_number> <relays> <flag_path>")
    exit(0)


if not sys.argv[2].isnumeric():
    print(f"{sys.argv[2]} is not a valid relay number")
    print("usage: run.py <node_number> <relays> <flag_path>")
    exit(0)

NUM_NODES = int(sys.argv[1])
NUM_RELAY = int(sys.argv[2])

res_path = list(range(NUM_NODES))
rand.shuffle(res_path)
#print(res_path)
routing = generate_routing(res_path)

src = res_path[0]
relays = sorted(
    rand.sample(
        res_path[int(NUM_NODES*0.1):int(NUM_NODES*0.9)], 
        k=NUM_RELAY))



print(f"We have {NUM_NODES} nodes playing")
print(f"Start is {src}, other routers are {nodes_to_string(relays)}")

def timeout(sig, frame):
    sys.stdout.flush()
    print("\nTime exceeded. The nodes got bored")
    exit(0)


signal.alarm(61)
signal.signal(signal.SIGALRM, timeout)


while True:
    given_tos = input("\nNext hops: ").split()

    if len(given_tos) != NUM_RELAY + 1:
        print(f"Need {NUM_RELAY+1} next hops, 1 for the start and 1 for each of the routers")
        continue

    if not all(map(str.isnumeric, given_tos)):
        print(f"Unvalid hops given")
        continue
        
    tos = list(map(lambda x: x% NUM_NODES, map(int,given_tos)))
    #assert len(res_path) == len(routing) 
    path = explore_paths([src] + relays, tos, routing)
    print("path: ", nodes_to_string(path))
    if(len(path) == NUM_NODES + 1 and path[0]==path[-1]):
        print("Well done")
        with open(sys.argv[3], 'r') as f:
            print(f.read())
        exit(0)
    time.sleep(1)
