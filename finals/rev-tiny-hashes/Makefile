#CFLAGS=-g -O0 -fno-stack-protector -no-pie
CFLAGS=

hash: main.c
	aarch64-linux-gnu-gcc ${CFLAGS} -o $@ $^
	aarch64-linux-gnu-strip $@

run:
	qemu-aarch64 -L /usr/aarch64-linux-gnu/ ./hash 2>&1

run-fork:
	socat tcp-l:"2020",fork,reuseaddr EXEC:"make run"
