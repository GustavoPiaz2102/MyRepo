#ifndef OBJECTS_H
#define OBJECTS_H
#include "lowscale.h"
#include <iostream>
#include <string>
#include <vector>
#include <random>

//==========================================================================================

class player : public object {
    private:
        float life;
        float damage;
        int level;
        float exp;
        float expToNextLevel;
        float speed;
        float money;
        float armor;
        float mana;
        int direction;  // 0: up, 1: right, 2: down, 3: left
    public:
        player(int x=0, int y=0, bool visible=true, bool HitBox=true, float life=100.0f, float damage=10.0f, int level=1, float exp=0.0f, float expToNextLevel=100.0f, float speed=1.0f, float money=0.0f, float armor=0.0f, float mana=100.0f, int direction=2,std::string name="player");
        void setLife(float life);
        void setDamage(float damage);
        void setLevel(int level);
        void setExp(float exp);
        void setExpToNextLevel(float expToNextLevel);
        void setSpeed(float speed);
        void setMoney(float money);
        void setArmor(float armor);
        void setMana(float mana);
        void setDirection(int direction);
        float getLife() const;
        float getDamage() const;
        int getLevel() const;
        float getExp() const;
        float getExpToNextLevel() const;
        float getSpeed() const;
        float getMoney() const;
        float getArmor() const;
        float getMana() const;
        int getDirection() const;
        void gainExp(float amount);
        void levelUp();
        void move(int deltaX, int deltaY) override;
};

//==========================================================================================

class wall : public object {
    public:
        wall(int x=0, int y=0, bool visible=false, bool HitBox=false, std::string name="wall");
};

//==========================================================================================

class randomChest : public object {
private:
    bool opened;
    int rarity;
    std::vector<double> pesos = {1.0/2048, 1.0/512, 1.0/128, 1.0/32 , 1.0/8, 1.0/2, 1.0};

public:
    randomChest(int x=0, int y=0, bool visible=true, bool HitBox=true, bool opened=false); // removi rarity
    void setOpened(bool opened);
    void setRarity(int rarity);
    bool isOpened() const;
    int getRarity() const;
    void openChest();
    int randomRarity();
};

//==========================================================================================

#endif // OBJECTS_H