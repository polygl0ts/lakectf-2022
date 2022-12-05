#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
extern void* environ;

#define SWAP(x, y) (x) ^= (y); (y) ^= (x); (x) ^= (y);
#define RDRAND(varname) register size_t varname asm ("rbx"); asm inline ( "rdrand %%rbx" : "=r" (varname) );
#define ll long long
#define SIZE 0x30

void setup() {
    setvbuf(stdout, 0, 2, 0);
}

unsigned int __attribute__((noinline)) get_gnomed(ll* arr, ll len) {
    ll* pos = arr;
    while (pos < arr + len) {
        if (pos == arr || *pos >= *(pos-1))
            pos++;
        else {
            SWAP(*pos, *(pos - 1));
            pos--;
        }
        
    }
    return 0;
}

void read_numbers(ll* numbers, ll len) {
    for (ll i = len; i > 0; i--) {
        printf("> ");
        numbers[i] = 42;
        scanf("%lld", &numbers[i]);
    }
}

void vuln(size_t randomness) {
    struct __attribute__((aligned(8), packed)) {
        ll numbers[SIZE];
        ll num_to_sort;
    } data;

    for (int i = 0; i < SIZE; i++) {
        data.numbers[i] = (ll)stdout;
    }
    RDRAND(rnd);
    randomness ^= rnd;
    printf("Have a gift: %p\n", (void*)data.numbers[randomness % SIZE]);

    printf("How many numbers to sort? ");
    scanf("%lld", &data.num_to_sort);
    if (data.num_to_sort > sizeof(data.numbers) / sizeof(data.numbers[0])) {
        exit(1);
    }
    read_numbers(&data.numbers[0], data.num_to_sort);
    get_gnomed(&data.numbers[0], data.num_to_sort);
}

int main() {
    setup();
    puts("Please enter the bitcoin address you'll be sending your donation from here.");
    char address[SIZE];
    read(0, &address[0], SIZE);
    RDRAND(rnd);
    vuln(rnd);
    puts("Thanks, we've sorted your numbers.");
    puts("Please donate any amount of your choosing (minimum of €1337) to polygl0ts to see the result.");
}
