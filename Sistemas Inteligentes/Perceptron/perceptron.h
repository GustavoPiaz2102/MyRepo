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

//==========================DEFINES===========================//

#define Epochs 1000
#define LeaningRate 0.1

//==========================STRUCTURES========================//

void train(float *weights, float *bias, FILE *arq);
int test(float *weights, float *bias);
int activation(float val);

#endif
