#include <stdio.h>

extern int somar(int a,int b);

int main(){
	int a,b;

	printf("Digite um numero\n");

	scanf("%d",&a);
	printf("Digite um numero\n");

	scanf("%d",&b);
	printf("%d",somar(a,b));
}