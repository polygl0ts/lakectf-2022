#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>

#define ARGS_COUNT 4096
#define HEAP_COUNT ((1 << 16) - 1024)

typedef enum __attribute__ ((__packed__)) {
    I_TAKE = 69, I_SELF, 
    I_PUSH_ARG, I_PUSH_LABEL, I_PUSH_COMB, I_PUSH_LITERAL,
    I_ENTER_ARG, I_ENTER_COMB,
    ERROR,
    NATIVE,
} ins_kind;

_Static_assert(sizeof(ins_kind) == 1, "Enum is not 1 bytes");

typedef struct {
    uint16_t value;
    uint8_t ck;
    ins_kind kind;
} ins;

_Static_assert(sizeof(ins) == 4, "Enum is not 4 bytes");

typedef struct {
    uint16_t pc;
    uint16_t frame_ptr;
} pair;

typedef struct {
    uint16_t pc;
    pair* args;
    uint16_t args_idx; 
    pair* heap;
    uint16_t heap_idx;
} vm;

/*
Format:
16start_pc 16self_comb_idx
ins <-- needs to be aligned to 32b (technically 16 but shush)
ins
ins...
*/

typedef struct {
    uint16_t start_pc;
    uint16_t self_comb_idx;
    ins* code;
    int code_len;
} binary;

int push(vm* vm, pair pair) {
    if (vm->args_idx == ARGS_COUNT) return 0;
    vm->args[vm->args_idx++] = pair;
    return 1;
}

int pop(vm* vm, pair* pair) {
    if (vm->args_idx == 0) return 0;
    *pair = vm->args[--vm->args_idx]; 
    return 1;
}

int heap_new(vm* vm, uint16_t size, uint16_t* out_frame) {
    if (size == 0 || vm->heap_idx + size > HEAP_COUNT) return 0;
    *out_frame = vm->heap_idx;
    vm->heap_idx += size;
    return 1;
}

pair* heap_get(vm* vm, uint16_t ptr, uint16_t off) {
    if (ptr + off < ptr) return NULL;
    uint16_t p = ptr + off;
    if (!(p < vm->heap_idx)) return NULL;
    return &vm->heap[p];
}

int ck_valid(ins* ins) {
    uint8_t* ptr = (uint8_t*)ins;
    uint8_t crc = ptr[0] ^ ptr[1] ^ ptr[2] ^ ptr[3];
    return crc == 0;
}

