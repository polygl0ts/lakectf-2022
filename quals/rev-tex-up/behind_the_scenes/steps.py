from pickle import FALSE
import utils
import random
def step(n:int):
    if n%2==0:
        return n//2
    else:
        return 3*n + 1

def reverse_step(n:int, even = True):
    #print(f"Reverse for {n} with even: {even}")
    if even:
        return 2*n
    else:
        n -= 1
        if n % 3 != 0:
            return -1
        else:
            if (n // 3) % 2 == 0:
                return -1
            return n // 3


def print_steps(n:int):
    if n<1:
        return
    i = 0
    print("%2d %9d"% (i,n))
    while n!=1:
        n = step(n)
        i+=1
        print("%2d %9d"% (i,n))

def get_steps(n):
    if n<1:
        return -1
    i = 0
    while n!=1:
        n = step(n)
        i+=1
    return i

def limit(n, limit, upper = True):
    if n<1:
        return False
    
    while n!=1:
        n = step(n)
        if upper and n > limit:
            return  False
        elif not upper and n < limit:
            return False
    return True

def is_num_key(i, target_steps = 13):
    return get_steps(i) > target_steps and limit(i,i)

def find_num_key(target_steps = 13):
    for i in range(100):
        if is_num_key(i, target_steps):
            print(i)
            print()

# step: is_even
path = {1: True, 6: False, 10: False, 12: True, 13: True, 14: True, 15: True, 18: True, 34: True, 42: False}


def find_num(start=52, start_step=47):
    def explore(i, n):
        #print("i:",i,'n:',n)
        if n < start or n > 2147483647:
            return -1
        if i == 0:
            return n

        if i-1 in path:
            #Choice is fixed
            next = reverse_step(n, path[i-1])
            if next == -1:
                return -1
            else:
                return explore(i-1, next)
        else:
            choice = random.choice([True, False])
            res = -1
            next = reverse_step(n, choice)

            if next != -1:
                res = explore(i-1, next)
                if res != -1:
                    # Found valid result
                    return res
            
            not_next = reverse_step(n, not choice)
            if not_next != -1:
                res = explore(i-1, not_next)
            return res

    return explore(start_step, start)
#print(find_num())

def really_find_num(key_steps=9):
    res = []
    for i in range(1,10000):
        if is_num_key(i,key_steps):
            find = find_num(i)
            if find != -1:
                res += [(find,i)]
    return res
really_find_num()

