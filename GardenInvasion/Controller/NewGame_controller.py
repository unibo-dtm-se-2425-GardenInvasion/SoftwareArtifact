import pygame
import sys
from pathlib import Path
from ..Model.menu_model import MenuModel, BackgroundModel
from ..View.menu_view import draw_pause_modal, get_pause_menu_button_rects
from ..Utilities.constants import*
from ..Model.plant_model import Player
from ..Model.wallnut_model import WallNutManager
from .plant_controller import handle_player_input
from .wallnut_controller import handle_wallnut_placement, handle_wallnut_collisions
from ..View.RunGame_view import draw_game
from .menu_controller_utilities import show_confirm_quit
from ..Model.setting_volume_model import SettingsModel
from ..Model.sound_manager_model import SoundManager

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
                print ("Quit event detected in pause menu, Bye Bye!")
                return 'quit' # Quit the game
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    pause_selected = (pause_selected - 1) % 3 # Left arrow or A pressed
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    pause_selected = (pause_selected + 1) % 3 # right arrow or D pressed
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if pause_selected == 0:
                        print("Enter/Space key detected, Returning to Main Menu from Pause Menu")
                        return 'menu'
                    elif pause_selected == 1:
                        print("Enter/Space key detected, Resuming Game from Pause Menu")
                        return 'resume'
                    else:
                        print("Enter/Space key detected, Quitting Game from Pause Menu, Bye Bye!")
                        return 'quit'
                elif event.key == pygame.K_ESCAPE:
                    print("Resuming Game from Pause Menu via ESC key")
                    return 'resume'  # ESC in pause menu = resume
                    
            if event.type == pygame.MOUSEMOTION:
                menu_rect, resume_rect, quit_rect = get_pause_menu_button_rects()# get button rects

                # Calculate dialog box position (matching draw_pause_modal positioning)
                box_width, box_height = int(SCREEN_WIDTH * 0.7), int(SCREEN_HEIGHT * 0.35)
                box_rect = pygame.Rect(0, 0, box_width, box_height)
                box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                
                # Position buttons relative to dialog box
                buttons_y = box_rect.top + int(box_height * 0.65)
                menu_rect.center = (box_rect.centerx - 160, buttons_y)
                resume_rect.center = (box_rect.centerx, buttons_y)
                quit_rect.center = (box_rect.centerx + 160, buttons_y)

                if menu_rect.collidepoint(event.pos):
                    pause_selected = 0
                elif resume_rect.collidepoint(event.pos):
                    pause_selected = 1
                elif quit_rect.collidepoint(event.pos):
                    pause_selected = 2
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_rect, resume_rect, quit_rect = get_pause_menu_button_rects()
                if pause_selected == 0:
                    print ("Returning to Main Menu from Pause Menu via Mouse Click")
                    return 'menu'
                elif pause_selected == 1:
                    print ("Resuming Game from Pause Menu via Mouse Click")
                    return 'resume'
                else:
                    print ("Quitting Game from Pause Menu via Mouse Click, Bye Bye!")
                    return 'quit'
        
        screen.blit(blurred, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        draw_pause_modal(screen, pause_selected)
        pygame.display.flip()
        clock.tick(60)

# ---------- game + options scenes ----------
def run_game(screen: pygame.Surface, model: MenuModel, settings_model: SettingsModel) -> None:
    #placeholder for actual game loop until the user quits
    clock = pygame.time.Clock()

    pkg_root = Path(__file__).resolve().parent.parent
    RunGame_bg_path = pkg_root / "Assets" / "images" / "RunGame01.png"
    RunGame_background = BackgroundModel(RunGame_bg_path) # load game background image

    sound_manager = SoundManager(settings_model)  # Initialize sound manager with settings

    # Create player with selected skin
    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.95), settings_model)  # Pass settings_model
    player_group = pygame.sprite.GroupSingle(player)
    projectile_group = pygame.sprite.Group()

    # create wall-nut manager with 4 wall-nut slots
    wallnut_manager = WallNutManager(
        player_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.95),
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        sound_manager=sound_manager # Pass sound manager for sound effects
    )
    wallnut_manager.place_all_wallnuts()  # Place all 4 wall-nuts at game start

    running = True
    while running:
        for event in pygame.event.get(): # event loop to handle user input
            if event.type == pygame.QUIT:
                print ("Quit event detected in game loop")
                if show_confirm_quit(screen, model):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Show pause menu instead of quit dialog
                print("Escape key pressed, Pause Menu shown")
                action = show_pause_menu(screen, model)
                if action == 'quit':
                    pygame.quit()
                    sys.exit()
                elif action == 'menu':
                    running = False  # Exit game loop, return to main menu
                # If 'resume', continue the loop normally

        handle_player_input(player,projectile_group, sound_manager) # handle player movement input and auto shooting    
        # Handle wall-nut placement (keys 1-4)
        keys = pygame.key.get_pressed()
        handle_wallnut_placement(keys, wallnut_manager)

        # Update player (plant) and projectile position based on keyboard input
        player_group.update()
        projectile_group.update()
        wallnut_manager.update()
        # Handle collisions (player projectiles blocked by wall-nuts)
        handle_wallnut_collisions(wallnut_manager, projectile_group)

        # Draw black background or optionally your game background here
        draw_game(screen, RunGame_background, player_group, projectile_group, wallnut_manager.get_wallnuts())

        # Update the full display surface
        pygame.display.flip() # update the full display
        clock.tick(60)  # Limit FPS to 60
