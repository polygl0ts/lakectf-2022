from curses.ascii import isdigit
import random as rand
import sys
import math
import utils
from enum import Enum,Flag, auto
import numpy as np

class Flags():
    flag:Flag

    def __init__(self, flag) -> None:
        self.flag=flag

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.flag == other.flag
        return False
    
    def write(self)->str:
        return '\t'+self.flag.value + "=1\n" 

class rX(Flags):
    rValue:chr
    def __init__(self, rValue:chr) -> None:
        self.rValue=rValue
        super().__init__(Flag.RX)
    def __eq__(self, other):
        return super().__eq__(other) and self.rValue == other.rValue
    
    def write(self):
        return super().write() + f"\t\\rValue={weights[self.rValue]}\n"

class nX(Flags):
    nValue:chr
    def __init__(self, nValue:chr) -> None:
        self.nValue=nValue
        super().__init__(Flag.NX)
    def __eq__(self, other):
        return super().__eq__(other) and self.nValue == other.nValue
    def write(self):
        return super().write() + f"\t\\nValue={weights[self.nValue]}\n"

    
class Must(Flags):
    number_of_m:int
    def __init__(self, number_of_m=1) -> None:
        self.number_of_m=number_of_m
        super().__init__(Flag.MUST)
    def __eq__(self, other):
        return super().__eq__(other)
    def write(self, num):
        assert num>0
        return f"\t\\m={num}\n"
        
    

    
class Flag(Enum):
    A0 = "\\aOn"
    C0 = "\\cOn"
    EVEN = "\\even"
    ODD = "\\odd"
    RX = "\\rX"#next value is \rValue
    NX = "\\nX"
    LT = "\\lt"
    GT = "\\gt"
    EQEQ = "\\eq"
    MUST = "\\m"



A0 = Flags(Flag.A0)
C0 = Flags(Flag.C0)
EVEN = Flags(Flag.EVEN)
ODD = Flags(Flag.ODD)
LT = Flags(Flag.LT)
GT = Flags(Flag.GT)
EQEQ = Flags(Flag.EQEQ)
MUST = Must()


c = 725258376
password = "w31c0me_the_8357_n3w_ou7s74ndin9_t3xnologie5_"
alphabet = "abcdefghijklmnopqrstuvwxyz"
weights = {'a': 31, 'b': 47, 'c': 43, 'd': 11, 'e': 5, 
'f': 73, 'g': 23, 'h': 101, 'i': 7, 'j': 59, 'k': 83, 'l': 19, 'm': 53, 'n': 2, 'o': 3, 'p': 79, 
'q': 71, 'r': 89, 's': 13, 't': 17, 'u': 37, 'v': 61, 'w': 29, 'x': 41, 'y': 67, 'z': 97, 
'0': 49, '1': 24, '2': 144, '3': 5, '4': 3, '5': 2, '6': 36, '7': 9, '8': 4, '9': 16, '_': 1}

# flags

flags = {'a': [], 'e': [ODD], 'i': [], 'o': [Must(3)], 'u': [MUST, rX('o'), nX('7')],
    'b': [], 'c': [], 'd': [rX('n')], 'f': [], 
    'g': [rX('o'), nX('i'), MUST], 
    'h': [nX('e'), A0, MUST], 'j': [rX('g')], 'k': [nX('0')],
    'l': [MUST,EQEQ, rX('o')], 'm': [nX('e')], 'n': [C0], 
    'p': [nX('q')], 'q': [nX('p')], 'r': [EVEN,ODD], 
    's': [MUST,EQEQ,nX('7')], 't': [C0,rX('_'),Must(2)], 
    'v': [nX('z')], 'w': [C0], 'x': [MUST,rX('3'),nX('n')],
    'y': [nX('z')], 'z': [rX('q')], 
    '0': [MUST,rX('c'),nX('m')], '1': [rX('3'),MUST], '2': [],
    '3': [EVEN,A0,C0], '4': [MUST,rX('7'),nX('n')], '5': [LT, rX('e'), Must(2)], 
    '6': [], '7': [], '8': [rX('_'),MUST,LT,C0], '9': [rX('n')], '_': []}

key_len = 8
flag_len = 14

def step(n:int):
    if n%2==0:
        return n//2
    else:
        return 3*n + 1
def steps(n:int, i:int):
    for i in range(i):
        n = step(n)
    return n

