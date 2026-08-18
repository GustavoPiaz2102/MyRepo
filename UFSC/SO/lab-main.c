#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

#define N 25 // tamanho do vetor
#define K 5  // numero de processos filhos
#define FATIA (N / K)
#define LIMIAR 5.75 // conta valores ACIMA deste limiar

double vetor[N];

/* Le os N numeros (ponto flutuante) do vetor a partir dos argumentos da
 *  linha de comando em vetor[N]. Ja esta pronto, nao precisa mexer aqui.
 *
 *  Para testar localmente, rode:
 *   gcc -Wall lab-main.c -o lab-main && ./lab-main 3.50 7.25 8.75 1.00
 * 0.25 10.00 6.50 4.25 9.75 2.50 5.75 8.00 7.75 6.25 3.25 10.00
 * 0.50 1.75 9.50 4.50 6.75 8.25 2.25 7.50 5.50
 */

void ler_vetor(int argc, char *argv[]) {
	if (argc != N + 1) {
		fprintf(stderr, "Uso: %s <%d numeros>\n", argv[0], N);
		exit(1);
	}
	for (int i = 0; i < N; i++)
		vetor[i] = atof(argv[i + 1]);
}

int main(int argc, char *argv[]) {
	ler_vetor(argc, argv);
	printf("Pai (PID %d)\n", getpid());
	pid_t pids[K];
	for (int i = 0; i < K; i++) {
		pids[i] = fork();
		if (pids[i] == 0) { // Filho
			int accumuiator = 0;
			for (int j = 0; j < K; j++) {
				if (vetor[i * K + j] >
				    5.75) { // o professor colocou >5.75 , 5.75
					    // já passa grazadeus.
					accumuiator++;
				}
			}
			_exit(accumuiator);
		}
	}
	int total = 0;
	for (int i = 0; i < K; i++) {
		int status;
		waitpid(pids[i], &status, 0);
		// aq o 0 é flag standart, só pra eu lembrar msm, mas da pra
		// usar uma flag para ser n bloqueante
		int ret = WEXITSTATUS(status);
		printf("Filho %d (PID %d): %d valores\n", i, pids[i], ret);
		total += ret;
	}
	printf("Total: %d valores\n", total);
	return 0;
}
/*
PS: Como dizia no enunciado eu não alterei o resto do código mas o format trocou
a identação por \t.
*/