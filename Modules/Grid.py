from Modules.Cell import Cell

# Manages the gameboard, allowing the user to add/remove items on cells
# or move items from cell to cell.
class Grid:
    
    def __init__(self, size, cellSize):
        self.size = size
        self.cellSize = cellSize
        self.numCells = pow(size,2)
        self.cells = []
        for i in range(0,size):
            for j in range(0,size):
                self.cells.append(Cell(i,j,cellSize))
                
    def getCells(self):
        return self.cells
    
    def getSize(self):
        return self.size
    
    def getNumCells(self):
        return self.numCells
    
    def getCellSize(self):
        return self.cellSize
    
    def setGridSize(self, newSize):
        self.size = newSize
        self.numCells = pow(newSize, 2)
        
    def setCellSize(self, newCellSize):
        self.cellSize = newCellSize
        for cell in self.cells:
            cell.setSize(newCellSize)
        
    def findCell(self, x, y):
        for cell in self.cells:
            if cell.getXCoord() == x and cell.getYCoord() == y:
                return cell
        
    def addObjectToCell(self, x, y, obj):
        cell = self.findCell(x,y)
        cell.addObject(obj)
        obj.setPos(x,y)
            
    def removeObjectFromCell(self, x, y):
        cell = self.findCell(x,y)
        cell.removeObject()
        
    def moveObject(self, x1, y1, obj, x2, y2):
        self.removeObjectFromCell(x1,y1)
        self.addObjectToCell(x2,y2,obj)
                
    def printCells(self):
        for cell in self.cells:
            print("[",cell.getXCoord(),",", cell.getYCoord(),"]", "items: ")
            for object in cell.getItems():
                print(object)