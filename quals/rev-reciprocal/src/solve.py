import primesieve

offset = 1
v6=0

def fib(n):
    a = 1
    b = 1
    while n>0:
        a,b = b, a+b 
        n -= 1
    return a
        
message = "SSwVgQ"
alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_"
alpha_len = 65
def encrypt(key, message):
    if key < 65:
        return
    buffer = {}
    interval = int(key /alpha_len)
    for i in range(key):

        if i % interval == 0 and int(i/interval) < 65:
            buffer[i] = [i, alphabet[int(i/interval)], 0, 0]
        else:
            buffer[i] = [i, "*", 0, 0]
        # (position, encoding, postion_of_next, ref_count)

    # Connecting
    for i in range(1,key):
        j=i
        
        j*=10
        #rest = j - (j//key * key)
        #print(rest)
        #print(j%key)
        #print("----------------")
        buffer[i][2]=buffer[j%key][0]
        buffer[j%key][3] += 1

        #print(f"{i} '{buffer[i][1]}' ---> {j%key} {buffer[j%key][1]}")
    
   

    res = ""
    for i,c in enumerate(message):
        

        b = buffer[alphabet.index(c) * interval]
        b_next = b
        if b[2] == 0:
            res += c 
            print("0 to 0")
            #print(f"Encrypted {alphabet[alphabet.index(c)]} into {c}")
        else:
            j = 0
            while(j < fib(i) % (alpha_len - 1)):
                b_next = buffer[b_next[2]]
                if b_next[1] != "*":
                    j+=1
              
                    
                     
              

            substitute = b_next[1]


            #print(f"Encrypted {alphabet[alphabet.index(c)]} into {substitute}")
            res += substitute
    return res

#test = "EPFL{"
#print(test)
#print(encrypt(9369319,"EPFL{"))
#def find_p(c, pos, target):

def decrypt(key, res_message):
    buffer = {}
    interval = int(key /alpha_len)
    for i in range(key):
        # (position, encoding, postion_of_next, ref_count)
        if i % interval == 0 and int(i/interval) < 65:
            buffer[i] = [i, alphabet[int(i/interval)], 0, 0]
        else:
            buffer[i] = [i, "*", 0, 0]


    for i in range(1,key):
        j=i
        
        j*=10
        buffer[i][2]=buffer[j%key][0]
        buffer[j%key][3] += 1
        




    res = ""
    print(res_message)
    for i,c in enumerate(res_message):
                
       
        b = buffer[alphabet.index(c) * interval]
        #print(b)
        # To find the decrpytion char we traverse 64 - fib(i) chars
        b_next = b
        if b[2] == 0:
            res += c 
            #print("0 to 0")
            #print(f"Encrypted {alphabet[alphabet.index(c)]} into {c}")
        else:
            #print(fib(i))
            l = 64 - (fib(i) % (alpha_len - 1))
            #print(l)

            j = 0
            while(j < l):
                b_next = buffer[b_next[2]]
                if b_next[1] != "*":
                    j+=1
                    
                    
                     
              
            #print(f"Got char {c}")
            substitute = b_next[1]


            #print(f"Encrypted {alphabet[alphabet.index(c)]} into {substitute}")
            res += substitute

    return res



def checkPeriodLength(p):
    i = 10
    steps = 1
    while(i != 1):
        i *= 10
        i = i % p
        steps += 1

    return steps == p - 1

def find_key(start):
    for p in primesieve.n_primes(18000,20000):
        print(p)
        if p > 67 and checkPeriodLength(p):
            print(p)
            if encrypt(p, "EPFL{") == start :
                print(encrypt(p, "EPFL{"))
                print("p found")
                return p


KEY = 120047
FLAG = "EPFL{7h3_r3cipr0c4l_0f_prim35_4r3_r3p347in9}"
key = find_key("XwSoY")
assert(key == KEY)
enc = encrypt(key,FLAG)
assert(enc == "XwSoYZWEXnbLmPP0{HO20TYYJKrLVr_2KfYhPgkVsFkR")
# Reversing part here
dec = decrypt(key,"XwSoYZWEXnbLmPP0{HO20TYYJKrLVr_2KfYhPgkVsFkR")
assert(dec == FLAG)
print(dec)

