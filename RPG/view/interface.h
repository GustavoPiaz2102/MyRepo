#pragma once
#include "../model/objects.h"
#include <SFML/Graphics.hpp>
#include <vector>
#include <string>
// Textures
#define wallFile "../textures/wall.png"
#define pixelFile "../textures/air.png"
#define playerFile "../textures/air.png"

class Interface {
public:
    Interface(int width, int height, int pixelSize);
    ~Interface();

    // Carrega as texturas (chamar antes do loop principal)
    bool loadTextures();

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

    // Texturas
    sf::Texture wallTexture;
    sf::Texture pixelTexture;
    sf::Texture playerTexture;
};
