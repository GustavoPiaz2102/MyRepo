#include "perceptron.h"

//==========================FUNCTIONS=========================//
int activation(float val)
{
    if (val >= 0.0)
        return 1;
    else
        return 0;
}
void train(float *weights, float *bias, FILE *arq, float **data, int NumExemples)
{
    float menorErro = 10000;
    int EpochComMenorErro = 0;
    float erro, ErroTotal;
    float soma;

    for (int epochs = 0; epochs < Epochs; epochs++)
    {
        printf("Epoch %d ", epochs + 1);
        fprintf(arq, "Epoch %d: Weights: [%f, %f], Bias: %f\n",
                epochs + 1, weights[0], weights[1], *bias);

        ErroTotal = 0.0;

        for (int i = 0; i < NumExemples; i++)
        {
            soma = data[i][0] * weights[0] + data[i][1] * weights[1] + *bias;
            int v = activation(soma);
            erro = data[i][2] - v;

            if (erro != 0)
            {
                ErroTotal += fabs(erro);
                // Att taxa de aprendizado
                weights[0] += LeaningRate * erro * data[i][0];
                weights[1] += LeaningRate * erro * data[i][1];
                *bias += LeaningRate * erro;
            }
        }
        printf("Erro: %f\n",ErroTotal);
        if(ErroTotal<menorErro){
            menorErro = ErroTotal;
            EpochComMenorErro = epochs;
        }
        if (ErroTotal == 0)
            break;

    }
    printf("Melhor Epoch: %d\nMenor Erro: %f\n",EpochComMenorErro,menorErro);
}
int test(float *weights, float *bias, float **data, int NumExemples)
{
    FILE *ArquivoSaveTest = fopen("TestResults.txt", "w");
    for(int i = 0; i < NumExemples; i++)
    {
        float soma = data[i][0] * weights[0] + data[i][1] * weights[1] + *bias;
        int v = activation(soma);
        fprintf(ArquivoSaveTest, "Input: [%f, %f], Expected: %f, Predicted: %d\n", data[i][0], data[i][1], data[i][2], v);
    }
}

int main()
{
    FILE *ArquivoSave = fopen("data.txt", "w");
    FILE *ArqLeitura = fopen("datasets/nonlinear.csv", "r");
    if (ArquivoSave == NULL || ArqLeitura == NULL)
    {
        printf("erro na abertura dos arquivos\n");
        return 1;
    }
    float **dataTotal = NULL;
    int i = 0;
    float x, y, out;

    while (fscanf(ArqLeitura, "%f,%f,%f", &x, &y, &out) == 3)
    {
        dataTotal = realloc(dataTotal, (i + 1) * sizeof(float *));
        dataTotal[i] = malloc(3 * sizeof(float));
        dataTotal[i][0] = x;
        dataTotal[i][1] = y;
        dataTotal[i][2] = out;
        i++;
    }
    // separando train e test (70/30)
    int trainSize = (int)(i * 0.7);
    float **dataTrain = malloc(trainSize * sizeof(float *));
    for (int j = 0; j < trainSize; j++)
    {
        dataTrain[j] = malloc(3 * sizeof(float));
        dataTrain[j][0] = dataTotal[j][0];
        dataTrain[j][1] = dataTotal[j][1];
        dataTrain[j][2] = dataTotal[j][2];
    }
    int testSize = (int)(i - trainSize);
    float **dataTest = malloc(testSize * sizeof(float *));
    for (int j = 0; j < testSize; j++)
    {
        dataTest[j] = malloc(3 * sizeof(float));
        dataTest[j][0] = dataTotal[j + trainSize][0];
        dataTest[j][1] = dataTotal[j + trainSize][1];
        dataTest[j][2] = dataTotal[j + trainSize][2];
    }
    for (int j = 0; j < i; j++)
    {
        free(dataTotal[j]);
    }
    free(dataTotal);

    fclose(ArqLeitura);
    float *weights = (float *)malloc(2 * sizeof(float));
    float bias = 0.0f;
    srand(time(NULL));
    for (int i = 0; i < 2; i++)
    {
        weights[i] = ((float)rand() / RAND_MAX - 0.5f) * 0.1f;
    }
    bias = 0.0f;
    train(weights, &bias, ArquivoSave, dataTrain, trainSize);
    fclose(ArquivoSave);
    test(weights, &bias, dataTest, testSize);
    // printf("Output: %d\n", output);
    free(weights);
    return 0;
}