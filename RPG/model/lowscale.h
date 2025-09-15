#ifndef LOWSCALE_H
#define LOWSCALE_H
#include <iostream>
#include <string>
#include <vector>
#include <SFML/Graphics.hpp>
//==========================================================================================

class object{
    private:
        bool visible;
        bool HitBox;
        std::string name;
        int id;
        sf::Texture texture;

    public:
        object(bool visible=true, bool HitBox=true, std::string name="object", std::string TexturePath="../textures/Pixel.png");
        void setTexture(std::string TexturePath);
        sf::Texture& getTexture();
        void setVisible(bool visible);
        void setHitBox(bool HitBox);
        bool isVisible() const;
        bool hasHitBox() const;
        std::string getName();
        void setName(const std::string& name);

};

//==========================================================================================

class item{
    private:
        std::string itemName;
        int itemID;
        bool stackable;
        bool usable;
        bool equippable;
        bool vendable;
        float value;
        std::string description;
    public:
        item(std::string itemName="", int itemID=0, bool stackable=true, bool usable=false, bool equippable=false, bool vendable=true);
        void setItemName(const std::string& itemName);
        void setItemID(int itemID);
        void setStackable(bool stackable);
        void setUsable(bool usable);
        void setEquippable(bool equippable);
        void setVendable(bool vendable);
        std::string getItemName() const;
        int getItemID() const;
        bool isStackable() const;
        bool isUsable() const;
        bool isEquippable() const;
        bool isVendable() const;
        void setValue(float value);
        float getValue() const;
        void setDescription(const std::string& description);
        std::string getDescription() const;
};

//==========================================================================================

#endif // LOWSCALE_H