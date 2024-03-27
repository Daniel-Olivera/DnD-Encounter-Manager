from Modules.Grid import Grid
from Modules.Objects import Item
from Modules.Objects import Character
from Modules.json import jsonReader

# Manages the Game. Used to manipulate the gameboard and move characters and items around
class GameMaster:
    
    TYPE_ENEMY = 1
    TYPE_CHARACTER = 2
    
    def __init__(self, gridSize, cellSize):
        self.grid = Grid(gridSize, cellSize)
        self.players = []
        self.enemies = []
        self.items = []
        
    def saveGame(self):
        js = jsonReader()
        data = {}
        for i, character in enumerate(self.getActiveParticipants()):
            data[i] = character.toJson()
        js.saveGame(data)
        
    def loadGame(self):
        js = jsonReader()
        data = js.loadGame()
        if data is None:
            return
        
        for item in data:
            thing = data[item]
            self.addCharacter(thing["type"], thing["Name"], thing["Description"],
                              thing["MaxHP"], thing["HP"], thing["Initiative"], thing["image file"])
        
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
    
    def addCharacter(self, type, name, desc, hp, currentHP, initiative, file):
        if type == Character.TYPE_CHARACTER:
            self.addPlayer(name, desc, hp, currentHP, initiative, file)
        if type == Character.TYPE_ENEMY:
            self.addEnemy(name, desc, hp, currentHP, initiative, file)
        
    def addPlayer(self, name, desc, hp, currentHP, initiative, file):
        newPlayer = Character(Character.TYPE_CHARACTER, name, desc, hp, currentHP, initiative, file)
        self.players.append(newPlayer)
        
    def addEnemy(self, name, desc, hp, currentHP, initiative, file):
        newEnemy = Character(Character.TYPE_ENEMY, name, desc, hp, currentHP, initiative, file)
        self.enemies.append(newEnemy)
        
    def hurtCharacter(self, character, damage):
        character.setHP(character.getCurrentHP() - damage)
        if character.getCurrentHP() < 0:
            character.setHP(0)
        
    def healCharacter(self, character, healAmount):
        character.setHP(character.getCurrentHP() + healAmount)
        if character.getCurrentHP() > character.getMaxHP():
            character.setHP(character.getMaxHP())
        
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