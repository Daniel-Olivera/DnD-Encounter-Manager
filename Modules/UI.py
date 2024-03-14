import pygame
from GameMaster import GameMaster
from Modules.Objects import Object

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
        self.font = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/5))
        self.infoFont = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/3))
        self.colorBoxCoords = [((1090,50),(30,30)), ((1125,50),(30,30)), ((1160,50),(30,30)), ((1195,50),(30,30))]
        self.elements = [Button(self.SCREEN, None,1090,50,30,30,Button.BUTTON_TYPE_RECT,self.DARKER_GREY),
                         Button(self.SCREEN, None,1125,50,30,30,Button.BUTTON_TYPE_RECT,self.BLACK),
                         Button(self.SCREEN, None,1160,50,30,30,Button.BUTTON_TYPE_RECT,self.DARK_RED),
                         Button(self.SCREEN, None,1195,50,30,30,Button.BUTTON_TYPE_RECT,self.DARK_BLUE)]
        
    # Draws a single cell of the grid, along with any items or characters that are in that cell
    def drawCell(self, gm, cell, x,y,size, timeLastClick):
        # Resets the color of a cell to its original after being clicked
        if (pygame.time.get_ticks() - timeLastClick) >= 350:
            cell.setColor(cell.getPermanentColor())
        
        pygame.draw.rect(self.SCREEN, cell.getColor(), (x, y, size-self.BORDERSIZE, size-self.BORDERSIZE))    
        if cell.hasObjects():
            for obj in cell.getItems():
                # Draw all the players on the board
                if obj in gm.getPlayers():
                    pygame.draw.circle(self.SCREEN, self.BLUE, (x+(size/2),y+(size/2)),size/2.5,0,1,1,1,1)
                    text = self.font.render(obj.getName(), True, self.WHITE, None)
                    textRect = text.get_rect()
                    textRect.center = (x+(size/2),y+(size/4))
                    self.SCREEN.blit(text, textRect)
                # Draw all the enemies on the board
                if obj in gm.getEnemies():
                    pygame.draw.circle(self.SCREEN, self.RED, (x+(size/2),y+(size/2)),size/2.5,0,1,1,1,1)
                    text = self.font.render(obj.getName(), True, self.WHITE, None)
                    textRect = text.get_rect()
                    textRect.center = (x+(size/2),y+(size/2))
                    self.SCREEN.blit(text, textRect)
    
    # Draws the entire grid on the screen using the drawCell function
    def drawGrid(self, gm, timeLastClick, cameraOffset):
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
        return (mousePosX > 0) and (mousePosY > 0) and (mousePosX < 950) and (mousePosY < 500)
    
    # Draws the UI sections where cell controls and info will appear
    def drawUI(self):
        pygame.draw.rect(self.SCREEN, self.DARKER_GREY, (0,500,950,720))
        pygame.draw.rect(self.SCREEN, self.DARKER_GREY, (950,0,1280,720))
        pygame.draw.line(self.SCREEN,self.BLACK,(950,500),(950,720))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(950,0),(950,500))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,500),(950,500))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,1),(950,1))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,0),(0,500))
        
    # The overall draw function which calls other draw functions to encapsulate 
    # it all into one function call
    def draw(self,gm, time_of_last_click, offsetx, offsety):
        self.SCREEN.fill(self.BLACK)
        self.drawGrid(gm, time_of_last_click, (offsetx, offsety))
        self.drawUI()
        if self.displayCellInfo:
            self.showCellInfo(self.cellToDisplay)
        
    def displayText(self, cell):
        self.displayCellInfo = True
        self.cellToDisplay = cell
        
    def showCellInfo(self, cell):
        if cell is None:
            return
        cellPos = "Cell: (" + str(cell.getXCoord()) + ", " + str(cell.getYCoord()) + ")" + "\n\nColors:  \n\n"
        if cell.hasObjects():
            cellPos += "Objects:  "
            for obj in cell.getItems():
                cellPos += obj.getName() + "\nDesc:  " + obj.getDescription() 
                if obj.getType() == Object.TYPE_CHARACTER or obj.getType() == Object.TYPE_ENEMY:
                    cellPos += "\nHP = " + str(obj.getHP())
        
        for element in self.elements:
            element.draw()
            
        cellPosText = self.infoFont.render(cellPos, True, self.WHITE, None)
        textRect = cellPosText.get_rect()
        textRect.topleft = (((self.WINDOW_WIDTH - 950)/4)+900, 30)
        self.SCREEN.blit(cellPosText, textRect)
    
    def getClickedColor(self, mousePos):        
        for button in self.elements:
            if button.isClicked(mousePos):
                return button.color
    
        return None
        
    def changeCellColor(self, newColor, cell):
        if newColor is None:
            return
        if cell is None:
            return
        self.gm.setCellColor(cell, newColor)

# Building block for any ui element
# Any element should be a subclass of this one
class UIElement:
    
    def __init__(self, SCREEN, text, x1, y1, x2, y2):
        self.SCREEN = SCREEN
        self.text = text
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