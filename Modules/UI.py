import pygame
from GameMaster import GameMaster
from Modules.Objects import *
import numpy as np

# Controls and draws all the UI elements
class UI:
    
    BLACK = (10, 10, 10)
    WHITE = (255, 255, 255)
    DARK_BLUE = (75, 75, 255)
    GREY = (150, 150, 150)
    LIGHT_GREY = (200, 200, 200)
    DARK_GREY = (50, 50, 50)
    DARKER_GREY = (25,25,30)
    BLUE = (100,100,200)
    RED = (255,100,100)
    GREEN = (100,255,100)
    DARK_RED = (255,50,50)
    WINDOW_HEIGHT = 720
    WINDOW_WIDTH = 1280
    BORDERSIZE = 2
    
    def __init__(self, SCREEN, gm, time_of_last_click, offsetx, offsety):
        self.SCREEN = SCREEN
        self.gm = gm
        self.time_of_last_click = time_of_last_click
        self.offsetx = offsetx
        self.offsety = offsety
        self.scale = 0
        self.offsetx = 0
        self.offsety = 0
        self.displayCellInfo = False
        self.cellToDisplay = None
        self.gridBorderScale = 0
        self.font = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/5))
        self.infoFont = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/3))
        self.colorBoxCoords = [((1090,50),(30,30)), ((1125,50),(30,30)), ((1160,50),(30,30)), ((1195,50),(30,30))]
        self.colorPickingButtons = [
                         Button(self.SCREEN, None,1090,50,30,30,Button.BUTTON_TYPE_RECT,self.DARKER_GREY),
                         Button(self.SCREEN, None,1125,50,30,30,Button.BUTTON_TYPE_RECT,self.BLACK),
                         Button(self.SCREEN, None,1160,50,30,30,Button.BUTTON_TYPE_RECT,self.DARK_RED),
                         Button(self.SCREEN, None,1195,50,30,30,Button.BUTTON_TYPE_RECT,self.DARK_BLUE)]
        
        self.hpChangeButtons = [
                         Button(self.SCREEN, "hurt", ((UI.WINDOW_WIDTH - 950)/2)+900, 200, 20, 20, Button.BUTTON_TYPE_RECT, self.RED),
                         Button(self.SCREEN, "heal", ((UI.WINDOW_WIDTH - 950)/2)+990, 200, 20, 20, Button.BUTTON_TYPE_RECT, self.GREEN)]
        self.healthInput = TextInput(self.SCREEN, None, ((UI.WINDOW_WIDTH - 950)/2)+930, 200, 50, 35)
        self.characterPortraits = []
        portraitXCoord = 30
        # TODO: add character image to portraits
        for character in gm.getActiveParticipants():
            self.characterPortraits.append(CharacterPortrait(self.SCREEN, character,portraitXCoord,530,character.getType()), None)
            portraitXCoord += CharacterPortrait.PORTRAIT_WIDTH + 10

            
    # Draws a single cell of the grid, along with any items or characters that are in that cell
    def drawCell(self, gm, cell, x,y,size, timeLastClick):
        # Resets the color of a cell to its original after being clicked
        if (pygame.time.get_ticks() - timeLastClick) >= 350:
            cell.setColor(cell.getPermanentColor())
        
        pygame.draw.rect(self.SCREEN, cell.getColor(), (x, y, size-self.BORDERSIZE, size-self.BORDERSIZE))    
        if cell.hasObject():
            obj = cell.getItem()
            # Draw the player in that cell
            if obj in gm.getPlayers():
                pygame.draw.circle(self.SCREEN, self.BLUE, (x+(size/2),y+(size/2)),size/2.5,0,1,1,1,1)
                text = self.font.render(obj.getName(), True, self.WHITE, None)
                textRect = text.get_rect()
                textRect.center = (x+(size/2),y+(size/4))
                self.SCREEN.blit(text, textRect)
            # Draw the enemy in that cell
            if obj in gm.getEnemies():
                pygame.draw.circle(self.SCREEN, self.RED, (x+(size/2),y+(size/2)),size/2.5,0,1,1,1,1)
                text = self.font.render(obj.getName(), True, self.WHITE, None)
                textRect = text.get_rect()
                textRect.center = (x+(size/2),y+(size/2))
                self.SCREEN.blit(text, textRect)
    
    # Draws the entire grid on the screen using the drawCell function
    def drawGrid(self, gm, timeLastClick, cameraOffset):
        gridSize = self.gm.getGridSize()
        cellSize = self.gm.getGridCellSize()
        gridBorderWidth = gridBorderHeight = (cellSize*(gridSize+1)) - self.gridBorderScale + 2
        # Draws blue square around the playing field
        pygame.draw.rect(self.SCREEN,self.DARK_BLUE,(-2+self.offsetx,-2+self.offsety,gridBorderWidth, gridBorderHeight),2)
        gridCells = gm.getGridCells()
        index = 0
        for i in range(gm.getNumRows()):
            for j in range(gm.getNumCols()):
                cell = gridCells[index]
                self.drawCell(gm, cell, cell.getXCoord()+(i*cell.getSize())+cameraOffset[0], cell.getYCoord()+(j*cell.getSize())+cameraOffset[1],
                        cell.getSize(), timeLastClick)
                index += 1
                
    # Returns the Cell object of whichever grid square the user clicked on
    def getClickedCell(self, gm, mousePos, offset):
        cellSize = gm.getGridCellSize()
        gridposx, gridposy = mousePos
        gridposx -= offset[0]
        gridposy -= offset[1]
        convertedPos = (int((gridposx - (gridposx/cellSize)) / cellSize), int((gridposy - (gridposy/cellSize)) / cellSize))
        return gm.getCell(convertedPos)

    # Checks if the user clicked in the gameboard window
    def clickedInGrid(self, mousePos):
        mousePosX, mousePosY = mousePos
        gridSize = self.gm.getGridSize()
        cellSize = self.gm.getGridCellSize()
        gridBorderWidth = gridBorderHeight = (cellSize*(gridSize+1)) - self.gridBorderScale + 2
        return (mousePosX > 0) and (mousePosY > 0) and (mousePosX < gridBorderWidth) and (mousePosY < gridBorderHeight) and (mousePosX < 950) and (mousePosY < 500)
    
    # Draws the UI sections where cell controls and info will appear
    def drawUI(self):
        pygame.draw.rect(self.SCREEN, self.DARKER_GREY, (0,500,950,720))
        pygame.draw.rect(self.SCREEN, self.DARKER_GREY, (950,0,1280,720))
        pygame.draw.line(self.SCREEN,self.BLACK,(950,500),(950,720))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(950,0),(950,500))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,500),(950,500))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,1),(950,1))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,0),(0,500))
        for character in self.characterPortraits:
            character.draw()
        
    # The overall draw function which calls other draw functions to encapsulate 
    # it all into one function call
    def draw(self,gm, time_of_last_click, offsetx, offsety, selection):
        self.offsetx = offsetx
        self.offsety = offsety
        self.SCREEN.fill(self.BLACK)
        self.drawGrid(gm, time_of_last_click, (offsetx, offsety))
        self.drawSelection(selection)
        self.drawUI()
        if self.displayCellInfo:
            self.showCellInfo(self.cellToDisplay)
        
    def displayText(self, cell, numberInput):
        self.displayCellInfo = True
        self.cellToDisplay = cell
        self.numberInput = numberInput
        
    def hideText(self):
        self.displayCellInfo = False
        
    def showCellInfo(self, cell):
        if cell is None:
            return
        
        cellPos = ""
        
        if isinstance(cell, list):
            min_x = 99999
            min_y = 99999
            max_x = 0
            max_y = 0
            for tile in cell:
                if tile is None:
                    continue
                min_x = min(tile.getXCoord(),min_x)
                min_y = min(tile.getYCoord(),min_y)
                max_x = max(tile.getXCoord(),max_x)
                max_y = max(tile.getYCoord(),max_y)
                
            cellPos = "Cells: (" + str(min_x) + "," + str(min_y) + ") - (" + str(max_x) + "," + str(max_y) + ")" + "\n\nColors:  "
            
        elif isinstance(cell, CharacterPortrait):
            character = cell.getCharacter()
            cellPos = "Position: (" + str(character.getPos()[0]) + ", " + str(character.getPos()[1]) + ")" + "  \n\n"
            cellPos += character.getName() + "\nDesc:  " + character.getDescription() 
            cellPos += "\nHP = " + str(character.getCurrentHP())
            self.healthInput.draw(self.numberInput)
            for button in self.hpChangeButtons:
                        button.draw()
            
        else:            
            cellPos = "Cell: (" + str(cell.getXCoord()) + ", " + str(cell.getYCoord()) + ")" + "\n\nColors:  \n\n"
            if cell.hasObject():
                cellPos += "Object:  "
                obj = cell.getItem()
                cellPos += obj.getName() + "\nDesc:  " + obj.getDescription() 
                if obj.getType() == Object.TYPE_CHARACTER or obj.getType() == Object.TYPE_ENEMY:
                    cellPos += "\nHP = " + str(obj.getCurrentHP())
                    self.healthInput.draw(self.numberInput)
                    for button in self.hpChangeButtons:
                        button.draw()
        
        if not isinstance(cell, CharacterPortrait):
            for element in self.colorPickingButtons:
                element.draw()
            
        cellPosText = self.infoFont.render(cellPos, True, self.WHITE, None)
        textRect = cellPosText.get_rect()
        textRect.topleft = (((self.WINDOW_WIDTH - 950)/4)+900, 30)
        self.SCREEN.blit(cellPosText, textRect)
    
    def getClickedColor(self, mousePos):        
        for button in self.colorPickingButtons:
            if button.isClicked(mousePos):
                return button.color
    
        return None
    
    def getClickedHPButton(self, mousePos):        
        for button in self.hpChangeButtons:
            if button.isClicked(mousePos):
                return button.name
    
        return None
        
    def changeCellColor(self, newColor, cell):
        if newColor is None:
            return
        if cell is None:
            return
        elif isinstance(cell,list):
            for tile in cell:
                self.gm.setCellColor(tile,newColor)
        else:
            self.gm.setCellColor(cell, newColor)
        
    def changeZoom(self, event):
        if event.y == 1:
            self.scale = 3
            self.gridBorderScale += 3
        if event.y == -1:
            self.scale = (-3)
            self.gridBorderScale -= 3
        self.gm.setGridCellSize(self.gm.getGridCellSize() + self.scale)
        
    def dragGrid(self, mousePos, drag_start_pos_x, drag_start_pos_y):
        mouse_x, mouse_y = mousePos
        offsetx = mouse_x + drag_start_pos_x
        offsety = mouse_y + drag_start_pos_y
        return (offsetx, offsety)
    
    def holdObject(self, mousePos, uiElement):
        if uiElement is None:
            return
        if not isinstance(uiElement, CharacterPortrait):
            if uiElement.hasObject() == False:
                return
            obj = uiElement.getItem()
        else:    
            obj = uiElement.getCharacter()
        size = self.gm.getGridCellSize()
        x, y = mousePos
        if obj in self.gm.getPlayers():
            pygame.draw.circle(self.SCREEN, self.BLUE, (x,y),size/2.5,0,1,1,1,1)

        if obj in self.gm.getEnemies():
            pygame.draw.circle(self.SCREEN, self.RED, (x,y),size/2.5,0,1,1,1,1)
            
        return obj
    
    def getClickedPortrait(self,mousePos):
        for element in self.characterPortraits:
            if element.isClicked(mousePos):
                return element

    def drawSelectionBox(self, startx, starty, mousex, mousey):
        
        diffx = mousex - startx
        diffy = mousey - starty
        
        if diffx < 0 and diffy < 0:
            # mouse is up and left from starting point
            pygame.draw.rect(self.SCREEN, self.DARK_RED, (mousex, mousey, startx-mousex, starty-mousey), 2)
        elif diffx < 0 and diffy > 0:
            pygame.draw.rect(self.SCREEN, self.DARK_RED, (mousex, starty, startx-mousex, mousey-starty), 2)
        elif diffx > 0 and diffy < 0:
            pygame.draw.rect(self.SCREEN, self.DARK_RED, (startx, mousey, mousex-startx, starty-mousey), 2)
        else:    
            pygame.draw.rect(self.SCREEN, self.DARK_RED, (startx, starty, diffx, diffy), 2)
            
    def selectMultiple(self, startx, starty, mousex, mousey):
    
        diffx = mousex - startx
        diffy = mousey - starty
        cells = []
        cellSize = self.gm.getGridCellSize()
                
        if diffx < 0 and diffy < 0:
            # mouse is up and left from starting point
            for j in range(int(mousey-self.offsety),int(starty-self.offsety),int(cellSize)):
                for i in range(int(mousex-self.offsetx),int(startx-self.offsetx),int(cellSize)):
                    cells.append(self.gm.getCell((int(i/cellSize), int(j/cellSize))))
            
        elif diffx < 0 and diffy > 0:
            # mouse is below and left from starting point
            for j in range(int(starty-self.offsety),int(mousey-self.offsety),cellSize):
                for i in range(int(mousex-self.offsetx),int(startx-self.offsetx),cellSize):
                    cells.append(self.gm.getCell((int(i/cellSize), int(j/cellSize))))
                    
        elif diffx > 0 and diffy < 0:
            # mouse is up and right from starting point
            for j in range(int(mousey-self.offsety),int(starty-self.offsety),cellSize):
                for i in range(int(startx-self.offsetx),int(mousex-self.offsetx),cellSize):
                    cells.append(self.gm.getCell((int(i/cellSize), int(j/cellSize))))
        else:    
            # mouse is down and right from starting point
            for j in range(int(starty-self.offsety),int(mousey-self.offsety),cellSize):
                for i in range(int(startx-self.offsetx),int(mousex-self.offsetx),cellSize):
                    cells.append(self.gm.getCell((int(i/cellSize), int(j/cellSize))))
            
        if len(cells) == 0:
            return None

        return cells
    
    def drawSelection(self, selection):
        size = self.gm.getGridCellSize()
        if selection is None:
            return
        elif isinstance(selection, list):
            min_x = 99999
            min_y = 99999
            max_x = 0
            max_y = 0
            for cell in selection:
                if cell is None:
                    continue
                min_x = min(cell.getXCoord(),min_x)
                min_y = min(cell.getYCoord(),min_y)
                max_x = max(cell.getXCoord(),max_x)
                max_y = max(cell.getYCoord(),max_y)
                
            selectionBorderWidth = ((max_x - min_x)*size)+(self.BORDERSIZE)+size
            selectionBorderHeight = ((max_y - min_y)*size)+(self.BORDERSIZE)+size

            pygame.draw.rect(self.SCREEN, self.DARK_RED, ((min_x*size) + self.offsetx + min_x, 
                                                          (min_y*size) + self.offsety + min_y, 
                                                          selectionBorderWidth, 
                                                          selectionBorderHeight), 2)
            
        else:
            x = selection.getXCoord()
            y = selection.getYCoord()
            pygame.draw.rect(self.SCREEN, self.DARK_RED, ((x*size) + self.offsetx + x, 
                                                          (y*size) + self.offsety + y, 
                                                          size-self.BORDERSIZE, 
                                                          size-self.BORDERSIZE), 2)
            
    def healthInputClicked(self, mousePos):
        return self.healthInput.isClicked(mousePos)
                    
        
