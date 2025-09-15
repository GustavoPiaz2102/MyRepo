#include "interface.h"
#include <iostream>

Interface::Interface(int w, int h, int ps)
    : width(w), height(h), pixelSize(ps),
      window(sf::VideoMode(w * ps, h * ps), "Mapa de Objetos") {}

Interface::~Interface() {
    window.close();
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
                sprite.setTexture(frameBuffer[i][j]->getTexture());
                sprite.setPosition(j * pixelSize, i * pixelSize);
                sprite.setScale(
                    static_cast<float>(pixelSize) / sprite.getTexture()->getSize().x,
                    static_cast<float>(pixelSize) / sprite.getTexture()->getSize().y
                );
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
