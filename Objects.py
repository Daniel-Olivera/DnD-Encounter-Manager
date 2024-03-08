# Defines a generic object. Objects have an ID known as objType which denotes
# if it is an item, a character or an enemy. Objects can populate Cells on the grid.
# There can be multiple objects on a grid cell.  
class Object:
    objType = -1
    
    x = 0
    y = 0
    
    # TYPE_ITEM = 0
    # TYPE_ENEMY = 1
    # TYPE_CHARACTER = 2
    
    name = ""
    description = ""
    
    def __init__(self, objType, name, desc):
        self.name = name
        self.objType = objType
        self.description = desc
    
    def getType(self):
        return self.objType
    
    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def getPos(self):
        return (self.x, self.y)
    
    def setPos(self, newX, newY):
        self.x = newX
        self.y = newY
    

# An item is a subclass of an object. Items can be owned by enemies or players.
# Items may also be un-owned. These can range from magic items, to just swords or barrels
class Item(Object):
    
    owner = None
    
    def __init__(self, name, desc):
        self.objType = 0
        self.name = name
        self.description = desc
    
    def getOwner(self):
        return self.owner
    
    def setOwner(self, newOwner):
        self.owner = newOwner
        
    def __str__(self):
        return "\tName: {0}\n\tDescription: {1}".format(self.getName(), self.getDescription())

# Slightly vague as a Character can be expressed as a player or an enemy.
# Will store info like how healthy they are and how many spell slots are remaining, etc.
# Players or enemies can also have items which are defined above, but not objects.
# Character items are a list because a character may have many duplicates of an item such as 2 daggers.
class Character(Object):
    
    TYPE_ENEMY = 1
    TYPE_CHARACTER = 2
    
    health = 0
    items = []
    
    def __init__(self, objType, name, desc, hp):
        self.objType = objType
        self.name = name
        self.description = desc
        self.health = hp
        self.items = []
        
    def getHP(self):
        return self.health
    
    def getItems(self):
        return self.items
    
    def removeItem(self, item):
        self.items.remove(item)
        
    def giveItem(self, item):
        self.items.append(item)
        
    def __str__(self):
        return "Name: {0}\nDescription: {1}\nHP: {2}\nItems: ".format(self.getName(), self.getDescription(), self.getHP())