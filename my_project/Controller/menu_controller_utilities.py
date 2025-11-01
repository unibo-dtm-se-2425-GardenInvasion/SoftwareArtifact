import pygame
from ..Model.menu_model import MenuModel
from ..View.menu_view import draw_modal
from ..Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT


def show_confirm_quit(screen: pygame.Surface, model: MenuModel) -> bool:
    # Returns True if user confirmed quit, False otherwise
    clock = pygame.time.Clock()
    background_copy = screen.copy() # Create a copy of the current screen to blur later
    small_size = (screen.get_width() // 3, screen.get_height() // 3) # Reduce size for faster blurring
    blurred = pygame.transform.smoothscale(background_copy, small_size) 
    blurred = pygame.transform.smoothscale(blurred, screen.get_size())
    # scales down the background image, which is a screen of the current game 
    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True # User closed the window
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    model.modal_selected_button = (model.modal_selected_button - 1) % 2
                    # if left arrow or 'a' is pressed, move selection to the left
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    model.modal_selected_button = (model.modal_selected_button + 1) % 2
                    # if right arrow or 'd' is pressed, move selection to the right
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return model.modal_selected_button == 0
                    # if enter or space is pressed, confirm selection
                elif event.key == pygame.K_ESCAPE:
                    return False
                    
            if event.type == pygame.MOUSEMOTION: # Update selection based on mouse position
                yes_rect = pygame.Rect(0, 0, 140, 50)
                no_rect = pygame.Rect(0, 0, 140, 50)
                box_y = SCREEN_HEIGHT//2 + int(SCREEN_HEIGHT*0.35*0.15)
                yes_rect.center = (SCREEN_WIDTH//2 - 110, box_y)
                no_rect.center = (SCREEN_WIDTH//2 + 110, box_y)
                # define buttons for yes and no selection
                
                if yes_rect.collidepoint(event.pos):
                    model.modal_selected_button = 0 # Yes button selected
                elif no_rect.collidepoint(event.pos):
                    model.modal_selected_button = 1 # No button selected
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return model.modal_selected_button == 0 # Confirm selection on left mouse click
        
        screen.blit(blurred, (0, 0)) # Draw the blurred background
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0)) # Darken the background
        draw_modal(screen, model.modal_selected_button) # Draw the modal dialog
        pygame.display.flip() # Update the display
        clock.tick(60)

def _global_quit(event: pygame.event.Event, screen: pygame.Surface, model: MenuModel) -> bool:
    # Handles global quit events, returns True if quit confirmed
    if event.type == pygame.QUIT:
        return show_confirm_quit(screen, model) # User clicked the window close button
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return show_confirm_quit(screen, model) # User pressed the Escape key
    return False
