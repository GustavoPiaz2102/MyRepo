#include "interface.h"
#include <iostream>

Interface::Interface(int w, int h, int ps)
    : width(w), height(h), pixelSize(ps),
      window(sf::VideoMode(w * ps, h * ps), "Mapa de Objetos") {}

Interface::~Interface() {
    window.close();
}

bool Interface::loadTextures() {
    if(!wallTexture.loadFromFile(wallFile)) {
        std::cerr << "Erro ao carregar wall texture\n";
        return false;
    }
    if(!pixelTexture.loadFromFile(pixelFile)) {
        std::cerr << "Erro ao carregar pixel texture\n";
        return false;
    }
    if(!playerTexture.loadFromFile(playerFile)) {
        std::cerr << "Erro ao carregar player texture\n";
        return false;
    }
    return true;
}

void Interface::render(const std::vector<std::vector<object*>>& frameBuffer) {
    sf::Event event;
    while (window.pollEvent(event)) {
        if(event.type == sf::Event::Closed)
            window.close();
    }

    window.clear();

    for(int i = 0; i < height; ++i) {
        for(int j = 0; j < width; ++j) {
            if(frameBuffer[i][j] && frameBuffer[i][j]->isVisible()) {
                sf::Sprite sprite;
                std::string name = frameBuffer[i][j]->getName();
                if(name == "wall")
                    sprite.setTexture(wallTexture);
                else if(name == "player")
                    sprite.setTexture(playerTexture);
                else
                    sprite.setTexture(pixelTexture);

                sprite.setPosition(j * pixelSize, i * pixelSize);
                window.draw(sprite);
            }
        }
    }

    window.display();
}

bool Interface::isOpen() const {
    return window.isOpen();
}

void Interface::close() {
    window.close();
}
