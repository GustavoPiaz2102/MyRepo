#include "perceptron.h"

//==========================FUNCTIONS=========================//
int activation(float val){
    if(val >= 0.0) return 1;
    else return 0;
}
void train(float *weights){
    int Inputs[4][2] = {{0,0},{0,1},{1,0},{1,1}};
    int Outs[4] = {0,0,0,1};
    float bias = 0.0;

    for(int i = 0;i<Epochs;i++){
        for (int j = 0;j<4;j++){
            float e=0.0;
            float soma=0.0;
            for(int k = 0;k<2;k++){
            soma += Inputs[j][k]*weights[k];
            }
            soma += bias;
            for(int k = 0;k<2;k++){
            if(activation(soma) != Outs[j]){
            e += Outs[j]-activation(soma);
            weights[k]+= LeaningRate*e*Inputs[j][k];
            }
        }
        bias += LeaningRate*e;
        }
        printf("Epoch: %d, Weights: [%f, %f], Bias: %f\n",i,weights[0],weights[1],bias);
        
    }
}
int test(float *weights){
    int val1=0,val2=0;
    printf("Digite o primeiro valor (0 ou 1): ");
    scanf("%d",&val1);
    printf("Digite o segundo valor (0 ou 1): ");   
    scanf("%d",&val2);
    float soma = val1*weights[0] + val2*weights[1];
    return activation(soma);
}

int main(){
    float *weights = (float*) malloc(2*sizeof(float));
    srand(time(NULL));
    for(int i = 0;i<2;i++){
        weights[i] = (float)rand()/(float)(RAND_MAX);
    }
    train(weights);
    int output = test(weights);
    printf("Output: %d\n",output);
    free(weights);
    return 0;
}