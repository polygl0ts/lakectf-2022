#!/usr/bin/env python

#!/usr/bin/env python3
import random as rand

def explore_path(source:int, to:int, routing:list[int])->list[int]:
    return explore_paths([source], [to], routing)

def explore_paths(sources: list[int], tos:list[int], routing:list[int])->list[int]:
    res = [sources[0]]
    visited = {sources[0]}
    dst = tos[0]
    src = sources[0]
    i = 1
    while dst not in visited:
        visited.add(dst)
        #src = dst
        if dst in sources:
            src, dst = dst, tos[i]
            i+=1
        else:
            src, dst = dst, (routing[dst] + src) % len(routing)
        res.append(src)
    res.append(dst)
    return res

def nodes_to_string(path:list[int]) -> str:
    return ', '.join(map(str,path))

def generate_routing(res_path:list[int])-> list[int]:
    num_nodes = len(res_path)
    routing = [0] * num_nodes
    for i in range(num_nodes):
        routing[res_path[i]] = (res_path[(i+1)%num_nodes] - res_path[(i-1)%num_nodes])%num_nodes
    return routing
