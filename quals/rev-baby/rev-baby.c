#include <stdio.h>

int main(){
    unsigned int number;
    printf("What's your your number:");
    fflush(stdout);
    scanf("%u", &number);
    if (number < 1<<16 || number > 1<<31) {
        printf("Bad number >:-(\n");
        return 0;
    }

    unsigned int new_number = 0;
    
    for(size_t i=0;i < sizeof(unsigned int)*8; ++i){
        new_number = new_number << 1;
        new_number += (number>>i)&1;
    }

    if(number!=new_number){
        printf("Bad number >:-(\n");
        return 0;
    }

    FILE* fd = fopen("flag.txt", "r");
    
    //necessary?
    if(fd == NULL){
        printf("No flag found\n");
        return -1;
    }
    
    size_t size = 0;
    char *line = NULL;
    ssize_t line_size = getline(&line, &size, fd);
    
    if(fd == NULL){
        printf("No flag found\n");
        return -1;
    }

    if(line_size==-1){
        printf("Unable to read flag\n");
        return -1;
    }

    printf("%s", line);
    
    return 0;

}
