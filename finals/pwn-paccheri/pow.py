#!/usr/bin/python3
"""
Remote: $ ./solve.py --connection-info "nc 127.0.0.1 5000"
Local: $ ./solve.py
"""

import pwn
import re
import subprocess
import sys

if len(sys.argv) >= 3 and sys.argv[1] == "--connection-info":
    _, host, port = sys.argv[2].split()
    conn = pwn.remote(host, port)

    print('Proof of work...')
    # proof of work: curl -sSfL https://pwn.red/pow | sh -s s.AAB1MA==.yxkRPPUmuXPTqdq19QMrlA==
    pow_cmd = re.findall(r'proof of work: (.*)', conn.recvline().decode())
    pow_solution = subprocess.run(pow_cmd, shell=True, capture_output=True).stdout
    conn.sendafter(b'solution: ', pow_solution)
else:
    conn = pwn.process(["./paccheri"])


#print('Send solution...')

#conn.send(open('solution.txt', 'rb').read())
#print(conn.recvline())
conn.interactive()