bs = "abcdefghijklmnopqrstuvwxyz"
def to_base(n:int, base:str = bs):
    """Transforms int into a str using base provided"""
    if n == 0:
        return base[0]
    res = ""
    while n > 0:
        res = base[n % len(base)] + res
        n = n//len(base)
    return res

def from_base(s:str, base:str = bs):
    """Gives int from string using base given"""
    count = 0
    while s:
        if base.find(s[0]) == -1:
            return  -1
        count = count * len(base) + base.find(s[0])
        s = s[1:]
    return count
        
def generate_key(n:int, alphabet:str = alphabet):
    """Generates key using key given"""
    #maybe use secrets instead?
    #check if overflows
    if n > 26**2:
        sys.eprint("Key too long, using truncated key instead")
        n %= 26**2
    rand.seed(n)
    choice = rand.choices(list(alphabet), k=key_len)
    while math.prod([weights[c] for c in choice]) > 2**31 -1:
        choice = rand.choices(list(alphabet), k=key_len)
    choice = sorted(choice, key=lambda item: weights[item])
    head = to_base(n)
    while len(head) < 2:
        head = bs[0] + head
    return head +"_"+ "".join(choice)
    
def verify_key(key:str, alphabet:str = alphabet):
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
    return key[3:]== "".join(choice)


