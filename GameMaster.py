from Modules.Grid import Grid
from Modules.Objects import Item
from Modules.Objects import Character

# Manages the Game. Used to manipulate the gameboard and move characters and items around
class GameMaster:
    
    def __init__(self, gridSize, cellSize):
        self.grid = Grid(gridSize, cellSize)
        self.players = []
        self.enemies = []
        self.items = []
        
    def getGrid(self):
        return self.grid
    
    def getGridSize(self):
        return self.grid.getSize()
    
    def getGridNumCells(self):
        return self.grid.getNumCells()
        
    def getCell(self, pos):
        return self.grid.findCell(pos[0], pos[1])
        
    def getGridCellSize(self):
        return self.grid.getCellSize()
    
    def setGridCellSize(self, newSize):
        self.grid.setCellSize(newSize)
    
    def getNumRows(self):
        return self.grid.getSize()
    
    def getNumCols(self):
        return self.grid.getSize()
        
    def getGridCells(self):
        return self.grid.getCells()
    
    def getActiveParticipants(self):
        activeParticipants = self.players + self.enemies
        activeParticipants.sort(key = lambda x: x.getInitiative(), reverse=True)
        return activeParticipants
        
    def addPlayer(self, name, desc, hp):
        newPlayer = Character(Character.TYPE_CHARACTER, name, desc, hp)
        self.players.append(newPlayer)
        
    def addEnemy(self, name, desc, hp):
        newEnemy = Character(Character.TYPE_ENEMY, name, desc, hp)
        self.enemies.append(newEnemy)
        
    def addItem(self, name, desc):
        self.items.append(Item(name, desc))
        
    def removePlayer(self, player):
        self.players.remove(player)
        
    def removeEnemy(self, enemy):
        self.enemies.remove(enemy)
        
    def removeItem(self, item):
        self.items.remove(item)
        
    def placeCharacterOnBoard(self, character, x, y):
        newCell = self.grid.findCell(x,y)
        if newCell is not None and not newCell.hasObject():
            self.grid.addObjectToCell(x,y,character)
    
    def placeItemOnBoard(self, item, x, y):
        self.grid.addObjectToCell(x,y,item)
        
    def removeCharacterFromBoard(self, x, y):
        self.grid.removeObjectFromCell(x,y)
        
    def removeItemFromBoard(self, item, x, y):
        self.grid.removeObjectFromCell(x,y,item)
        
    def moveObjectOnBoard(self, obj, x1, y1, x2, y2):
        newCell = self.grid.findCell(x2,y2)
        if newCell is not None and not newCell.hasObject():
            self.grid.moveObject(x1,y1,obj,x2,y2)
        
    def giveItemToCharacter(self, item, character):
        item.setOwner(character)
        character.giveItem(item)
        
    def takeItemFromCharacter(self, item, character):
        item.setOwner(None)
        character.removeItem(item)
        
    def getPlayers(self):
        return self.players
    
    def getEnemies(self):
        return self.enemies
    
    def getItems(self):
        return self.items
    
    def getCellColor(self,x,y):
        return self.grid.findCell(x,y).getColor()
    
    def setCellColor(self, cell, color):
        if cell is None:
            return
        cell.setPermanentColor(color)
                
    def listPlayers(self):
        print("*---- PLAYERS ----*")
        for player in self.players:
            print(player)
            i = 0
            for item in player.getItems():
                print(i, ":", item)
                i += 1
            print("-----------------------")
            
    def listEnemies(self):
        print("*---- ENEMIES ----*")
        for enemy in self.enemies:
            print(enemy)
            i = 0
            for item in enemy.getItems():
                print(i, ":", item)
                i += 1
            print("-----------------------")
            
    def listItems(self):
        print("*----- ITEMS -----*")
        for item in self.items:
            print(item, "\n-----------------------")