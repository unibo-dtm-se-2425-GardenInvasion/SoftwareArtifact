import pygame
import sys
from .. import logger
from ..Model.menu_model import MenuModel
from ..View.menu_view import draw_menu
from ..Utilities.constants import*
from ..Model.setting_volume_model import SettingsModel
from .menu_controller_utilities import _global_quit
from .options_controller import run_options
from .NewGame_controller import run_game
from ..Model.sound_manager_model import SoundManager

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

    # Priming draw so hit-test rects are available before the first event is processed
    _, click_rects = draw_menu(screen, model, background_surf, background_rect, fonts)
    pygame.display.flip()

    while running: # loop reads events, updates model, draws view
        for event in pygame.event.get():
            if _global_quit(event, screen, model):
                logger.debug("Global quit confirmed from main menu")
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
                        logger.debug("Starting Game from enter/space key")
                        sound_manager.stop_music(fade_ms=500) # Fade out menu music quickly
                        run_game(screen, model, settings_model, sound_manager)  # Pass sound_manager
                        # Restart menu music when returning
                        sound_manager.play_music('menu', loops=-1, fade_ms=2000) # Play menu music with fade-in
                    else:
                        logger.debug("Opening Options from enter/space key")
                        run_options(screen, model, background_surf, background_rect, fonts, settings_model, sound_manager)
            # this if handles the input from the keyboard (UP/W and DOWN/S to navigate, ENTER/SPACE to select)
            
            elif event.type == pygame.MOUSEMOTION: # mouse hover detection
                for i, rect in enumerate(click_rects):
                    if rect.collidepoint(event.pos):
                        model.selected_index = i  # Update selection on hover
                        break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # click detection using View-computed hit-test rects
                for i, rect in enumerate(click_rects):
                    if rect.collidepoint(event.pos):
                        model.selected_index = i
                        if i == 0:
                            logger.debug("Starting Game from Mouse Click")

                            sound_manager.stop_music(fade_ms=500) # Fade out menu music quickly
                            run_game(screen, model, settings_model, sound_manager)  # Pass sound_manager
                            # Restart menu music when returning
                            sound_manager.play_music('menu', loops=-1, fade_ms=2000) # Play menu music with fade-in
                        else:
                            logger.debug("Opening Options from Mouse Click")
                            run_options(screen, model, background_surf, background_rect, fonts, settings_model, sound_manager)
            # this if handles the input from the mouse left click with an approximate hitbox
        _, click_rects = draw_menu(screen, model, background_surf, background_rect, fonts) # draw the menu
        pygame.display.flip() # update the display, matching every other controller's loop
        clock.tick(60) # limit to 60 FPS