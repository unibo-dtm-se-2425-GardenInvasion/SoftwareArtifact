import pygame
import sys
from pathlib import Path
from ..Model.menu_model import MenuModel, BackgroundModel
from ..View.menu_view import draw_menu, draw_modal, draw_pause_modal, get_pause_menu_button_rects
from ..Utilities.constants import*
from ..Model.plant_model import Player
from ..Model.setting_volume_model import SettingsModel
from .plant_controller import handle_player_input
from ..View.RunGame_view import draw_game
from .menu_controller_utilities import _global_quit, show_confirm_quit
from .options_controller import run_options

# ---------- modal helper ----------
def show_pause_menu(screen: pygame.Surface, model: MenuModel) -> str:
    clock = pygame.time.Clock()
    background_copy = screen.copy()
    small_size = (screen.get_width() // 3, screen.get_height() // 3)
    blurred = pygame.transform.smoothscale(background_copy, small_size)
    blurred = pygame.transform.smoothscale(blurred, screen.get_size())
    # Reset to middle button (Resume) by default
    pause_selected = 1  # 0=Main Menu, 1=Resume, 2=Quit
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit' # Quit the game
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    pause_selected = (pause_selected - 1) % 3 # Left arrow or A pressed
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    pause_selected = (pause_selected + 1) % 3 # right arrow or D pressed
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if pause_selected == 0:
                        return 'menu'
                    elif pause_selected == 1:
                        return 'resume'
                    else:
                        return 'quit'
                elif event.key == pygame.K_ESCAPE:
                    return 'resume'  # ESC in pause menu = resume
                    
            if event.type == pygame.MOUSEMOTION:
                menu_rect, resume_rect, quit_rect = get_pause_menu_button_rects()
                if menu_rect.collidepoint(event.pos):
                    pause_selected = 0
                elif resume_rect.collidepoint(event.pos):
                    pause_selected = 1
                elif quit_rect.collidepoint(event.pos):
                    pause_selected = 2
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_selected == 0:
                    return 'menu'
                elif pause_selected == 1:
                    return 'resume'
                else:
                    return 'quit'
        
        screen.blit(blurred, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        draw_pause_modal(screen, pause_selected)
        pygame.display.flip()
        clock.tick(60)

# ---------- game + options scenes ----------
def run_game(screen: pygame.Surface, model: MenuModel) -> None:
    #placeholder for actual game loop until the user quits
    clock = pygame.time.Clock()

    pkg_root = Path(__file__).resolve().parent.parent
    RunGame_bg_path = pkg_root / "Assets" / "images" / "RunGame01.png"
    RunGame_background = BackgroundModel(RunGame_bg_path) # load game background image

    # Create player sprite (plant) positioned at bottom center of screen
    player = Player((SCREEN_WIDTH//2, SCREEN_HEIGHT*0.95)) # position at bottom center
    player_group = pygame.sprite.GroupSingle(player) # group to manage the player sprite
    projectile_group = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get(): # event loop to handle user input
            if event.type == pygame.QUIT:
                if show_confirm_quit(screen, model):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Show pause menu instead of quit dialog
                action = show_pause_menu(screen, model)
                if action == 'quit':
                    pygame.quit()
                    sys.exit()
                elif action == 'menu':
                    running = False  # Exit game loop, return to main menu
                # If 'resume', continue the loop normally

        handle_player_input(player,projectile_group) # handle player movement input and auto shooting    
        # Update player (plant) and projectile position based on keyboard input
        player_group.update()
        projectile_group.update()

        # Draw black background or optionally your game background here
        draw_game(screen, RunGame_background, player_group, projectile_group)

        # Update the full display surface
        pygame.display.flip() # update the full display
        clock.tick(60)  # Limit FPS to 60

# ---------- main menu ----------
settings_model = SettingsModel()
settings_model.load()

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
                        run_options(screen, model, background_surf, background_rect, fonts, settings_model)
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
                            run_options(screen, model, background_surf, background_rect, fonts, settings_model)
            # this if handles the input from the mouse left click with an approximate hitbox
        draw_menu(screen, model, background_surf, background_rect, fonts) # draw the menu
        clock.tick(60) # limit to 60 FPS