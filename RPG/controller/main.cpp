#include "../view/interface.h"
#include "../model/itens.h"
#include "../model/objects.h"
#include <vector>

#define WallPath "../textures/Wall.png"
#define GrassPath "../textures/Grass.png"
#define PixelPath "../textures/Pixel.png"

int main() {
    const int size = 50;
    const int pixelSize = 16;
    const int width = size;
    const int heigth = (int)(size/1.7);
    // Inicializa interface
    Interface ui(width,heigth , pixelSize);

    // Cria frameBuffer
    std::vector<std::vector<object*>> frameBuffer(
        size, std::vector<object*>(size, nullptr)
    );
    object* grass = new object(true, true, "grass", GrassPath);
    object* pixel = new object(false, false, "pixel", PixelPath);
    object* wall = new object(true, true, "wall", WallPath);
    randomChest* chest = new randomChest(true, true, false);

    for(int i = 0; i < heigth; ++i) {
        for(int j = 0; j < width; ++j) {
            if(i == 0) {
                frameBuffer[i][j] = wall;
            } else if(i == heigth-1) {
                frameBuffer[i][j] = grass;
            } else if(i == heigth - 2 && j == width-2) {
                frameBuffer[i][j] = chest;
            } else {
                frameBuffer[i][j] = pixel;
            }
        }
    }
    

    // Loop principal
    while(ui.isOpen()) {
        ui.render(frameBuffer);
    }
    for(int i = 0; i < size; ++i)
        for(int j = 0; j < size; ++j)
            delete frameBuffer[i][j];
}