def generate_flag(n:int, alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"):
    rand.seed(n)
    for i in range(rand.randrange(100,1000)):
        rand.random()
    return "".join(rand.choices(list(alphabet), k=flag_len))

def generate_file(group_num:int, solved:bool=False, flagged:bool=False):
    from num2words import num2words
    import fonter
    def name(c:chr):
        if c == '_':
            return "textUnderscore"
        elif str.isdigit(c):
            return 'text'+num2words(int(c))
        else:
            return f"text{c}"

    def to_body(s:str):
        res = ""
        for c in s:
            a = "\\_" if c=='_' else c
            res += f"\n\t\\{name(c)}\n\t\\eval\n"#\t{a} \\the\\e\\\\\n"
        return res

    with open("template.tex",'r') as f:
        template = f.read()
        key = generate_key(group_num)


        #c stuff ==========
        global c
        template = template.replace("0%==c==", str(c))
        c_end = steps(c, len(password)+key_len+3) # c at end
        template = template.replace("0%==c_end==", str(c_end))
        c_limit = steps(c, len(password)+2) # start of key
        template = template.replace("0%==c_limit==", str(c_limit))

        print('key_tot', password+key)
        
        uctot = password.count('_') + key.count('_')
        template = template.replace("0%==uctot==", str(uctot))

        resp = math.prod([weights[c] for c in key[2:]]) # key answer
        template = template.replace("0%==resp==", str(resp))
        

        #group num encoded
        uni1 = steps(c, len(password))
        uni2 = steps(uni1, 1)
        template = template.replace("0%==uni1==", str(uni1))
        template = template.replace("0%==uni2==", str(uni2))
        template = template.replace("0%==char1==", '`'+key[0])
        template = template.replace("0%==char2==", '`'+key[1])


        # must stuff 
        must_c = [c for c in flags if any(isinstance(x,Must) for x in flags[c])]
        musts = {c:i for i,c in enumerate(must_c)}
        must_num = len(musts) + 3

        mmem_init = "".join([f"\\newcount\\mmem{to_base(i)}\n" for i in range(must_num)])
        template = template.replace("%==mmem_init==", mmem_init)
        mmem_set=[f"\t\\mmem{to_base(i)}=" for i in range(must_num)]
        must_tot=0
        for i in range(must_num):
            if i<len(musts):
                for flag in flags[must_c[i]]:
                    if isinstance(flag, Must):
                        mmem_set[i]+=str(flag.number_of_m)+'\n'
                        must_tot+=flag.number_of_m
            else:
                mmem_set[i]+=str(rand.randrange(0,4))+'\n'

        mmem_set="".join(mmem_set)
        template = template.replace("%==mmem_set==", mmem_set)
        template = template.replace("0%==must_tot==", str(must_tot))

        must_verif="".join([f"\t\\ifnum\\mmem{to_base(i)}<0 \\err \\fi\n" for i in range(must_num)])
        template = template.replace("%==must_verif==", must_verif)
        must_incr = "".join([f"\t\\ifnum\\m={i+1} \\advance\\mmem{to_base(i)} by -1 \\fi\n" for i in range(must_num)])
        must_incr += "\n\t\\advance\\musts by 1"
        template = template.replace("%==must_incr==", must_incr)

        #positions stuff
        position_template = """
        \\ifnum\\np=\\pmem{num}
            \\temp=0
{cond}
            \\ifnum\\temp<1 \\err \\fi
        \\fi\n

{reccond}
        """
        position_check = "".join([f"\t\t\\ifnum\\c={steps(c,password.find(letter))} \\pmem{to_base(i)}=\\np \\fi\n" for i,letter in enumerate(['3', '5', 'i','h'])])
        position_check+='\n'
        for i,letter in enumerate(['e', 'n', 'i','h']):
            base_char = to_base(i)
            positions = [pos for pos, char in enumerate(password) if weights[char] == weights[letter]]
            #print(letter,positions)
            cond = "".join([f"\t\t\t\\ifnum\\c={steps(c,pos)} \\advance\\temp by 1 \\fi\n" for pos in positions])
            reccond = "".join([f"\t\t\\ifnum\\c={steps(c,pos)} \\ifnum\\np=\\pmem{base_char} \\else \\err \\fi \\fi\n" for pos in positions])
            
            position_check += position_template.format(cond=cond, reccond=reccond, num=base_char)
        template = template.replace("%==position_check==", position_check)

        # data stuff
        flag = generate_flag(group_num)
        print('flag', flag)
        add_init = "\n".join([f"\\newcount\\add{to_base(i)}" for i in range(flag_len)])
        template = template.replace("%==add_init==", add_init)
        data_init = "".join([f"\\newcount\\data{to_base(i)}\n" for i in range(flag_len)])
        template = template.replace("%==data_init==", data_init)
        add_set="".join([f"\t\\add{to_base(i)}=0\n" for i in range(flag_len)])
        template = template.replace("%==add_set==", add_set)
        
        add_data="".join([f"\t\\advance\\data{to_base(i)} \\add{to_base(i)}\n" for i in range(flag_len)])
        template = template.replace("%==add_data==", add_data)

        offsets = fonter.get_flag_offsets(flag)
        target_data = np.array(offsets)
        np.random.seed(group_num)
        text_offsets = {c:np.random.randint(-200, 200, flag_len) for c in utils.alphabet}
        tot_offset = np.zeros(flag_len)
        for c in password+key:
            tot_offset += text_offsets[c]

        base_data = target_data - tot_offset
        data_set = "".join([f"\t\\data{to_base(i)}={int(base_data[i])}\n" for i in range(flag_len)])
        template = template.replace("%==data_set==", data_set)    


        #text generation
        text_template = """
\\newcommand{{\\{name}}}{{
\t\\np={np}
\t\\uni={uni}
{flags}
}}\n"""
        text = ""
        for c in utils.alphabet:
            #print(flags[c])
            written_flags = [flag.write() for flag in flags[c] if not isinstance(flag, Must)]
            written_flags += [flag.write(musts[c]+1) for flag in flags[c] if isinstance(flag, Must)]
            text_flags = "".join(written_flags)
            data_string = "".join([f"\t\\add{to_base(i)}={int(text_offsets[c][i])}\n" for i in range(flag_len)])
            text_flags += data_string
            text+= text_template.format(name=name(c), np=weights[c], uni=ord(c), flags=text_flags)

        #print(text)
        template = template.replace("%==text==", text)
        #body 
        body:str
        if solved:
            print("solved")
            body = to_body(password+key)
        else:
            body = to_body("wtf")
        template = template.replace("%==body==", body)
        if flagged:
            flag_template = """
            Well done!\\\\

    \\resizebox{{\\textwidth}}{{!}}{{%
    \\begin{{tikzpicture}}
		
{draw}
        	
	\\end{{tikzpicture}}
    }}"""
            flag_text = fonter.draw_flag(flag, [f"\\data{to_base(i)}" for i in range(flag_len)])
            flag_text = flag_template.format(draw=flag_text)
            template = template.replace("%==flag==", flag_text)
        else:
            template = template.replace("%==flag==", "\tTry more")
        #print(fonter.draw_flag(flag, data))

        
        with open(f"template_filled.tex",'w') as result:
            result.write(template)

generate_file(1)
#with open(f"POC_solved.tex",'r') as f:
#    print(f.read())
"""
n = 0
with open(f"test/test{n}.tex",'w') as f:
    f.write(text)
"""
