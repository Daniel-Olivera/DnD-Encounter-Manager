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
    gm.addPlayer("Nicole", "mage", 100)
    gm.addEnemy("Auntie", "archer", 100)
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
    leftMouseDragging = False
    rightMouseDragging = False
    heldItem = None
    selection_box_start_pos_x = 0
    selection_box_start_pos_y = 0

    ui = UI(SCREEN, gm, time_of_last_click=0, offsetx=0, offsety=0)
    selectedCell = None
    startDragCell = None
# TODO: Fix characters can eat eachother if you put them on the same square
# MAIN LOOP
    while running:
        font = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/5))
        ui.draw(gm, time_of_last_click, offsetx, offsety, selectedCell)
        
        if selectedCell is None:
            ui.hideText()
        
        if leftMouseDragging:
            heldItem = ui.holdObject(pygame.mouse.get_pos(), startDragCell)
            
        if rightMouseDragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            ui.drawSelectionBox(selection_box_start_pos_x, selection_box_start_pos_y, mouse_x, mouse_y)

        for event in pygame.event.get():
            # Closes pygame
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle Left Clicks
                if event.button == LEFT_CLICK:
                    time_of_last_click = pygame.time.get_ticks()
                    startDragCell = ui.getClickedCell(gm, event.pos, (offsetx, offsety))
                    leftMouseDragging = True
                    
                # Handle Middle mouse clicks
                if event.button == MIDDLE_MOUSE:
                    mouse_x, mouse_y = event.pos  
                    drag_start_pos_x = offsetx - mouse_x
                    drag_start_pos_y = offsety - mouse_y
                    middleMouseDragging = True
                    
                # Handle Right mouse clicks
                if event.button == RIGHT_CLICK:
                    mouse_x, mouse_y = event.pos
                    selection_box_start_pos_x = mouse_x
                    selection_box_start_pos_y = mouse_y
                    rightMouseDragging = True
                    
            # What happens when the mouse button is released
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == MIDDLE_MOUSE:
                    middleMouseDragging = False
                    
                # When left mouse is released
                if event.button == LEFT_CLICK:
                    if heldItem is not None:
                        newCell = ui.getClickedCell(gm, event.pos, (offsetx, offsety))
                        if newCell is not None:
                            gm.moveObjectOnBoard(heldItem, startDragCell.getXCoord(), startDragCell.getYCoord(), newCell.getXCoord(), newCell.getYCoord())
                    leftMouseDragging = False
                    mousePos = pygame.mouse.get_pos()
                    
                    if ui.clickedInGrid(mousePos):
                        selectedCell = ui.getClickedCell(gm, mousePos, (offsetx, offsety))
                        if selectedCell is not None:
                            selectedCell.setColor(ui.DARK_GREY)
                            ui.displayText(selectedCell)
                    else:
                        newColor = ui.getClickedColor(mousePos)
                        ui.changeCellColor(newColor, selectedCell)
                
                # When right mouse is released
                if event.button == RIGHT_CLICK:
                    rightMouseDragging = False
                    selectedCell = ui.selectMultiple(selection_box_start_pos_x, selection_box_start_pos_y, mouse_x, mouse_y)
                    ui.displayText(selectedCell)
                        
            # What happens when the mouse moves
            if event.type == pygame.MOUSEMOTION:
                if middleMouseDragging:
                    offsetx, offsety = ui.dragGrid(event.pos, drag_start_pos_x, drag_start_pos_y)
                    
            # What happens when you use the scroll wheel
            if event.type == pygame.MOUSEWHEEL:
                ui.changeZoom(event)
    
        # Handles when keyboard buttons are used
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
        if keys[pygame.K_ESCAPE]:
            selectedCell = None


        pygame.display.update()

    pygame.quit()
                
if __name__ == "__main__":
    main()
