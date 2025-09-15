#include "lowscale.h"

//==========================================================================================


//OBJECT CLASS

//==========================================================================================

object::object(bool visible, bool HitBox, std::string name,std::string TexturePath)
    : visible(visible), HitBox(HitBox), name(name) {
    setTexture(TexturePath);
    }

//carrega a textura
void object::setTexture(std::string TexturePath) {
    if(!texture.loadFromFile(TexturePath)) {
        std::cerr << "Erro ao carregar textura de " << name << " de " << TexturePath << "\n";
    }
}
sf::Texture& object::getTexture() {
    return texture;
}
void object::setVisible(bool visible) {
    this->visible = visible;
}
void object::setHitBox(bool HitBox) {
    this->HitBox = HitBox;
}

bool object::isVisible() const {
    return visible;
}
bool object::hasHitBox() const {
    return HitBox;
}

std::string object::getName() {
    return name;
}
void object::setName(const std::string& name) {
    this->name = name;
}

//END OBJECT CLASS

//==========================================================================================

//ITEM CLASS

item::item(std::string itemName, int itemID, bool stackable, bool usable, bool equippable, bool vendable)
    : itemName(itemName), itemID(itemID), stackable(stackable), usable(usable), equippable(equippable), vendable(vendable), value(0.0f) {}
void item::setItemName(const std::string& itemName) {
    this->itemName = itemName;
}
void item::setItemID(int itemID) {
    this->itemID = itemID;
}
void item::setStackable(bool stackable) {
    this->stackable = stackable;
}
void item::setUsable(bool usable) {
    this->usable = usable;
}
void item::setEquippable(bool equippable) {
    this->equippable = equippable;
}
void item::setVendable(bool vendable) {
    this->vendable = vendable;
}
std::string item::getItemName() const {
    return itemName;
}
int item::getItemID() const {
    return itemID;
}
bool item::isStackable() const {
    return stackable;
}
bool item::isUsable() const {
    return usable;
}
bool item::isEquippable() const {
    return equippable;
}
bool item::isVendable() const {
    return vendable;
}
void item::setValue(float value) {
    this->value = value;
}
float item::getValue() const {
    return value;
}
void item::setDescription(const std::string& description) {
    this->description = description;
}
std::string item::getDescription() const {
    return description;
}

//END ITEM CLASS

//==========================================================================================