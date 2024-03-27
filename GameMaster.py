from Modules.Grid import Grid
from Modules.Objects import Item
from Modules.Objects import Character
from Modules.json import jsonReader
from ast import literal_eval as make_tuple

# Manages the Game. Used to manipulate the gameboard and move characters and items around
class GameMaster:
    
    DEFAULT_COLOR = (25,25,30)
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
            key = "Character " + str(i)
            data[key] = character.toJson()
        
        for i, cell in enumerate(self.grid.getCells()):
            if cell.getColor() != self.DEFAULT_COLOR or cell.hasObject():
                data[str(cell.getPos())] = cell.toJson()
        
        js.saveGame(data)
        
        
    def loadGame(self):
        js = jsonReader()
        data = js.loadGame()
        if data is None:
            return
        
        for item in data:
            thing = data[item]
            if "Character" in item:
                newCharacter = self.addCharacter(thing["type"], thing["Name"], thing["Description"],
                                    thing["MaxHP"], thing["HP"], thing["Initiative"], thing["Position"], thing["image file"])
                self.placeCharacterOnBoard(newCharacter, thing["Position"][0], thing["Position"][1])
            else:
                coords = make_tuple(item)
                self.setCellColor(self.grid.findCell(coords[0], coords[1]), (thing["color_r"], thing["color_g"], thing["color_b"]))
            
        
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
    
    def addCharacter(self, type, name, desc, hp, currentHP, initiative, pos, file):
        newCharacter = None
        if type == Character.TYPE_CHARACTER:
            newCharacter = self.addPlayer(name, desc, hp, currentHP, initiative, pos, file)
        if type == Character.TYPE_ENEMY:
            newCharacter = self.addEnemy(name, desc, hp, currentHP, initiative, pos, file)
        return newCharacter
        
    def addPlayer(self, name, desc, hp, currentHP, initiative, pos, file):
        newPlayer = Character(Character.TYPE_CHARACTER, name, desc, hp, currentHP, initiative, pos, file)
        self.players.append(newPlayer)
        return newPlayer
        
    def addEnemy(self, name, desc, hp, currentHP, initiative, pos, file):
        newEnemy = Character(Character.TYPE_ENEMY, name, desc, hp, currentHP, initiative, pos, file)
        self.enemies.append(newEnemy)
        return newEnemy
        
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