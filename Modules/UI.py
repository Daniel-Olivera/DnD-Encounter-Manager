import pygame
from GameMaster import GameMaster
from Modules.Objects import Object
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
    def draw(self,gm, time_of_last_click, offsetx, offsety, selection):
        self.offsetx = offsetx
        self.offsety = offsety
        self.SCREEN.fill(self.BLACK)
        self.drawGrid(gm, time_of_last_click, (offsetx, offsety))
        self.drawSelection(selection)
        self.drawUI()
        if self.displayCellInfo:
            self.showCellInfo(self.cellToDisplay)
        
    def displayText(self, cell):
        self.displayCellInfo = True
        self.cellToDisplay = cell
        
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
                min_x = min(tile.getXCoord(),min_x)
                min_y = min(tile.getYCoord(),min_y)
                max_x = max(tile.getXCoord(),max_x)
                max_y = max(tile.getYCoord(),max_y)
            
            cellPos = "Cells: (" + str(min_x) + "," + str(min_y) + ") - (" + str(max_x) + "," + str(max_y) + ")" + "\n\nColors:  "
            
        else:            
            cellPos = "Cell: (" + str(cell.getXCoord()) + ", " + str(cell.getYCoord()) + ")" + "\n\nColors:  \n\n"
            if cell.hasObject():
                cellPos += "Object:  "
                obj = cell.getItem()
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
        elif isinstance(cell,list):
            for tile in cell:
                self.gm.setCellColor(tile,newColor)
        else:
            self.gm.setCellColor(cell, newColor)
        
    def changeZoom(self, event):
        if event.y == 1:
            scale = 3
        if event.y == -1:
            scale = (-3)
        self.gm.setGridCellSize(self.gm.getGridCellSize() + scale)
        
    def dragGrid(self, mousePos, drag_start_pos_x, drag_start_pos_y):
        mouse_x, mouse_y = mousePos
        offsetx = mouse_x + drag_start_pos_x
        offsety = mouse_y + drag_start_pos_y
        return (offsetx, offsety)
    
    def holdObject(self, mousePos, cell):
        if cell.hasObject() == False:
            return
        size = cell.getSize()
        x, y = mousePos
        obj = cell.getItem()
        if obj in self.gm.getPlayers():
            pygame.draw.circle(self.SCREEN, self.BLUE, (x,y),size/2.5,0,1,1,1,1)

        if obj in self.gm.getEnemies():
            pygame.draw.circle(self.SCREEN, self.RED, (x,y),size/2.5,0,1,1,1,1)
            
        return obj

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
            for j in range(mousey-self.offsety,starty-self.offsety,cellSize):
                for i in range(mousex-self.offsetx,startx-self.offsetx,cellSize):
                    cells.append(self.gm.getCell((int(i/cellSize), int(j/cellSize))))
            
        elif diffx < 0 and diffy > 0:
            # mouse is below and left from starting point
            for j in range(starty-self.offsety,mousey-self.offsety,cellSize):
                for i in range(mousex-self.offsetx,startx-self.offsetx,cellSize):
                    cells.append(self.gm.getCell((int(i/cellSize), int(j/cellSize))))
                    
        elif diffx > 0 and diffy < 0:
            # mouse is up and right from starting point
            for j in range(mousey-self.offsety,starty-self.offsety,cellSize):
                for i in range(startx-self.offsetx,mousex-self.offsetx,cellSize):
                    cells.append(self.gm.getCell((int(i/cellSize), int(j/cellSize))))
        else:    
            # mouse is down and right from starting point
            for j in range(starty-self.offsety,mousey-self.offsety,cellSize):
                for i in range(startx-self.offsetx,mousex-self.offsetx,cellSize):
                    cells.append(self.gm.getCell((int(i/cellSize), int(j/cellSize))))
            
        return cells
    
    def drawSelection(self, selection):
        if selection is None:
            return
        elif isinstance(selection, list):
            min_x = 99999
            min_y = 99999
            max_x = 0
            max_y = 0
            for cell in selection:
                size = cell.getSize()
                min_x = min(cell.getXCoord(),min_x)
                min_y = min(cell.getYCoord(),min_y)
                max_x = max(cell.getXCoord(),max_x)
                max_y = max(cell.getYCoord(),max_y)

            pygame.draw.rect(self.SCREEN, self.DARK_RED, ((min_x*size) + self.offsetx + min_x, (min_y*size) + self.offsety + min_y, (1+max_x-min_x)*size, (1+max_y-min_y)*size), 2)
            
        else:
            size = selection.getSize()
            x = selection.getXCoord()
            y = selection.getYCoord()
            pygame.draw.rect(self.SCREEN, self.DARK_RED, ((x*size) + self.offsetx + x, (y*size) + self.offsety + y, size-self.BORDERSIZE, size-self.BORDERSIZE), 2)
            
            
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