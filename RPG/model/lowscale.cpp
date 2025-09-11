#include "lowscale.h"

//==========================================================================================

//OBJECT CLASS

object::object(int x, int y, bool visible, bool HitBox, std::string name)
    : x(x), y(y), visible(visible), HitBox(HitBox), name(name) {}
void object::setX(int x) {
    this->x = x;
}
void object::setY(int y) {
    this->y = y;
}
void object::setSizeX(int sizex) {
    this->sizex = sizex;
}
void object::setSizeY(int sizey) {
    this->sizey = sizey;
}
int object::getSizeX() const {
    return sizex;
}
int object::getSizeY() const {
    return sizey;   
}
void object::setVisible(bool visible) {
    this->visible = visible;
}
void object::setHitBox(bool HitBox) {
    this->HitBox = HitBox;
}
int object::getX() const {
    return x;
}
int object::getY() const {
    return y;
}
bool object::isVisible() const {
    return visible;
}
bool object::hasHitBox() const {
    return HitBox;
}
void object::move(int deltaX, int deltaY) {
    x += deltaX;
    y += deltaY;
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