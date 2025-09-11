#include "itens.h"

//==========================================================================================

//SWORD CLASS

sword::sword(std::string itemName, int itemID, bool stackable, bool usable, bool equippable, bool vendable, float damage, float durability, bool repairable)
    : item(itemName, itemID, stackable, usable, equippable, vendable), damage(damage), durability(durability), repairable(repairable) {}
void sword::setDamage(float damage) {
    this->damage = damage;
}
void sword::setDurability(float durability) {
    this->durability = durability;
}
float sword::getDamage() const {
    return damage;
}
float sword::getDurability() const {
    return durability;
}
void sword::use() {
    if (durability > 0) {
        durability -= 1.0f; // Decrease durability on use
        if (durability < 0) {
            durability = 0;
        }
    }
}
bool sword::isRepairable() const {
    return repairable;
}
void sword::repair(float amount) {
    if (repairable) {
        durability += amount;
        if (durability > 100.0f) { // Assuming max durability is 100
            durability = 100.0f;
        }
    }
}

//END SWORD CLASS

//==========================================================================================

//ARMOR CLASS

armor::armor(std::string itemName, int itemID, bool stackable, bool usable, bool equippable, bool vendable, float defense, float durability, bool repairable)
    : item(itemName, itemID, stackable, usable, equippable, vendable), defense(defense), durability(durability), repairable(repairable) {}
void armor::setDefense(float defense) {
    this->defense = defense;
}
void armor::setDurability(float durability) {
    this->durability = durability;
}
float armor::getDefense() const {
    return defense;
}
float armor::getDurability() const {
    return durability;
}
void armor::use() {
    if (durability > 0) {
        durability -= 0.5f; // Decrease durability on use
        if (durability < 0) {
            durability = 0;
        }                                                       
    }
}
bool armor::isRepairable() const {                                                                      
    return repairable;
}
void armor::repair(float amount) {
    if (repairable) {
        durability += amount;
        if (durability > 100.0f) { // Assuming max durability is 100
            durability = 100.0f;
        }
    }
}

//END ARMOR CLASS

//==========================================================================================
