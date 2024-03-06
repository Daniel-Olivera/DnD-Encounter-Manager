from Object import Object

class Item(Object):
    
    owner = ""
    
    def __init__(self, name, desc):
        self.objType = 0
        self.name = name
        self.description = desc
    
    def getOwner(self):
        return self.owner
    
    def setOwner(self, newOwner):
        self.owner = newOwner