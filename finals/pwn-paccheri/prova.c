#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/mman.h>
#include <stdint.h>

// TODO
// 3: test on qemu
// 6: add POW


void menu();

struct __attribute__((packed)) package {
        char* address;
        int id;
        int state;
        void (*callback) (char*);
};

struct package *listeur[20];
int list_length = 0;

unsigned int crc32b(unsigned int crc, long long message) {
    int i, j;
    unsigned int byte, mask;
    crc = ~crc;

    i = 0;
    for (int z = 0; z < 8; z++) {
        byte = ((0xff << (z*8)) & message) >> (z*8);
        crc = crc ^ byte;
        for (j = 7; j >= 0; j--) {    // Do eight times.
            mask = -(crc & 1);
            crc = (crc >> 1) ^ (0xEDB88320 & mask);
        }
        i = i + 1;
    }
    return ~crc;
}


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

long long* max_range = 0;
long long* state_array = 0;
FILE* urandom;

int main() {
    setvbuf(stdin,NULL,_IONBF,0);
    setvbuf(stdout,NULL,_IONBF,0);
    setvbuf(stderr,NULL,_IONBF,0);

    urandom = fopen("/dev/urandom", "r");
    void *fanculo = malloc(200);

    void *ptr = mmap ( NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0 );
    max_range = (long long*)ptr;
    state_array = ptr + 8;

    FILE* f = fopen("postal_codes", "r");
    char s[20000];
    void* a;
    void* b;
    while (1) {
        fscanf(f, "%p-%p %2000[^\n]", &a, &b, s);
        if (b > *max_range) *max_range = b;
        if (strstr(s, "[heap]")) {
            break;
        }
    }

    *max_range += 0x2000000;

    printf("Welcome to the Swiss post office\n");
    printf("Our famous privacy policies encrypt (and sign!) the destination of every packet\n");
    printf("How can we help you?\n");
    menu();
}



void* encrypt_da_pointer(void* x, int state) {
    __asm__("mov x2, x0; mov x20, x30; mov x0, x1");
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

long long BIT_MASK = 0xffff000000000000;

int i = 0;
void* decrypt_da_pointer(void* x, int state) {
    __asm__("mov x2, x0; mov x20, x30; mov x0, x1");
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
    __asm__("b.eq 8");
    __asm__("mov x2, 0");

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
    fread(&new_pkg->state, 1, 4, urandom);

    new_pkg->callback = encrypt_da_pointer(default_callback, new_pkg->state);

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
    listeur[(int)c] = 0;
}


void myset() {
    printf("Which package do you want to edit?\n");
    int c = read_int();
    int mysize = sizeof(struct package);
    printf("Please enter the new address:\n");

    if ((uintptr_t)listeur[c]->address > (uintptr_t)(*max_range)) {
        printf("This address is not in Switzerland %p!\n", listeur[c]->address);
        printf("Highets postal code: %llx", *max_range);
        exit(0);
    }

    int result = fread(listeur[c]->address, 1, mysize, stdin);
    printf("read %d bytes\n", result);
    printf("New address: %s\n", listeur[c]->address);
    printf("New callback: %p\n", decrypt_da_pointer(listeur[c]->callback, listeur[c]->state));
}

void mycheck() {
    printf("Which package do you want to check?\n");
    int c = read_int();
    void (*callback) (char*) = decrypt_da_pointer(listeur[(int)c]->callback, listeur[c]->state);
    callback(listeur[(int)c]->address);
}

void mylist() {
    printf("---\n");
    unsigned int crc = 0;
    for (int i = 0; i < list_length; i++) {
        printf("Address: %s", listeur[i]->address);
        printf("id: %d\n", listeur[i]->id);
        printf("callback: %p\n", decrypt_da_pointer(listeur[i]->callback, listeur[i]->state));
        crc = crc32b(crc, (long long) listeur[i]->callback ^ (long long) encrypt_da_pointer(((long long) listeur[i]->callback) & (~BIT_MASK), listeur[i]->state));
        printf("---\n");
    }
    printf("Error state: %x\n", crc);
}

void mylmao() {
    puts("Ragequit because of no qemu skillz?\n");
    exit(1);
}

void mycomplaint() {
    puts("Unimplemented.");
    exit(1);
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
            default:
                printf("Vouz parlez franchoise?\n");
                break;
        }

    }
}




