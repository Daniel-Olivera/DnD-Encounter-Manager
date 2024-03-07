from Cell import Cell

class Grid:
    size = 0
    cellSize = 0
    numCells = 0
    
    cells = []
    
    def __init__(self, size, cellSize):
        self.size = size
        self.cellSize = cellSize
        self.numCells = pow(size,2)
        for i in range(0,size):
            for j in range(0,size):
                self.cells.append(Cell(i,j,cellSize))
    
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
        
    def addObjectToCell(self, x, y, obj):
        for cell in self.cells:
            if cell.getXCoord() == x and cell.getYCoord() == y:
                cell.addObject(obj)
                break
                
    def printCells(self):
        for cell in self.cells:
            print("[",cell.getXCoord(),",", cell.getYCoord(),"]", "items: ", cell.getItems())