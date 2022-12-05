#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#define ENDORSE_SIZE 0x20
#define BRIEF_SIZE 0x40

typedef struct {
    char* ptr;
    unsigned long size;
    unsigned long freed;
} chunk;

typedef struct {
    unsigned long size;
    unsigned long used;
    chunk* data;
} plan;

static plan free_plan;
static plan pro_plan;
static chunk free_plan_data[12];

void setup() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    free_plan.size = 12;
    free_plan.used = 0;
    free_plan.data = &free_plan_data[0];

    pro_plan.size = 0;
    pro_plan.used = 0;
}

void cleanup() {
    for (unsigned long i = 0; i < free_plan.used; i++) {
        if (!free_plan.data[i].freed) {
            free(free_plan.data[i].ptr);
            free_plan.data[i].freed = 1;
        }
    }
    for (unsigned long i = 0; i < pro_plan.used; i++) {
        if (!pro_plan.data[i].freed) {
            free(pro_plan.data[i].ptr);
            pro_plan.data[i].freed = 1;
        }
    }
}

chunk* get_next_chunk(unsigned long size) {
    chunk* c;
    if (free_plan.used < free_plan.size) {
        c = &free_plan.data[free_plan.used++];
    } else if (pro_plan.used < pro_plan.size) {
        c = &pro_plan.data[pro_plan.used++];
    } else {
        puts("No more data available, Nile is bankrupt. Thanks a lot!");
        abort();
    }
    c->freed = 0;
    c->size = size;
    c->ptr = calloc(size, 1);
    return c;
}

void endorse() {
    chunk* next = get_next_chunk(ENDORSE_SIZE);
    printf("Okay, how long is your endorsement (max %d)?\n> ", ENDORSE_SIZE - 1);
    unsigned long len;
    scanf("%lu", &len);
    if (len > ENDORSE_SIZE - 1) {
        puts("Can you read? How did you manage to get an endorsement, even if it's a fake one...");
        return;
    }
    long res = read(0, next->ptr, len);
    if (res != -1) next->ptr[res] = 0;
}

void description() {
    chunk* next = get_next_chunk(BRIEF_SIZE);
    printf("Feel free to describe your book in as much detail as you like. On the condition that there are at most %d details, of course.\nHow long is it?\n> ", BRIEF_SIZE - 1);
    unsigned long len;
    scanf("%lu", &len);
    if (len > BRIEF_SIZE - 1) {
        puts("Can you read? I don't understand how you'd write a description you can't even read yourself...");
        return;
    }
    long res = read(0, next->ptr, len);
    if (res != -1) next->ptr[res] = 0;
}

void review() {
    puts("Here's an overview of the information you provided us, and our NSA overlords, so far:");
    for (unsigned long i = 0; i < free_plan.used; i++) {
        if (!free_plan.data[i].freed) {
            puts(free_plan.data[i].ptr);
        }
    }
    for (unsigned long i = 0; i < pro_plan.used; i++) {
        if (!pro_plan.data[i].freed) {
            puts(pro_plan.data[i].ptr);
        }
    }
    puts("I hope that's helpful to you.");
}

void data_remove() {
    puts("Which piece of data would you like to remove?");
    printf("> ");
    unsigned long idx = 0;
    scanf("%lu", &idx);
    chunk* c;
    if (idx < free_plan.used) {
        c = &free_plan.data[idx];
    } else {
        idx -= free_plan.used;
        if (idx >= pro_plan.used) {
            puts("Nope, you haven't provided us with *that* much data yet...");
            return;
        }
        c = &pro_plan.data[idx];
    }
    free(c->ptr);
    c->freed = 1;
    c->size = 0;
}

void upgrade() {
    if (pro_plan.size > 0) {
        puts("You're already on our most expensive plan.");
        return;
    }
    puts("Thank you for choosing to pay for Nile. Please be informed that your credit card will now be charged for all expenses our company will have over the next 5 years.\nNile appreciates having you as a customer!");
    pro_plan.used = 0;
    pro_plan.size = 128;
    pro_plan.data = calloc(pro_plan.size * sizeof(chunk), 1);
    puts("Unfortunately, during the migration, we lost some of your historical data. We sincerely apologize, and hope you won't reconsider your choice for Nile.");
    free_plan.data += 10;
    free_plan.used = free_plan.used >= 10 ? free_plan.used  - 10 : 0;
    free_plan.size -= 10;
}

int menu() {
    if (feof(stdin)) return 0;

    puts("Would you like to:\n\t1. Add a fake endorsement\n\t2. Add a brief description\n\t3. Review your current entries\n\t4. Remove some data\n\t5. Upgrade your plan\n\t6. quit\n");
    printf("> ");
    int choice = 0;
    scanf("%d", &choice);
    switch (choice) {
        case 1:
            endorse();
            break;
        case 2:
            description();
            break;
        case 3:
            review();
            break;
        case 4:
            data_remove();
            break;
        case 5:
            upgrade();
            break;
        case 6:
            puts("Goodbye! Thank you for using Nile.");
            return 0;
        default:
            puts("What?");
    }
    return 1;
}

int main() {
    setup();
    
    puts("Welcome to Nile, the newest and most advanced publishing and selling platform known to mankind.");
    while (menu());
    cleanup();
}
