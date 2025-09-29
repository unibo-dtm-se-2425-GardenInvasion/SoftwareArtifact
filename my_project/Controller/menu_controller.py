import pygame
import sys
from ..Model.menu_model import MenuModel
from ..View.menu_view import draw_menu, draw_modal
from ..Utilities.constants import*

# ---------- modal helper ----------
def show_confirm_quit(screen: pygame.Surface, model: MenuModel) -> bool:
    #function returns True if user confirmed quit
    clock = pygame.time.Clock() # clock to control frame rate
    # we use the clock to set how fast the screen update itself in order to reduce CPU usage

    background_copy = screen.copy() # used to capture screen content for blurring
    small_size = (screen.get_width() // 3, screen.get_height() // 3)  # adjust factor for blur strength
    blurred = pygame.transform.smoothscale(background_copy, small_size)
    blurred = pygame.transform.smoothscale(blurred, screen.get_size())
    # apply a blur effect to the confirm_quit window background

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # window X → quit
                return True
            
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    model.modal_selected_button = (model.modal_selected_button - 1) % 2
                    # used to switch between Yes/No buttons -> more left or up
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    model.modal_selected_button = (model.modal_selected_button + 1) % 2
                    # used to switch between Yes/No buttons -> move right or down
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return model.modal_selected_button == 0
                elif event.key == pygame.K_ESCAPE:      # ESC inside modal = No
                    return False
            # this if handles the input from the keyboard

            if event.type == pygame.MOUSEMOTION:
                # highlight button under cursor
                yes_rect = pygame.Rect(0, 0, 140, 50)
                no_rect  = pygame.Rect(0, 0, 140, 50)
                box_y = SCREEN_HEIGHT//2 + int(SCREEN_HEIGHT*0.35*0.15)
                yes_rect.center = (SCREEN_WIDTH//2 - 110, box_y)
                no_rect.center  = (SCREEN_WIDTH//2 + 110, box_y)
                if yes_rect.collidepoint(event.pos):
                    model.modal_selected_button = 0
                elif no_rect.collidepoint(event.pos):
                    model.modal_selected_button = 1
            # this if handles the input from the mouse movement

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return model.modal_selected_button == 0
            # this if handles the input from the mouse left click

        screen.blit(blurred, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # semi-transparent overlay to a darken the background
        screen.blit(overlay, (0, 0))
        draw_modal(screen, model.modal_selected_button) # draw the modal window
        pygame.display.flip() # update the full display
        clock.tick(60) # limit to 60 FPS

def _global_quit(event: pygame.event.Event, screen: pygame.Surface, model: MenuModel) -> bool:
    # returns True if user confirmed quit by pressing the ESC key or window X
    if event.type == pygame.QUIT:
        return show_confirm_quit(screen, model)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return show_confirm_quit(screen, model)
    return False
    # centralized helper to handle global quit events (QUIT or ESC key)

# ---------- game + options scenes ----------
def run_game(screen: pygame.Surface, model: MenuModel) -> None:
    #placeholder for actual game loop until the user quits

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if _global_quit(event, screen, model):
                pygame.quit(); sys.exit() # handle the global quit
        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

def run_options(screen: pygame.Surface, model: MenuModel) -> None:
    #placeholder for the option menu until the user quits

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if _global_quit(event, screen, model):
                pygame.quit(); sys.exit() # handle the global quit
        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

# ---------- main menu ----------
def main_menu_loop(screen: pygame.Surface,
                   background_surf: pygame.Surface | None,
                   background_rect: pygame.Rect | None,
                   fonts: tuple):
    # main menu loop, returns when user starts game or options
    # it handles user's input and enter either run_game or run_options
    model  = MenuModel()
    clock  = pygame.time.Clock()
    running = True

    while running: # loop reads events, updates model, draws view
        for event in pygame.event.get():
            if _global_quit(event, screen, model):
                running = False
                break
            # this if handles the global quit events (QUIT or ESC key)

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    model.selected_index = (model.selected_index - 1) % len(model.menu_items)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    model.selected_index = (model.selected_index + 1) % len(model.menu_items)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if model.selected_index == 0:
                        run_game(screen, model)
                    else:
                        run_options(screen, model)
            # this if handles the input from the keyboard (UP/W and DOWN/S to navigate, ENTER/SPACE to select)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # simple click detection using View-computed rects
                mx, my = event.pos
                line_h = SCREEN_HEIGHT*0.1
                for i in range(len(model.menu_items)):
                    cy = SCREEN_HEIGHT*0.4 + i*line_h # compute center y of each menu item, i.e. new game and options
                    if abs(my - cy) < line_h*0.4: # checks if the mouse y is close enough to the center of the item
                        # within 40% of the line height
                        model.selected_index = i
                        if i == 0:
                            run_game(screen, model)
                        else:
                            run_options(screen, model)
            # this if handles the input from the mouse left click with an approximate hitbox
        draw_menu(screen, model, background_surf, background_rect, fonts) # draw the menu
        clock.tick(60) # limit to 60 FPS