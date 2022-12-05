from dealer import deal
from player import *

def separate(m, expected_length):
    msg = m
    lens = []
    msgs = ["","","",""]
    for i in range (0, 4):
        try:
            l = int(msg[:4])
            lens.append(l)
            msg = msg[4:]
            if l%expected_length != 0:
                return msgs
        except:
            return msgs
    if lens[0]+lens[1]+lens[2]+lens[3] != len(msg):
        return msgs
    for i in range (0, 4):
        l = lens[i]
        msgs[i] = msg[:l]
        msg = msg[l:]
    return msgs


def exec():
    rounds = 4
    length = 482
    resstr = "0"+deal()[:482]
    res = [resstr for j in range (0,4)]
    p1 = Player(1,rounds= rounds, dealerid = 0)
    p2 = Player(2,rounds= rounds, dealerid = 0)
    p3 = Player(3,rounds= rounds, dealerid = 0)
    for i in range (1, rounds+4):
        if i==rounds+1:
            length = 130
        elif i==rounds+2:
            length = 132
        elif i==rounds+3:
            length = 15
        else:
            length+=129
        m1 = p1.treat(res[0])
        m1 = separate(m1,length)
        m2 = p2.treat(res[1])
        m2 = separate(m2,length)
        m3 = p3.treat(res[2])
        m3 = separate(m3,length)
        print(res[3])
        m4 = input("round " + str(i)+" input :\n")
        m4 = separate(m4,length)
        res = [str(i) + m1[j] + m2[j] + m3[j] + m4[j] for j in range (0,4)]
    print(res[3])


if __name__ == '__main__':
    exec()
    
    


