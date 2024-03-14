import pygame
from GameMaster import GameMaster

class UI:
    
    def __init__(self, SCREEN, gm, time_of_last_click, offsetx, offsety):
        self.SCREEN = SCREEN
        self.gm = gm
        self.time_of_last_click = time_of_last_click
        self.offsetx = offsetx
        self.offsety = offsety
        self.BLACK = (10, 10, 10)
        self.WHITE = (255, 255, 255)
        self.DARK_BLUE = (75, 75, 255)
        self.GREY = (150, 150, 150)
        self.LIGHT_GREY = (200, 200, 200)
        self.DARK_GREY = (50, 50, 50)
        self.DARKER_GREY = (25,25,30)
        self.BLUE = (100,100,200)
        self.RED = (255,100,100)
        self.DARK_RED = (255,50,50)
        self.WINDOW_HEIGHT = 720
        self.WINDOW_WIDTH = 1280
        self.BORDERSIZE = 2
        self.scale = 0
        self.offsetx = 0
        self.offsety = 0
        self.displayCellInfo = False
        self.cellToDisplay = None
        self.font = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/5))
        self.infoFont = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/3))
        self.colorBoxCoords = [((1090,50),(30,30)), ((1125,50),(30,30)), ((1160,50),(30,30)), ((1195,50),(30,30))]
        
        
    def drawCell(self, gm, cell, x,y,size, timeLastClick):
        if (pygame.time.get_ticks() - timeLastClick) >= 350:
            cell.setColor(cell.getPermanentColor())
            
        pygame.draw.rect(self.SCREEN, cell.getColor(), (x, y, size-self.BORDERSIZE, size-self.BORDERSIZE))    
        if cell.hasObjects():
            for obj in cell.getItems():
                #Draw all the players on the board
                if obj in gm.getPlayers():
                    pygame.draw.circle(self.SCREEN, self.BLUE, (x+(size/2),y+(size/2)),size/2.5,0,1,1,1,1)
                    text = self.font.render(obj.getName(), True, self.WHITE, None)
                    textRect = text.get_rect()
                    textRect.center = (x+(size/2),y+(size/4))
                    self.SCREEN.blit(text, textRect)
                #Draw all the enemies on the board
                if obj in gm.getEnemies():
                    pygame.draw.circle(self.SCREEN, self.RED, (x+(size/2),y+(size/2)),size/2.5,0,1,1,1,1)
                    text = self.font.render(obj.getName(), True, self.WHITE, None)
                    textRect = text.get_rect()
                    textRect.center = (x+(size/2),y+(size/2))
                    self.SCREEN.blit(text, textRect)
                    
    def drawGrid(self, gm, timeLastClick, cameraOffset):
        gridCells = gm.getGridCells()
        index = 0
        for i in range(gm.getNumRows()):
            for j in range(gm.getNumCols()):
                cell = gridCells[index]
                self.drawCell(gm, cell, cell.getXCoord()+(i*cell.getSize())+cameraOffset[0], cell.getYCoord()+(j*cell.getSize())+cameraOffset[1],
                        cell.getSize(), timeLastClick)
                index += 1
                
    def getClickedCell(self, gm, mousePos, offset):
        cellSize = gm.getGridCellSize()
        gridposx, gridposy = mousePos
        gridposx -= offset[0]
        gridposy -= offset[1]
        convertedPos = (int((gridposx - (gridposx/cellSize)) / cellSize), int((gridposy - (gridposy/cellSize)) / cellSize))
        return gm.getCell(convertedPos)

    def clickedInGrid(self, mousePos):
        mousePosX, mousePosY = mousePos
        return (mousePosX > 0) and (mousePosY > 0) and (mousePosX < 950) and (mousePosY < 500)
    
    
    def drawUI(self):
        pygame.draw.rect(self.SCREEN, self.DARKER_GREY, (0,500,950,720))
        pygame.draw.rect(self.SCREEN, self.DARKER_GREY, (950,0,1280,720))
        pygame.draw.line(self.SCREEN,self.BLACK,(950,500),(950,720))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(950,0),(950,500))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,500),(950,500))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,1),(950,1))
        pygame.draw.line(self.SCREEN,self.DARK_BLUE,(0,0),(0,500))
        
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
        cellPos = "Cell: (" + str(cell.getXCoord()) + ", " + str(cell.getYCoord()) + ")" + "\n\nColors:  "
        pygame.draw.rect(self.SCREEN, self.DARK_BLUE, (1090,50,30,30),2)
        pygame.draw.rect(self.SCREEN, self.BLACK, (1125,50,30,30))
        pygame.draw.rect(self.SCREEN, self.DARK_RED, (1160,50,30,30))
        pygame.draw.rect(self.SCREEN, self.DARK_BLUE, (1195,50,30,30))
        cellPosText = self.infoFont.render(cellPos, True, self.WHITE, None)
        textRect = cellPosText.get_rect()
        textRect.center = (((self.WINDOW_WIDTH - 950)/2)+900, 50)
        self.SCREEN.blit(cellPosText, textRect)
        
    def getClickedColor(self, mousePos):
        mousePosX, mousePosY = mousePos
        index = 0
        for colorBox in self.colorBoxCoords:
            box_top_left_x, box_top_left_y = colorBox[0] 
            box_bot_right_x, box_bot_right_y = colorBox[1]
            if (mousePosX > box_top_left_x) and (mousePosY > box_top_left_y) and (mousePosX < box_top_left_x+box_bot_right_x) and (mousePosY < box_top_left_y+box_bot_right_y):
                break
            index += 1
    
        if index == 0:
            return self.DARKER_GREY
        elif index == 1:
            return self.BLACK
        elif index == 2:
            return self.DARK_RED
        elif index == 3:
            return self.DARK_BLUE
        else:
            return None
        
    def changeCellColor(self, newColor, cell):
        if newColor is None:
            return
        self.gm.setCellColor(cell, newColor)