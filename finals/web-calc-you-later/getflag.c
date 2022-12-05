#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
    FILE* secret_f = fopen("/secret", "r");
    char secret[100] = {0};
    fgets(secret, sizeof(secret), secret_f);
    if (argc < 2 || strcmp(argv[1], secret)) {
        puts("Please provide the secret from `/app/config/credentials.yml.enc` as argv[1]");
    } else {
        FILE* flag_f = fopen("/flag", "r");
        char flag[100] = {0};
        fgets(flag, sizeof(flag), flag_f);
        puts(flag);
    }
}
