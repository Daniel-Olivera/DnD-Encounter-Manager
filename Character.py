from Object import Object
from Item import Item

class Character(Object):
    
    health = 0
    spellSlots = 0
    items = []
    
    def __init__(self, objType, hp, slots, items):
        self.objType = objType
        self.health = hp
        self.spellSlots = slots
        self.items = items
        
    def getHP(self):
        return self.health
    
    def getSpellSlots(self):
        return self.spellSlots
    
    def getItems(self):
        return self.items
    
    def removeItem(self, index):
        self.items.pop(index)
        
    def giveItem(self, item):
        self.items.append(item)