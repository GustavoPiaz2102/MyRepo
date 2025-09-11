#ifndef ITENS_H
#define ITENS_H
#include <iostream>
#include <string>
#include "lowscale.h"

//==========================================================================================

class sword : public item {
    private:
        float damage;
        float durability;
        bool repairable;
    public:
        sword(std::string itemName="", int itemID=0, bool stackable=false, bool usable=false, bool equippable=true, bool vendable=true, float damage=10.0f, float durability=100.0f, bool repairable=true);
        void setDamage(float damage);
        void setDurability(float durability);
        float getDamage() const;
        float getDurability() const;
        void use();
        bool isRepairable() const;
        void repair(float amount);
};

//==========================================================================================

class armor : public item {
    private:
        float defense;
        float durability;
        bool repairable;
    public:
        armor(std::string itemName="", int itemID=0, bool stackable=false, bool usable=false, bool equippable=true, bool vendable=true, float defense=5.0f, float durability=100.0f, bool repairable=true);
        void setDefense(float defense);
        void setDurability(float durability);
        float getDefense() const;
        float getDurability() const;
        void use();
        bool isRepairable() const;
        void repair(float amount);
};

//==========================================================================================
#endif // ITENS_H