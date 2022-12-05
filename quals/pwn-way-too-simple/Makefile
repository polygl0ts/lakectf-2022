
all:
	gcc string.c -static -m32 -s  -Wl,--section-start=.text=0x11111111 -o remote_files/exe -O0 -no-pie -fno-pic -g
	strip -s remote_files/exe
