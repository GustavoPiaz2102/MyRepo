#pragma once
#include "../model/objects.h"
#include <SFML/Graphics.hpp>
#include <vector>
#include <string>
// Textures
class Interface {
public:
    Interface(int width, int height, int pixelSize);
    ~Interface();


    // Loop de exibição (desenha o framebuffer na tela)
    void render(const std::vector<std::vector<object*>>& frameBuffer);

    // Verifica se a janela está aberta
    bool isOpen() const;

    // Fecha a janela
    void close();

private:
    sf::RenderWindow window;
    int width;
    int height;
    int pixelSize;
};
