/*

Nome: Gustavo Piaz Da Silva
Matrícula: 23200958

Implementação de um Perceptron AND



Funcionamento

SOMA(Entradas*Pesos) + Bias -> Função de Ativação -> Saída

*/

//==========================INCLUDES==========================//
#ifndef PERCEPTRON_H
#define PERCEPTRON_H
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
//==========================DEFINES===========================//

#define Epochs 200
#define LeaningRate 0.0001f

//==========================STRUCTURES========================//

void train(float *weights, float *bias, FILE *arq, float** data,int NumExemples);
int test(float *weights, float *bias, float** data,int NumExemples);
int activation(float val);

#endif
