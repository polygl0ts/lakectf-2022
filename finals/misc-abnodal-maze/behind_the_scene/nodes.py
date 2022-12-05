import random as rand
from collections import Counter
import sys 
from utils import *
#NUM_NODES = 50000
NUM_NODES = 400
if len(sys.argv) == 2:
    NUM_NODES = int(sys.argv[1])


res_path = list(range(NUM_NODES))

rand.shuffle(res_path)
#print("res path",res_path)
 
# from + idx = to <=> idx = to - from
routing = generate_routing(res_path)
#print("routing", routing)
count = Counter()
src = res_path[0]
"""
for to in range(NUM_NODES):

    #if res_path[0] != src or res_path[1] != to:
    #    continue
    path = explore_path(src, to, routing)
    #if res_path[0] == src and res_path[1] == to:
    #    print("res try", path)
    count[len(path)]+=1
    #if len(path) > NUM_NODES :
        #print(f"Found {len(path)} path {path}")
"""
#new_routing = routing[:src] + [0] + routing[src:]
#print(src,len(new_routing), new_routing)
print(res_path)
for src_ix in range(int(NUM_NODES*0.1),int(NUM_NODES*0.9)):
    src1 = res_path[src_ix]
    if src1==src:
        continue
    count.clear()
    for to in range(NUM_NODES):
        if src1 not in explore_path(src, to, routing):
            print(f"All src {src} to {to} (does not reach) src1 {src1} path: {explore_path(src, to, routing)}")
            continue
        for to1 in range(NUM_NODES):


    #if res_path[0] != src or res_path[1] != to:
    #    continue
            path = explore_paths([src,src1], [to, to1], routing)
            print(f"src {src} to {to} src1 {src1} to1 {to1} path: {path}")
    #if res_path[0] == src and res_path[1] == to:
    #    print("res try", path)
            count[len(path)]+=1
    #if len(path) > NUM_NODES :
        #print(f"Found {len(path)} path {path}")
    #print(count.most_common())
    print("src1", src1, "solutions", count[NUM_NODES + 1])

"""

for i in range(NUM_NODES+1):
    if count.count(i)>0:
        print(f"{i}:{count.count(i)}")
"""



