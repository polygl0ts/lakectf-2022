all : nile

27 : PoC.c
	gcc PoC.c -o 27 -DLIBC_VERSION=27 -L. -lc-2.27
	patchelf --interpreter ./ld-2.27.so  27
	patchelf --replace-needed libc.so.6 ./libc-2.27.so 27
	patchelf --set-rpath ./ 27

31 : PoC.c
	gcc PoC.c -o 31 -DLIBC_VERSION=31 -L. -lc-2.31
	patchelf --interpreter ./ld-2.31.so  31
	patchelf --replace-needed libc.so.6 ./libc-2.31.so 31
	patchelf --set-rpath ./ 31

32 : PoC.c
	gcc PoC.c -o 32 -DLIBC_VERSION=32 -L. -lc-2.32
	patchelf --interpreter ./ld-2.32.so  32
	patchelf --replace-needed libc.so.6 ./libc-2.32.so 32
	patchelf --set-rpath ./ 32

nile : challenge.c
	gcc challenge.c -o nile -L. -lc-2.32
	patchelf --interpreter ./ld-2.32.so nile
	patchelf --replace-needed libc.so.6 ./libc-2.32.so nile
	patchelf --set-rpath ./ nile

.PHONY : clean

clean :
	rm -f 27 31 32 nile
