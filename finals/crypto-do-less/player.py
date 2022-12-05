from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from binascii import hexlify, unhexlify


def sign(message,key):
    h = SHA256.new(message.encode())
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(h)
    return(signature)


# Raises value error in case of verification failure
def verify(message, key, signature):
    h = SHA256.new(message.encode())
    verifier = DSS.new(key, 'fips-186-3')
    verifier.verify(h, signature)


class Player:
    def __init__(self, id,  rounds= 3, dealerid = 0, max_player_number=4):
        self.max_player_number = max_player_number
        self.id = id
        self.max_round = rounds
        self.dealerid = dealerid
        self.privkey = ECC.import_key(open(str(id)+'/privkey.pem').read())
        self.pubkeys = [0 for i in range (self.max_player_number+1)]
        for i in range (0,self.max_player_number+1):
            self.pubkeys[i] = ECC.import_key(open('pub' + str(i) + '.pem').read())
        f = open(str(id) + "/flag","r")
        self.flag = f.read()
        f.close()
        self.flagkey = None
        self.failed = True
        self.seenkeys = []


    def parse(self, message, round):
        if round>self.max_round or round<0:
            raise ValueError ("Too many rounds")
        newflagkey = message[:354]
        dealersignature = unhexlify(message[354:482].encode())
        verify(newflagkey,self.pubkeys[self.dealerid],dealersignature)
        remainder = message[482:]
        previous = message[:482]
        signerlist = []
        for i in range (0,round):
            signer = int(remainder[0])
            if (signer in signerlist) or (signer == 0):
                raise ValueError("Signed twice by same")
            signature = unhexlify(remainder[1:129].encode())
            previous += remainder[0]
            verify(previous,self.pubkeys[signer],signature)
            previous = previous + remainder[1:129]
            remainder = remainder[129:]
        if len(remainder) != 0:
            raise ValueError ("Wrong round number")
        return(newflagkey)

    def send_to_all(self,m):
        l = len(m)
        ls = str(l)
        while (len(ls)<4):
            ls = "0"+ls
        res = ls + ls + ls + ls + m + m + m + m
        return(res)

    def forward(self,message):
        new = message + str(self.id)
        s = hexlify(sign(new, self.privkey)).decode()
        concat = new + s
        return(concat)

    def round(self,message,r):
        length = 482 + 129*r
        msgs_recevs = []
        msgs_fwrd = []
        send = ""
        while len(message) !=0:
            msgs_recevs.append(message[:length])
            message = message[length:]
        for m in msgs_recevs:
            try: 
                k = self.parse(m,r)
                if not k in self.seenkeys:
                    self.seenkeys.append(k)
                    msgs_fwrd.append(self.forward(m))
            except Exception:
                pass
        send = ""
        for m in msgs_fwrd:
            send += m
        return(send)


    def vote(self):
        res = (len(self.seenkeys)==1)
        msg = 0
        if res:
            msg = 1
        msg = str(self.id) + str(msg)
        msg = msg + hexlify(sign(msg, self.privkey)).decode()
        return(msg)

    #do voting
    def vote_result(self,mi):
        seenids = []
        ok = 0
        no = 0
        expected_len = 130
        nb = len(mi)//expected_len
        msgs = [mi[i*expected_len: (i+1)*expected_len] for i in range (0, nb)]
        if len(msgs) > self.max_player_number or len(msgs)< self.max_player_number-1:
            return True
        for m in msgs:
            try: 
                id = int(m[0])
                choice = int(m[1])
            except:
                return True
            if id in seenids:
                return True
            seenids.append(id)
            try: 
                signature = unhexlify(m[2:130].encode())
                verify(m[0:2], self.pubkeys[id], signature)
            except ValueError:
                return True
            if choice not in [0,1]:
                return True
            if choice == 0:
                no+=1
            if choice == 1:
                ok +=1
        if ok > 2:
            return False
        if no > 2:
            return True

    def set_result(self,mi):
        self.failed = self.vote_result(mi)
        if self.failed == True:
            self.flagkey = ECC.generate(curve='P-256').public_key()
        if self.failed == False:
            try:
                self.flagkey = ECC.import_key(unhexlify(self.seenkeys[0].encode()).decode())
            except: 
                self.flagkey = ECC.generate(curve='P-256').public_key()

    #do flag query management
    def check_flag_query(self,message):
        if self.failed:
            return False
        query = message[:4]
        signature = unhexlify(message[4:132].encode())
        if query != "flag":
            return False
        if self.flagkey:
            try: 
                verify(query, self.flagkey, signature)
            except ValueError:
                return False
        return True
        
    def get_flag(self,message):
        test = self.check_flag_query(message)
        if(test):
            return(self.flag)
        return("")

    def treat(self,message_received):
        send = ""
        # extract round and message content
        message, r = message_received[1:], int(message_received[0])
        if (r<self.max_round):
            send = self.send_to_all(self.round(message,r))
        if r==self.max_round:
            self.round(message,r)
            send = self.send_to_all(self.vote())
        if r==self.max_round+1:
            self.set_result(message)
            send = self.send_to_all("")
        if r==self.max_round+2:
            send = self.send_to_all(self.get_flag(message))
        return(send)




    