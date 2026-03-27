// main.c
#include <stdio.h>

// Declaração da função definida no arquivo capture.s
extern void run_camera_capture_asm();

int main() {
    printf("--- Iniciando Captura ASCII via Assembly ---\n");
    printf("Abra o terminal em tela cheia para melhor visualização.\n");
    printf("Pressione Ctrl+C para encerrar.\n\n");

    // Chamar a função Assembly
    run_camera_capture_asm();

    // Esta linha nunca será alcançada devido ao loop infinito no Assembly
    return 0;
}