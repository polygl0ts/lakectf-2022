#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const size_t alphaLength = 65;
char alphabet[65] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_";

typedef struct node {
	int number;
	char encoding;
	struct node *next;
} node_t;

/*
void computeBackref(node_t** n,size_t size){
	int tot = 0;
	int max = 0;
	for(int i = 0; i < size; i++){
		if(n[i]->backref > 1){
			tot += 1;
			if(max < n[i]->backref)
				max = n[i]->backref;
		}

	}

	printf("Total of multiple backref is %d\n", tot);
	printf("Max num of backref on one node is %d\n", max);
}
*/	

int isPrime(int n) {
	int  i, c = 0;

  for (i = 1; i <= n; i++) {
		if (n % i == 0) {
   		c++;
		}

		if(c > 2) 
			return 0;
  }

	if (c == 2) {
		return 1;
	} else {
		return 0;
	}
}

int isPeriodBig(int n) {
	int i= 10;
	int steps = 1;
	while(i != 1){
		i*=10;
		i=i%n;
		++steps;
	}
	return steps == n - 1;
	
	
	
}


void buildGraph(node_t** n, size_t size, int interval) {
	for (int i=0; i<size; i++) {
		node_t* node = malloc(sizeof(node_t));
     	n[i] = node;
		n[i]->number = i;
		
		if(i % (interval) == 0 && (i / interval) < 65){
			n[i]->encoding = alphabet[i/interval];
		} else {
			n[i]->encoding = 0;
		}
		
	}

}

void connectGraph(node_t** n, size_t size) {

	for(int i=0; i < size; i++){
		
		if(i == 0){

			n[i]->next = NULL;

		} else {

			int d = i;
			int rest;
			d *= 10;
			
			if(d < size){
				rest = d;
			}else {
				rest = d - (d/size * size);
			}
			
			n[i]->next = n[rest];
		}
	}
}


void encrypt(char* flag, node_t** n, size_t graphSize, int interval) {

	int prevFib = 0;
	int fib = 1;
	char* out = malloc(strlen(flag) + 1);
	out[strlen(flag)] = '\0';
	
	for(int i = 0; i < strlen(flag); i++){
	
		char * pos = strchr(alphabet, flag[i]);
		if(pos == NULL){
			printf("Invalid character, can't encrypt it\n");
			exit(0);
		}
		
		
		int index = (int) (pos - alphabet);
	
	
		struct node* encNode = n[index * interval];
		
		if (!encNode->next) {
			out[i] = *pos;
		} else {
			int j = 0;
			while( j < fib%(alphaLength - 1)){
				encNode = encNode->next;
				if(encNode->encoding)
					j++;
			}
			
			out[i] = encNode->encoding;
		}
		
		
		int tmp = fib;
		fib += prevFib;
		prevFib = tmp;
		
	}
	
	printf("Encrypted message : %s\n",out);
}


int main(void) {
		

	//char* flag = "EPFL{7h3_r3cipr0c4l_0f_prim35_4r3_r3p347in9}"; 
	char msg[45];
	
	printf("Welcome to the encryption service of the swiss army. Please enter the message you want to encrypt and the secret key you want to encrypt it with.\n");
	printf("Message :\n");
	if(fgets(msg, 45, stdin) == NULL){
		printf("Could not read input\n");
	}
	
	msg[strcspn(msg, "\n")] = '\0';
	int input;
	printf("Secret key : \n");
	if (scanf("%d", &input)	== EOF) {
		printf("Error reading secret key. Exiting\n");
		exit(0);
	}

	
	if(input < 66 || !isPrime(input) || !isPeriodBig(input) || input > 200000) {
		printf("Please provide a nicer key, I don't like this one\n");
		return 0;
	}
		
	size_t graphSize = input;

	
	node_t **n = (node_t **) malloc(sizeof(node_t *) * graphSize);

	// Populate the array with pointers.
	int interval = (int)(graphSize/alphaLength);
	buildGraph(n, graphSize, interval);
	connectGraph(n, graphSize);
	
	encrypt(msg, n, graphSize, interval);
}


