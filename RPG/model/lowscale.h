#ifndef LOWSCALE_H
#define LOWSCALE_H
#include <iostream>
#include <string>

//==========================================================================================

class object{
    private:
        int x;
        int y;
        bool visible;
        bool HitBox;
        std::string name;
        int sizex = 1;
        int sizey = 1;
        int id;
    public:
        object(int x=0, int y=0, bool visible=true, bool HitBox=true, std::string name="object");
        void setX(int x);
        void setY(int y);
        void setSizeX(int sizex);
        void setSizeY(int sizey);
        int getSizeX() const;
        int getSizeY() const;
        void setVisible(bool visible);
        void setHitBox(bool HitBox);
        int getX() const;
        int getY() const;
        bool isVisible() const;
        bool hasHitBox() const;
        virtual void move(int deltaX, int deltaY);  
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