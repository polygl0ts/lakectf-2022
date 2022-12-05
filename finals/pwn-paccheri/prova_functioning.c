#include <stdio.h>
#include <stdlib.h>
#include <time.h>


// TODO
// 2: signign oracle is too easy : 7 bits, 128 tries on average? 
// 3: test on qemu
// 4: look into pacga to use more than one byte
// 5: encryption oracle takes an argument (in register x1)
//
//
//
//
//


// 2 problems:
// - 7 bits is too low
// - oracle is too easy



void menu();

struct __attribute__((packed)) package {
        char* address;
        int id;
        void (*callback) (char*);
};

struct package *listeur[20];
int list_length = 0;


int read_int() {
    char input[20];
    fgets(input, 10, stdin);
    return atoi(input);
}

long long read_long() {
    char input[40];
    fgets(input, 20, stdin);
    return atol(input);
}

void default_callback (char* addr) {
    printf("The package has arrived to: %s!\n", addr);
}

int main() {
    srand(time(0));
    setvbuf(stdin,NULL,_IONBF,0);
    setvbuf(stdout,NULL,_IONBF,0);
    setvbuf(stderr,NULL,_IONBF,0);

    printf("Welcome to the Swiss post office\n");
    printf("Our famous privacy policies encrypt (and sign!) the destination of every packet\n");
    printf("How can we help you?\n");
    menu();


    __asm__("ldr x8, =0x00fffff7e69d50");
    __asm__("mov x9, sp");
    __asm__("add x9, x9, 16");
    __asm__("pacia x8, x9");
    __asm__("paciasp");
    __asm__("paciasp");
    printf("hello\n");
}

int state = 0;


__attribute__((always_inline))
int fake_prng() {
    return 24;
}

//__attribute__((always_inline))
//void* actual_encryption(void* x, int y) {
    //__asm__("mov x1, 24");
    //__asm__("pacia x0, x1; add sp, sp, 0x10; ret");
    //return 0;
//}

////__attribute__((always_inline))
//void* actual_decryption(void* x, int y) {
    //__asm__("mov x1, 24");
    //__asm__("autia x0, x1; add sp, sp, 0x10; ret");
    //return 0;
//}
//
//
// 0xaaaaaaaa0d88
//
// 0x92eef9d00000000
// 0xffff000000000000
//
//
// 0xfc7e752a00000000
//     0xaaaaaaaa0d88
// 0xfc7eaaaaaaaa0d88

void* encrypt_da_pointer(void* x) {
    __asm__("mov x2, x0; mov x20, x30; bl fake_prng;");
    __asm__("mov x3, 0");
    __asm__("mov x4, 0");
    __asm__("mov x5, 0");

    __asm__("pacga x3, x2, x0;");

    __asm__("ldr x4, BIT_MASK");
    __asm__("and x5, x3, x4");
    __asm__("eor x2, x2, x5");


    __asm__("mov x0, x2; add sp, sp, 0x10; mov x30, x20; ret");
    return 0;
}

long long BIT_MASK = 0x007f000000000000;

int i = 0;
void* decrypt_da_pointer(void* x) {
    __asm__("mov x2, x0; mov x20, x30; bl fake_prng;");
    __asm__("mov x3, 0");
    __asm__("mov x4, 0");
    __asm__("mov x5, 0");

    // remove upper bits
    __asm__("ldr x4, BIT_MASK");
    __asm__("and x5, x2, x4");
    __asm__("eor x2, x2, x5");

    __asm__("pacga x3, x2, x0;");
    __asm__("and x3, x3, x4");

    // compare new pacga with old one
    __asm__("cmp x3, x5");
    __asm__("b.ne -0x40000");
    __asm__("mov x0, x2; add sp, sp, 0x10; mov x30, x20; ret");
    return 0;
}

void mymalloc() {
    if (list_length >= 20) {
        printf("Sorry, we are swiss but we can't handle so many packages\n");
        return;
    }
    struct package *new_pkg = (struct package*) malloc(sizeof(struct package));
    listeur[list_length++] = new_pkg;
    int mysize = sizeof(struct package);
    char *mystr = (char*)malloc(mysize);
    printf("Please enter your destination address:\n");
    fgets(mystr, mysize, stdin);
    new_pkg->address = mystr;

    new_pkg->callback = encrypt_da_pointer(default_callback);

    new_pkg->id = list_length - 1;
}

void myfree() {
    printf("Which package did you lose?\n");
    int c = read_int();
    free(listeur[(int)c]->address);
    if (c >= 18  || c < 0) {
        printf("You definitely did not.\n");
        return;
    }
    free(listeur[(int)c]);
    //listeur[(int)c] = 0;
}

void myset() {
    printf("Which package do you want to edit?\n");
    int c = read_int();
    int mysize = sizeof(struct package);
    printf("Please enter the new address:\n");
    int result = fread(listeur[c]->address, 1, mysize, stdin);
    printf("read %d bytes\n", result);
    printf("New address: %s\n", listeur[c]->address);
    printf("New callback: %p\n", decrypt_da_pointer(listeur[c]->callback));
}

void mycheck() {
    printf("Which package do you want to check?\n");
    int c = read_int();
    printf("old callback: %p\n", listeur[c]->callback);
    printf("new callback: %p\n", decrypt_da_pointer(listeur[c]->callback));
    void (*callback) (char*) = decrypt_da_pointer(listeur[(int)c]->callback);
    callback(listeur[(int)c]->address);
}

void mylist() {
    printf("---\n");
    for (int i = 0; i < list_length; i++) {
        printf("Address: %s", listeur[i]->address);
        printf("id: %d\n", listeur[i]->id);
        printf("callback: %p\n", decrypt_da_pointer(listeur[i]->callback));
        printf("---\n");
    }
}

void mylmao() {
    puts("Ragequit because of no qemu skillz?\n");
    exit(1);
}

void mycomplaint() {
    puts("Unimplemented.");
    exit(1);
}

void win() {
    system("/bin/sh");
}


/*
 *  - Allocate 18 packages
 *  - You free package (18)
 *  - Allocate package 19, package struct has address of 18->address
 *  - Edit package 18
 *  - win!
 * */

void menu() {
    while (1) {
        printf("1. Send a package\n");
        printf("2. Report a lost package\n");
        printf("3. List outgoing packages\n");
        printf("4. Set address of outgoing package\n");
        printf("5. Check if a package is arrived\n");
        printf("6. Exit\n");
        printf("7. Get angry because you don't have an aarch64 machine available\n");
        printf("8. Complain because this menu is too long\n");
        printf("\n");

        int c = read_int();
        switch(c) {
            case 1:
                mymalloc();
                break;
            case 2:
                myfree();
                break;
            case 3:
                mylist();
                break;
            case 4:
                myset();
                break;
            case 5:
                mycheck();
                break;
            case 6:
                exit(0);
                break;
            case 7:
                mylmao();
                break;
            case 8:
                mycomplaint();
                break;
            case 1337:
                puts("Gimme\n");
                long long x = read_long();
                printf("Result: %p\n", encrypt_da_pointer(x));
                break;
            default:
                printf("Vouz parlez franchoise?\n");
                break;
        }

    }
}




