#!/usr/bin/python3
import random as rand
import fonter
import math

password_len = 45
flag_len =14
key_len = 8 

bs = "abcdefghijklmnopqrstuvwxyz"
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
weights = {'a': 31, 'b': 47, 'c': 43, 'd': 11, 'e': 5, 
'f': 73, 'g': 23, 'h': 101, 'i': 7, 'j': 59, 'k': 83, 'l': 19, 'm': 53, 'n': 2, 'o': 3, 'p': 79, 
'q': 71, 'r': 89, 's': 13, 't': 17, 'u': 37, 'v': 61, 'w': 29, 'x': 41, 'y': 67, 'z': 97, 
'0': 49, '1': 24, '2': 144, '3': 5, '4': 3, '5': 2, '6': 36, '7': 9, '8': 4, '9': 16, '_': 1}

def from_base(s:str, base:str = bs):
    """Gives int from string using base given"""
    count = 0
    while s:
        if base.find(s[0]) == -1:
            return  -1
        count = count * len(base) + base.find(s[0])
        s = s[1:]
    return count

def to_base(n:int, base:str = bs):
    """Transforms int into a str using base provided"""
    if n == 0:
        return base[0]
    res = ""
    while n > 0:
        res = base[n % len(base)] + res
        n = n//len(base)
    return res
        
def verify_key(key:str, alphabet:str = bs):
    if len(key)!= 3 + key_len:
        return False
    seed = from_base(key[:2])
    if seed == -1 or key[2]!='_':
        return False
    rand.seed(seed)
    choice = rand.choices(list(alphabet), k=key_len)
    while math.prod([weights[c] for c in choice]) > 2**31 -1:
        choice = rand.choices(list(alphabet), k=key_len)
    choice = sorted(choice, key=lambda item: weights[item])
    #print("".join(choice))
    return key[3:]== "".join(choice)

def generate_flag(n:int, alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"):
    rand.seed(n)
    for i in range(rand.randrange(100,1000)):
        rand.random()
    return "".join(rand.choices(list(alphabet), k=flag_len))

def text_flag(flag):
    flag_template = """
\\newcommand{{\\flag}}{{
    Well done!\\\\

    \\resizebox{{\\textwidth}}{{!}}{{%
    \\begin{{tikzpicture}}
		
{draw}
        	
	\\end{{tikzpicture}}
    }}
}}"""
    flag_text = fonter.draw_flag(flag, [f"\\data{to_base(i)}" for i in range(flag_len)])
    flag_text = flag_template.format(draw=flag_text)
    return flag_text

input = input("So what have you done? ")

if input[:password_len] == "w31c0me_the_8357_n3w_ou7s74ndin9_t3xnologie5_" and verify_key(input[password_len:]):
    print(text_flag(generate_flag(from_base(input[password_len:password_len+2]))))
    print("There you go")
else:
    print("What's that bulls@#%? Do your work properly!")

