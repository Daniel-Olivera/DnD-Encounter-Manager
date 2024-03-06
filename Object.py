class Object:
    objType = -1
    
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