#include <stdio.h>

extern int multiplicar(int a);

int main(){
	int a = 10;
	printf("\n%d\n",multiplicar(a));
	return 0;
}