import pygame
from GameMaster import GameMaster
from Modules.UI import UI

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

LEFT_CLICK = 1
MIDDLE_MOUSE = 2
RIGHT_CLICK = 3

def main():
    
    gm = GameMaster(50, 50)
    gm.addPlayer("Evan", "mage", 100)
    gm.addEnemy("Hunnlef", "archer", 100)
    gm.placeCharacterOnBoard(gm.getPlayers()[0], 1,1)
    gm.placeCharacterOnBoard(gm.getEnemies()[0], 2,3)
    running = True
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('DND Encounter Simulator')
    time_of_last_click = 0
    offsetx = 0
    offsety = 0
    global font
    middleMouseDragging = False
    mouseOneDragging = False
    heldItem = None

    scale = 0
    ui = UI(SCREEN, gm, time_of_last_click=0, offsetx=0, offsety=0)
    selectedCell = None

# MAIN LOOP
    while running:
        font = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/5))
        ui.draw(gm, time_of_last_click, offsetx, offsety)
        
        if mouseOneDragging:
                    heldItem = ui.holdObject(pygame.mouse.get_pos(), selectedCell)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle Left Clicks
                if event.button == 1:
                    time_of_last_click = pygame.time.get_ticks()
                    selectedCell = ui.getClickedCell(gm, event.pos, (offsetx, offsety))
                    mouseOneDragging = True
                # Handle Middle mouse clicks
                if event.button == 2:
                    mouse_x, mouse_y = event.pos  
                    drag_start_pos_x = offsetx - mouse_x
                    drag_start_pos_y = offsety - mouse_y
                    middleMouseDragging = True
            # What happens when the mouse button is released
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    middleMouseDragging = False
                if event.button == 1:
                    if heldItem is not None:
                        newCell = ui.getClickedCell(gm, event.pos, (offsetx, offsety))
                        gm.moveObjectOnBoard(heldItem, selectedCell.getXCoord(), selectedCell.getYCoord(), newCell.getXCoord(), newCell.getYCoord())
                    mouseOneDragging = False
                    mousePos = pygame.mouse.get_pos()
                    if ui.clickedInGrid(mousePos):
                        selectedCell = ui.getClickedCell(gm, mousePos, (offsetx, offsety))
                        if selectedCell is not None:
                            selectedCell.setColor(ui.DARK_GREY)
                            ui.displayText(selectedCell)
                    else:
                        newColor = ui.getClickedColor(mousePos)
                        ui.changeCellColor(newColor, selectedCell)
            if event.type == pygame.MOUSEMOTION:
                if middleMouseDragging:
                    offsetx, offsety = ui.dragGrid(event.pos, drag_start_pos_x, drag_start_pos_y)
            if event.type == pygame.MOUSEWHEEL:
                ui.changeZoom(event)
    

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            offsety -= 0.15 * gm.getGridSize()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            offsetx -= 0.15 * gm.getGridSize()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            offsety += 0.15 * gm.getGridSize()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            offsetx += 0.15 * gm.getGridSize()
        if keys[pygame.K_SPACE]:
            offsetx = 0
            offsety = 0

        pygame.display.update()

    pygame.quit()
                
if __name__ == "__main__":
    main()