void vm_run(vm* vm, binary* binary, char* input, uint32_t input_len) {
    uint16_t pc = binary->start_pc;
    uint16_t frame = 0;

    while (1) {
        if (pc >= binary->code_len) return;
        ins ins = binary->code[pc];
        if (!ck_valid(&ins)) return;
        switch (ins.kind) {
        case I_TAKE:
            if (ins.value == 0) return;
            if (!heap_new(vm, ins.value, &frame)) return;
            for (uint16_t i = 0; i < ins.value; ++i) {
                pair* ptr;
                if (!(ptr = heap_get(vm, frame, i))) return;
                if (!pop(vm, ptr)) return;
            }
            break;
        case I_SELF: {
            pair n;
            if (!pop(vm, &n)) return;
            if (!push(vm, (pair){binary->self_comb_idx, frame})) return;
            pc = n.pc - 1;
            frame = n.frame_ptr;
            break;
        }
        case I_PUSH_ARG: {
            pair* p;
            if (!(p = heap_get(vm, frame, ins.value))) return;
            if (!push(vm, *p)) return;
            break;
        }
        case I_PUSH_LABEL: {
            if (!push(vm, (pair){ins.value, frame})) return;
            break;
        }
        case I_PUSH_COMB: {
            if (!push(vm, (pair){ins.value, 0})) return;
            break;
        }
        case I_PUSH_LITERAL: {
            if (!push(vm, (pair){binary->self_comb_idx, ins.value})) return;
            break;
        }
        case I_ENTER_ARG: {
            pair* p;
            if (!(p = heap_get(vm, frame, ins.value))) return;
            pc = p->pc - 1;
            frame = p->frame_ptr;
            break;
        }
        case I_ENTER_COMB:
            pc = ins.value - 1;
            frame = 0;
            break;
        case ERROR:
            return;
        case NATIVE: {
            /*
            debug
            negate
            add
            sub
            printi
            printc
            eq
            input
            */
            switch (ins.value) {
            case 0: // debug
                return;
            case 1: { // neg
                pair p;
                if (!pop(vm, &p)) return;
                p.frame_ptr = -p.frame_ptr;
                if (!push(vm, p)) return;
                break;
            }
            case 2: // add
            case 3: { // sub
                pair x1;
                pair x2;
                if (!pop(vm, &x1)) return;
                if (!pop(vm, &x2)) return;
                if (x1.pc != binary->self_comb_idx || x2.pc != binary->self_comb_idx) return;
                pair res = x1;
                if (ins.value == 2) {
                    res = (pair){binary->self_comb_idx, x2.frame_ptr + x1.frame_ptr};
                } else if (ins.value == 3) {
                    res = (pair){binary->self_comb_idx, x2.frame_ptr - x1.frame_ptr};
                } else {
                    return;
                }
                if (!push(vm, res)) return;
                break;
            }
            case 4: { // printi
                if (vm->args_idx == 0) return;
                pair p = vm->args[vm->args_idx - 1];
                printf("%d", p.frame_ptr);
                break;
            }
            case 5: { // printc
                if (vm->args_idx == 0) return;
                pair p = vm->args[vm->args_idx - 1];
                printf("%c", p.frame_ptr);
                break;
            }
            case 6: { // eq
                pair x1;
                pair x2;
                pair ye;
                pair no;
                if (!pop(vm, &x1)) return;
                if (!pop(vm, &x2)) return;
                if (!pop(vm, &ye)) return;
                if (!pop(vm, &no)) return;
                if (x1.pc != binary->self_comb_idx || x2.pc != binary->self_comb_idx) return;
                if (x1.frame_ptr == x2.frame_ptr) {
                    if (!push(vm, ye)) return;
                } else {
                    if (!push(vm, no)) return;
                }
                break;
            }
            case 7: { // input
                char c = {0};
                scanf(" %c", &c);
                if (!push(vm, (pair){binary->self_comb_idx, c})) return;
                break;
            }
            case 8: { // inputI
                pair p;
                if (!pop(vm, &p)) return;
                if (p.pc != binary->self_comb_idx) return;
                if (p.frame_ptr >= input_len) return;
                if (!push(vm, (pair){binary->self_comb_idx, input[p.frame_ptr]})) return;
                break;
            }
            default: return;
            }
            break;
        }
        default: return;
        }
        pc += 1;
    }
}

int parse_header(char* file, int len, binary* binary) {
    if (len < 2 || len % 4 != 0) return 0;
    uint16_t* as_16 = (uint16_t*)file;
    binary->start_pc = as_16[0];
    binary->self_comb_idx = as_16[1];
    binary->code_len = len/4 - 1;
    binary->code = (ins*)&as_16[2];
    return 1;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: ./fun file.b\n");
        return -1; 
    }
    char* filename = argv[1];

    int file_desc = open(filename, O_RDONLY);
    if (file_desc < 0) return -1;

    struct stat file_stat = {0}; 
    if (fstat(file_desc, &file_stat) < 0) return -1;

    char* file = mmap(NULL, file_stat.st_size, PROT_READ, MAP_PRIVATE, file_desc, 0);
    if (file == MAP_FAILED) return -1;

    binary binary = {0};
    if (!parse_header(file, file_stat.st_size, &binary)) return -1;

    pair* args = calloc(ARGS_COUNT, sizeof(*args));
    if (!args) return -1;
    pair* heap = calloc(HEAP_COUNT, sizeof(*heap));
    if (!heap) return -1;

    pair* args_end = args + ARGS_COUNT;
    pair* heap_end = heap + HEAP_COUNT;

    vm vm = {
        0, args, 0, heap, 0,        
    };

    printf("welcome ! my name is Tim. i am a Fun flag checker ! i says \"Win!\" if the input is the flag :)\ni only check the part inside the curlies \"EPFL{this here}\", don't enter \"EPFL{\" and \"}\".\n");

    char input[256] = {0};
    scanf("%255s", input);

    vm_run(&vm, &binary, input, 256);
    printf("\nbeep boop i am done goodbye *wave*\n");
}
