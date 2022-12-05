import pgpy
import re
import socketserver

import bot

def read_ascii_armored(f):
    buf = ''
    while not (line := f.readline()).startswith('-----END'):
        buf += line
    buf += line
    return buf

with open('flag.asc') as f:
    FLAG = f.read()

SECRET_KEY, _ = pgpy.PGPKey.from_file("secret.asc")

with open('wordlist.txt') as f:
    WORDS = re.compile('|'.join(f.read().split()))

CHOICES = '''
1. Show flag
2. Show public key
3. Submit feedback
4. Quit
'''

class MyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pipe = self.request.makefile('rw', 1)
        while True:
            pipe.write(CHOICES)
            pipe.write('Your choice: ')
            try:
                choice = int(pipe.readline())
            except ValueError:
                choice = 0
            if choice == 1:
                pipe.write(FLAG)
            elif choice == 2:
                pipe.write(str(SECRET_KEY.pubkey))
            elif choice == 3:
                pipe.write("Please enter your encrypted feedback below.\n")
                feedback = pgpy.PGPMessage.from_blob(read_ascii_armored(pipe))
                feedback = SECRET_KEY.decrypt(feedback).message.decode(errors='replace')
                response = bot.respond(feedback)
                response = pgpy.PGPMessage.new(response, cleartext=False)
                pipe.write(str(response))
            elif choice == 4:
                pipe.write("Bye!\n")
                pipe.close()
                break

with socketserver.ThreadingTCPServer(('0.0.0.0', 1337), MyRequestHandler) as server:
    server.serve_forever()
    