# /////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////
# Building block for any ui element
# Any element should be a subclass of this one
class UIElement:
    
    name = ""
    
    def __init__(self, SCREEN, text, x1, y1, x2, y2):
        self.SCREEN = SCREEN
        self.name = text
        self.boundingBox = (x1, y1, x2, y2)
        
    def isClicked(self, mousePos):
        mousePosX, mousePosY = mousePos
        x1, y1, x2, y2 = self.boundingBox
        return (mousePosX > x1) and (mousePosY > y1) and (mousePosX < x1+x2) and (mousePosY < y1+y2)
    
class Button(UIElement):
    
    BUTTON_TYPE_RECT = 0
    BUTTON_TYPE_DROPDOWN = 1
    
    def __init__(self, SCREEN, text, x1, y1, x2, y2, type, color):
        super().__init__(SCREEN, text, x1, y1, x2, y2)
        self.type = type
        self.color = color
        
    def draw(self):
        self.__drawButton()        
        
    def __drawButton(self):
        x1,y1,x2,y2 = self.boundingBox
        if self.type == self.BUTTON_TYPE_RECT:
            if self.color == UI.DARKER_GREY:
                pygame.draw.rect(self.SCREEN, UI.DARK_BLUE, (x1,y1,x2,y2),2)
            else:
                pygame.draw.rect(self.SCREEN, self.color, (x1,y1,x2,y2))
                
