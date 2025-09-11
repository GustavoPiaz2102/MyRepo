#include "../view/interface.h"
#include "../model/itens.h"
#include "../model/objects.h"
#include <vector>

int main() {
    const int size = 160;
    const int pixelSize = 4;

    // Inicializa interface
    Interface ui(size, size, pixelSize);
    ui.loadTextures();

    // Cria frameBuffer
    std::vector<std::vector<object*>> frameBuffer(
        size, std::vector<object*>(size, nullptr)
    );

    // Preenche frameBuffer
    for(int i = 0; i < size; ++i){
        for(int j = 0; j < size; ++j){
            if(i == size-2 && j == 1)
                frameBuffer[i][j] = new player(i, j, true, true, 100.0f, 10.0f, 1, 0.0f, 100.0f, 1.0f, 0.0f, 5.0f, 0);
            else if(i == 0 || i == size-1)
                frameBuffer[i][j] = new wall(i, j, true, true, "wall");
            else
                frameBuffer[i][j] = new object(i, j, true, false, "pixel");
        }
    }

    // Loop principal
    while(ui.isOpen()) {
        ui.render(frameBuffer);
    }

    // Limpa memória
    for(int i = 0; i < size; ++i)
        for(int j = 0; j < size; ++j)
            delete frameBuffer[i][j];
}
