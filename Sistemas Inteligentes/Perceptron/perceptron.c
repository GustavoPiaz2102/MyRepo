#include "perceptron.h"

//==========================FUNCTIONS=========================//
int activation(float val)
{
    if (val >= 0.0)
        return 1;
    else
        return 0;
}
void train(float *weights, float *bias)
{
    int Inputs[4][2] = {{0, 0}, {0, 1}, {1, 0}, {1, 1}};
    int Outs[4] = {0, 0, 0, 1};
    float erro = 0.0, ErroTotal = 0.0;
    float soma;
    for (int epochs = 0; epochs < Epochs; epochs++)
    {
        soma = 0.0;
        ErroTotal = 0.0;
        erro = 0.0;
        for (int i = 0; i < 4; i++)
        {

            for (int j = 0; j < 2; j++)
            {
                soma += Inputs[i][j] * weights[j];
            }
            soma += *bias;
            int v = activation(soma);
            erro = Outs[i] - v;
            if (erro != 0)
                ErroTotal += erro;

            // Atualização de valores
            for (int j = 0; j < 2; j++)
            {
                weights[j] += LeaningRate * erro * Inputs[i][j];
            }
            *bias += LeaningRate * erro;
        }
        if (ErroTotal == 0)
            break;
    }
}
int test(float *weights, float *bias)
{
    int val1 = 0, val2 = 0;
    printf("Digite o primeiro valor (0 ou 1): ");
    scanf("%d", &val1);
    printf("Digite o segundo valor (0 ou 1): ");
    scanf("%d", &val2);
    float soma = val1 * weights[0] + val2 * weights[1] + *bias;
    return activation(soma);
}

int main()
{
    float *weights = (float *)malloc(2 * sizeof(float));
    float bias = 0.0;
    srand(time(NULL));
    for (int i = 0; i < 2; i++)
    {
        weights[i] = (float)rand() / (float)(RAND_MAX);
    }
    train(weights, &bias);
    int output = test(weights, &bias);
    printf("Output: %d\n", output);
    free(weights);
    return 0;
}