class TextInput(UIElement):
    
    def __init__(self, SCREEN, text, x1, y1, x2, y2):
        super().__init__(SCREEN, text, x1, y1, x2, y2)
        
    def draw(self, input):
        self.__drawTextInput(input)
    
    def __drawTextInput(self, inputStr):
        x1,y1,x2,y2 = self.boundingBox
        pygame.draw.rect(self.SCREEN, UI.BLACK, (x1,y1-8,x2,y2))
        pygame.draw.rect(self.SCREEN, UI.DARK_GREY, (x1+2,y1-6,x2-4,y2-4))
        txtFont = pygame.font.Font('freesansbold.ttf', int(16.7))
        inputText = txtFont.render(inputStr, True, UI.WHITE, None)
        inputTextRect = inputText.get_rect()
        inputTextRect.topleft = (x1+8, y1)
        self.SCREEN.blit(inputText, inputTextRect)

class CharacterPortrait(UIElement):
    
    TYPE_PLAYER = 0
    TYPE_ENEMY = 1
    PORTRAIT_WIDTH = 120
    PORTRAIT_HEIGHT = 150
    
    def __init__(self, SCREEN, character, x1, y1, type, file):
        super().__init__(SCREEN, character.getName(), x1,y1,self.PORTRAIT_WIDTH,self.PORTRAIT_HEIGHT)
        self.type = type
        self.character = character
        if file is not None:
            self.charImage = pygame.image.load(file)
            self.imagerect = self.charImage.get_rect()
        if type == Object.TYPE_CHARACTER:
            self.color = UI.DARK_BLUE
        else:
            self.color = UI.DARK_RED
            
    def getCharacter(self):
        return self.character
    
    def draw(self):
        self.__drawPortrait()        
        
    def __drawPortrait(self):
        x1,y1,x2,y2 = self.boundingBox
        # Draw the box
        pygame.draw.rect(self.SCREEN, self.color, (x1,y1,x2,y2),2)
        
        # Draw the HP Bar
        pygame.draw.rect(self.SCREEN, UI.RED, (x1+UI.BORDERSIZE,
                                               y1+self.PORTRAIT_HEIGHT-5,
                                               x2-UI.BORDERSIZE,
                                               5))
        pygame.draw.rect(self.SCREEN, UI.GREEN, (x1+UI.BORDERSIZE,
                                                 y1+self.PORTRAIT_HEIGHT-5,
                                                 int((x2-UI.BORDERSIZE)*self.character.getHPPercent()),
                                                 5))
        
        # Draw and write the nameplate
        pygame.draw.rect(self.SCREEN, self.color, (x1+UI.BORDERSIZE,
                                                   y1+2,
                                                   x2-UI.BORDERSIZE,
                                                   25))
        
        txtFont = pygame.font.Font('freesansbold.ttf', int(16.7))
        inputText = txtFont.render(self.character.getName(), True, UI.WHITE, None)
        inputTextRect = inputText.get_rect()
        inputTextRect.topleft = (x1+(self.PORTRAIT_WIDTH/4), y1+5)
        self.SCREEN.blit(inputText, inputTextRect)