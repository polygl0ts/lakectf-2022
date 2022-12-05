import random as rand

def target(num, steps=6):
    array=[]
    target = -2
    av = num//steps
    for i in range(4):
        val= rand.randint(av-50,av+50)
        array.append(val)
        target+=val
        if i == 2:
            target+=val
    array.append(num - target)
    return array
    

E = target(ord('X'))
P = target(ord('8'))
F = target(ord('0'))
L = target(ord('7'))
letters = ['w','a','s','u','p']
for i in range(len(E)):
    text = f"""For letter {letters[i]}
        \\adda={E[i]}
	\\addb={P[i]}
	\\addc={F[i]}
	\\addd={L[i]}"""
    print(text)
