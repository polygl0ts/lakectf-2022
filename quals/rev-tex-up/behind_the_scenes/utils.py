import pprint
import math
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789_"
occ = {alphabet[i]:0 for i in range(len(alphabet))}

weights = {'a': 31, 'b': 47, 'c': 43, 'd': 11, 'e': 5, 
'f': 73, 'g': 23, 'h': 101, 'i': 7, 'j': 59, 'k': 83, 'l': 19, 'm': 53, 'n': 2, 'o': 3, 'p': 79, 
'q': 71, 'r': 89, 's': 13, 't': 17, 'u': 37, 'v': 61, 'w': 29, 'x': 41, 'y': 67, 'z': 97, 
'0': 49, '1': 24, '2': 144, '3': 5, '4': 3, '5': 2, '6': 36, '7': 9, '8': 4, '9': 16, '_': 1}
def sum(s):
    tot=0
    for c in s:
        if c in weights:
            tot+=weights[c]
        else:
            print(c,"not in alphabet")
    return tot

def value(s):
    tot=1
    for c in s:
        if c in weights:
            if weights[c]==1:
                print("No weight for", c)
            tot*=weights[c]
        else:
            print(c,"not in alphabet")
    print("We are left with ",2147483647/tot)
    return tot

def is_prime(n):
    for num in range(2, int(math.sqrt(n))):
        if n%num==0:
            return False
    return True

def first_primes(n):
    res=[2]
    start = 3
    while len(res)<n:
        if is_prime(start):
            res.append(start)
        start+=2
    return res
hard1= "ou7s74ndin9"
hard2="t3xnologie5"
hard3="w31c0me"
password = "w31c0me_the_8357_n3w_ou7s74ndin9_t3xnologie5_"
def occurences(s = password):
    occ = {}
    for c in s:
        if c in occ:
            occ[c]+=1
        else:
            occ[c]=1
    pprint.pprint(dict(sorted(occ.items(), key=lambda item: item[1], reverse=True)), sort_dicts=False)


def check_num_mult():
    count = 1
    res = []
    target = 360
    for c1 in alphabet[:-1]:
        count1 = count * weights[c1]
        for c2 in alphabet[:-1]:
            count2 = count1 * weights[c2]
            if count2 < target and c1 != 'e' and c2 != 'e':
                for c3 in alphabet[:-1]:
                    count3 = count2 * weights[c3]
                    if count3 < target and c3 != 'e':
                        for c4 in alphabet[:-1]:
                            count4 = count3 * weights[c4]
                            if count4 == target and c4 != 'e':
                                res.append(sorted([c1,c2,c3,c4]))
    import itertools
    res.sort()
    print(list(k for k,_ in itertools.groupby(res)))

def check_num_sum(target):
    count = 0
    res = []
    for c1 in alphabet[:-1]:
        count1 = count + weights[c1]
        for c2 in alphabet[:-1]:
            count2 = count1 + weights[c2]
            if count2 < target:
                for c3 in alphabet[:-1]:
                    count3 = count2 + weights[c3]
                    if count3 == target:
                        res.append(sorted([c1,c2,c3]))
    import itertools
    res.sort()
    return list(k for k,_ in itertools.groupby(res))

    
#pprint.pprint(doubles)
