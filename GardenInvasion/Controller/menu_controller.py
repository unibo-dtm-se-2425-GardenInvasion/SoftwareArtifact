import pygame
import sys
from ..Model.menu_model import MenuModel
from ..View.menu_view import draw_menu
from ..Utilities.constants import*
from ..Model.setting_volume_model import SettingsModel
from .menu_controller_utilities import _global_quit
from .options_controller import run_options
from .NewGame_controller import run_game
from ..Model.sound_manager_model import SoundManager

# ---------- main menu ----------
settings_model = SettingsModel()
settings_model.load()
sound_manager = SoundManager(settings_model) # Initialize sound manager with settings

def main_menu_loop(screen: pygame.Surface,
                   background_surf: pygame.Surface | None,
                   background_rect: pygame.Rect | None,
                   fonts: tuple,):
    # main menu loop, returns when user starts game or options
    # it handles user's input and enter either run_game or run_options
    model  = MenuModel()
    clock  = pygame.time.Clock()

    sound_manager.play_music('menu', loops=-1, fade_ms=2000) # Play menu music with fade-in

    running = True

    while running: # loop reads events, updates model, draws view
        for event in pygame.event.get():
            if _global_quit(event, screen, model):
                print("Global quit confirmed from main menu")
                sound_manager.stop_music(fade_ms=1000) # Fade out music over 1 second
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
                        print ("Starting Game from enter/space key")
                        sound_manager.stop_music(fade_ms=500) # Fade out menu music quickly
                        run_game(screen, model, settings_model, sound_manager)  # Pass sound_manager
                        # Restart menu music when returning
                        sound_manager.play_music('menu', loops=-1, fade_ms=2000) # Play menu music with fade-in
                    else:
                        print ("Opening Options from enter/space key")
                        run_options(screen, model, background_surf, background_rect, fonts, settings_model, sound_manager)
            # this if handles the input from the keyboard (UP/W and DOWN/S to navigate, ENTER/SPACE to select)
            
            elif event.type == pygame.MOUSEMOTION: # mouse hover detection
                mx, my = event.pos # get mouse position
                line_h = SCREEN_HEIGHT * 0.1
                for i in range(len(model.menu_items)):
                    cy = SCREEN_HEIGHT * 0.4 + i * line_h  # Center y of each menu item
                    if abs(my - cy) < line_h * 0.4:  # Within 40% of line height
                        model.selected_index = i  # Update selection on hover
                        break

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
                            print ("Starting Game from Mouse Click")

                            sound_manager.stop_music(fade_ms=500) # Fade out menu music quickly
                            run_game(screen, model, settings_model, sound_manager)  # Pass sound_manager
                            # Restart menu music when returning
                            sound_manager.play_music('menu', loops=-1, fade_ms=2000) # Play menu music with fade-in
                        else:
                            print ("Opening Options from Mouse Click")
                            run_options(screen, model, background_surf, background_rect, fonts, settings_model, sound_manager)
            # this if handles the input from the mouse left click with an approximate hitbox
        draw_menu(screen, model, background_surf, background_rect, fonts) # draw the menu
        clock.tick(60) # limit to 60 FPS