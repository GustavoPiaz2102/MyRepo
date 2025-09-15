#include "objects.h"

//==========================================================================================

//PLAYER CLASS

player::player(int x, int y, bool visible, bool HitBox, float life, float damage, int level, float exp, float expToNextLevel, float speed, float money, float armor, float mana, int direction,std::string name)
    : object(visible, HitBox,name), life(life), damage(damage), level(level), exp(exp), expToNextLevel(expToNextLevel), speed(speed), money(money), armor(armor), mana(mana), direction(direction) {}
void player::setLife(float life) {
    this->life = life;
}
void player::setDamage(float damage) {
    this->damage = damage;
}
void player::setLevel(int level) {
    this->level = level;
}
void player::setExp(float exp) {
    this->exp = exp;
}
void player::setExpToNextLevel(float expToNextLevel) {
    this->expToNextLevel = expToNextLevel;
}
void player::setSpeed(float speed) {
    this->speed = speed;
}
void player::setMoney(float money) {
    this->money = money;
}
void player::setArmor(float armor) {
    this->armor = armor;
}
void player::setMana(float mana) {
    this->mana = mana;
}
void player::setDirection(int direction) {
    this->direction = direction;
}
float player::getLife() const {
    return life;
}
float player::getDamage() const {
    return damage;
}
int player::getLevel() const {
    return level;
}
float player::getExp() const {
    return exp;
}
float player::getExpToNextLevel() const {
    return expToNextLevel;
}
float player::getSpeed() const {
    return speed;
}
float player::getMoney() const {
    return money;
}
float player::getArmor() const {
    return armor;
}
float player::getMana() const {     
    return mana;
}
int player::getDirection() const {
    return direction;
}
void player::gainExp(float amount) {
    exp += amount;
    while (exp >= expToNextLevel) {
        levelUp();
    }
}
void player::levelUp() {
    exp -= expToNextLevel;
    level++;
    expToNextLevel *= 1.5f; // Increase the required EXP for the next level
    life += 20.0f;          // Increase life on level up
    damage += 5.0f;         // Increase damage on level up
    mana += 10.0f;          // Increase mana on level up
}
void player::move(int deltaX, int deltaY) {
    x += deltaX * speed;
    y += deltaY * speed;
}

//END PLAYER CLASS

//==========================================================================================

//RANDOM CHEST CLASS

randomChest::randomChest(bool visible, bool HitBox, bool opened)
    : object(visible, HitBox,"chest"), opened(opened), rarity(randomRarity()) {
        object::setTexture("../textures/Tier" + std::to_string(rarity) + "Chest.png");
    }
void randomChest::setOpened(bool opened) {
    this->opened = opened;
}
void randomChest::setRarity(int rarity) {
    this->rarity = rarity-1;
}
bool randomChest::isOpened() const {
    return opened;
}
int randomChest::getRarity() const {
    return rarity;
}
void randomChest::openChest() {
    if (!opened) {
        opened = true;
        if(rarity == 0) {
            rarity = randomRarity();
        }
        // logica de drop
    }
}
int randomChest::randomRarity() {
    static bool initialized = false;
    if(!initialized) {
        srand((unsigned)time(NULL));  // inicializa o rand uma vez
        initialized = true;
    }

    std::vector<int> pesos = {4096, 1024, 256, 64, 16, 4};
    int total = 0;
    for(auto p : pesos) total += p;

    int randomValue = rand() % total;

    for(int i = 0; i < pesos.size(); i++) {
        if(randomValue < pesos[i]) return i;
        randomValue -= pesos[i];
    }
    return pesos.size() - 1; // fallback
}
