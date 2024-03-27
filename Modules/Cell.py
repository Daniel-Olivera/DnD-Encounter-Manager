from Modules.Objects import Object

class Cell:
        
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.permanentColor_r = 25
        self.permanentColor_g = 25
        self.permanentColor_b = 30
        self.color_r = 25
        self.color_g = 25
        self.color_b = 30
        self.cellObject = None
    
    def addObject(self, newObject):
        self.cellObject = newObject
        
    def removeObject(self):
        self.cellObject = None
        
    def getXCoord(self):
        return self.x
    
    def getYCoord(self):
        return self.y
    
    def getPos(self):
        return (self.x, self.y)
    
    def getSize(self):
        return self.size
    
    def setSize(self, newSize):
        self.size = newSize
    
    def getItem(self):
        return self.cellObject
    
    def getColor(self):
        return (self.color_r,self.color_g,self.color_b)
    
    def setColor(self, color):
        self.color_r = color[0]
        self.color_g = color[1]
        self.color_b = color[2]
        
    def getPermanentColor(self):
        return (self.permanentColor_r,self.permanentColor_g,self.permanentColor_b)
    
    def setPermanentColor(self, color):
        self.permanentColor_r = color[0]
        self.permanentColor_g = color[1]
        self.permanentColor_b = color[2]
    
    def hasObject(self):
        return self.cellObject != None
    
    def toJson(self):
        if self.cellObject is None:
            data = {"color_r" : self.permanentColor_r, "color_g" : self.permanentColor_g,
                    "color_b" : self.permanentColor_b, "object" : self.cellObject}
        else:
            data = {"color_r" : self.permanentColor_r, "color_g" : self.permanentColor_g,
                    "color_b" : self.permanentColor_b, "object" : self.cellObject.toJson()}
        return data
        
        
        
        