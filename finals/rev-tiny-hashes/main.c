/*
 * Hash functions stolen from
 * https://stackoverflow.com/questions/7666509/hash-function-for-string/45641002#45641002
 */

#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<sys/mman.h>
#include <unistd.h>
#include <string.h>

#define PAGESIZE (sysconf(_SC_PAGESIZE))
#define NNOPS 4
#define INSN_SZ 4

char ALPHABET[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\\'()*+,-./:;<=>?@[\\]^_`{|}~ ";

char* MANIFESTO[] = {
"This",
"is",
"our",
"world",
"now...",
"the",
"world",
"of",
"the",
"electron",
"and",
"the",
"switch,",
"the",
"beauty",
"of",
"the",
"baud.",
"We",
"make",
"use",
"of",
"a",
"service",
"already",
"existing",
"without",
"paying",
"for",
"what",
"could",
"be",
"dirt-cheap",
"if",
"it",
"wasn't",
"run",
"by",
"profiteering",
"gluttons,",
"and",
"you",
"call",
"us",
"criminals.",
"We",
"explore...",
"and",
"you",
"call",
"us",
"criminals.",
"We",
"seek",
"after",
"knowledge...",
"and",
"you",
"call",
"us",
"criminals.",
"We",
"exist",
"without",
"skin",
"color,",
"without",
"nationality,",
"without",
"religious",
"bias...",
"and",
"you",
"call",
"us",
"criminals.",
"You",
"build",
"atomic",
"bombs,",
"you",
"wage",
"wars,",
"you",
"murder,",
"cheat,",
"and",
"lie",
"to",
"us",
"and",
"try",
"to",
"make",
"us",
"believe",
"it's",
"for",
"our",
"own",
"good,",
"yet",
"we're",
"the",
"criminals.",
"Yes,",
"I",
"am",
"a",
"criminal.",
"My",
"crime",
"is",
"that",
"of",
"curiosity.",
"My",
"crime",
"is",
"that",
"of",
"judging",
"people",
"by",
"what",
"they",
"say",
"and",
"think,",
"not",
"what",
"they",
"look",
"like.",
"My",
"crime",
"is",
"that",
"of",
"outsmarting",
"you,",
"something",
"that",
"you",
"will",
"never",
"forgive",
"me",
"for.",
"I",
"am",
"a",
"hacker,",
"and",
"this",
"is",
"my",
"manifesto.",
"You",
"may",
"stop",
"this",
"individual,",
"but",
"you",
"can't",
"stop",
"us",
"all...",
"after",
"all,",
"we're",
"all",
"alike."};

uint32_t SOL[][2] = {
{1, 65},
{1, 114},
{1, 158},
{1, 0},
{2, 23},
{0, 69},
{1, 8},
{2, 18},
{2, 18},
{1, 115},
{1, 91},
{1, 88},
{0, 30},
{0, 55},
{1, 17},
{2, 95},
{1, 6},
{1, 79},
{1, 5},
{0, 65},
{2, 26},
{2, 95},
{0, 75},
{1, 126},
{1, 6},
{1, 17},
{2, 95},
{0, 117},
{2, 92},
{0, 31},
{2, 98},
{2, 66},
{2, 123},
{2, 157}
};

uint32_t HASHES[][3] = {
{408, 2605758, 2089609149},
{220, 3370, 5863489},
{342, 110412, 193501851},
{552, 113318802, 279393645},
{478, 3255308248, 277947587},
{321, 114801, 193506854},
{552, 113318802, 279393645},
{213, 3543, 5863674},
{321, 114801, 193506854},
{860, 4277843426, 504887617},
{307, 96727, 193486360},
{321, 114801, 193506854},
{702, 2491101048, 3043763843},
{321, 114801, 193506854},
{650, 2901938300, 4090720047},
{213, 3543, 5863674},
{321, 114801, 193506854},
{458, 93510368, 253989135},
{188, 2798, 5862881},
{414, 3343854, 2090500003},
{333, 116103, 193508306},
{213, 3543, 5863674},
{97, 97, 177670}
};

uint32_t wrapper(char *s, uint32_t initial, uint32_t(*hash)(uint32_t, char)) {

    uint32_t h = initial;
    char c;

    while (c = *s++) {
      h = hash(h, c);
    }

    return h;
}

static void template(void) {
  asm volatile(
      "nop        \n\t"
      "nop        \n\t"
      "nop        \n\t"
      "nop        \n\t"
      "ret        \n\t"
  :::);
}

void* read_user(void) {
  void *addr = mmap(NULL, PAGESIZE, PROT_READ | PROT_WRITE,
                    MAP_ANONYMOUS | MAP_SHARED, -1, 0);
  memcpy(addr, template, (NNOPS+1)*INSN_SZ);
  read(STDIN_FILENO, addr, NNOPS*INSN_SZ);
  mprotect(addr, PAGESIZE, PROT_READ | PROT_EXEC);
  return addr;
}


int main() {

  uint32_t kr1_h;
  uint32_t kr2_h;
  uint32_t djb_h;
  void *f,*g,*h;

  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  f = read_user();
  size_t manifesto_sz = sizeof(HASHES)/(3*sizeof(uint32_t));
  for(int i = 0; i < manifesto_sz; i++) {
    kr1_h = wrapper(MANIFESTO[i], 0, (uint32_t (*)(uint32_t, char))f);
    if (HASHES[i][0] != kr1_h) {
      printf("STAGE 1: NOPE\n");
      abort();
    }
  }
  printf("STAGE 1 CLEARED\n");

  g = read_user();
  for(int i = 0; i < manifesto_sz; i++) {
    kr2_h = wrapper(MANIFESTO[i], 0, (uint32_t (*)(uint32_t, char))g);
    if (HASHES[i][1] != kr2_h) {
      printf("STAGE 2: NOPE\n");
      abort();
    }
  }
  printf("STAGE 2 CLEARED\n");

  h = read_user();
  for(int i = 0; i < manifesto_sz; i++) {
    djb_h = wrapper(MANIFESTO[i], 5381, (uint32_t (*)(uint32_t, char))h);
    if (HASHES[i][2] != djb_h) {
      printf("STAGE 3: NOPE\n");
      abort();
    }
  }
  printf("STAGE 3 CLEARED\n");

  size_t SOL_SZ = sizeof(SOL)/(2*sizeof(uint32_t));
  for(int i = 0; i < SOL_SZ; i++) {
    uint32_t hash;
    if(SOL[i][0] == 0) {
      hash = wrapper(MANIFESTO[SOL[i][1]], 0, (uint32_t (*)(uint32_t, char))f);
    } else if (SOL[i][0] == 1) {
      hash = wrapper(MANIFESTO[SOL[i][1]], 0, (uint32_t (*)(uint32_t, char))g);
    } else if (SOL[i][0] == 2) {
      hash = wrapper(MANIFESTO[SOL[i][1]], 5381, (uint32_t (*)(uint32_t, char))h);
    }

    int idx = hash % sizeof(ALPHABET);
    printf("%c", ALPHABET[idx]);
  }
  return 0;
}

