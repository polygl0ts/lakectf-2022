#!/bin/bash
socat tcp-l:5000,reuseaddr,fork exec:"/srv/app/run.py 20 1 /srv/app/flag_lv0.txt" &
socat tcp-l:5001,reuseaddr,fork exec:"/srv/app/run.py 450 3 /srv/app/flag_lv1.txt"
