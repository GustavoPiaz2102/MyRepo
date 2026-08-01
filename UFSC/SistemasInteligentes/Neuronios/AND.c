#include <stdio.h>

#define w1 1 
#define w2 1
#define teta 2

int and(int x1,int x2){
    if((x1*w1)+(x2*w2)>=teta){
        return 1;
    }
    else return 0;
}

int main(){
    int x1,x2;
    while (1){
        printf("Digite o valor do x1\n");
        scanf("%d",&x1);
        printf("Digite o valor do x2\n");
        scanf("%d",&x2);
        printf("Valor do AND : %d\n",and(x1,x2));
    }
}