#include "interface.h"
#include <iostream>

Interface::Interface(int w, int h, int ps)
    : width(w), height(h), pixelSize(ps),
      window(sf::VideoMode(sf::Vector2u(w * ps, h * ps)), "Mapa de Objetos") {}

Interface::~Interface() {
    window.close();
}

void Interface::render(const std::vector<std::vector<object*>>& frameBuffer) {
    // Loop de eventos SFML 3 (pollEvent agora retorna std::optional)
    while (auto event = window.pollEvent()) {
        if (event->is<sf::Event::Closed>())
            window.close();
    }

    window.clear();

    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            if (frameBuffer[i][j] && frameBuffer[i][j]->isVisible()) {
                // Criar sprite com textura obrigatoriamente
                const sf::Texture& tex = frameBuffer[i][j]->getTexture();
                sf::Sprite sprite(tex);

                sprite.setPosition(sf::Vector2f(
                    static_cast<float>(j * pixelSize),
                    static_cast<float>(i * pixelSize)
                ));

                sprite.setScale(sf::Vector2f(
                    static_cast<float>(pixelSize) / tex.getSize().x,
                    static_cast<float>(pixelSize) / tex.getSize().y
                ));


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
