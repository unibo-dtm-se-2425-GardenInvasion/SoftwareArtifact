import pygame
import sys
from .. import logger
from ..Model.menu_model import MenuModel
from ..Model.skin_selection_model import SkinSelectionModel
from ..Model.setting_volume_model import SettingsModel
from ..View.skin_selection_view import draw_skin_selection_menu
from .menu_controller_utilities import show_confirm_quit


def run_skin_selection(screen: pygame.Surface,
                       model: MenuModel,
                       background_surf,
                       background_rect,
                       fonts,
                       settings_model: SettingsModel) -> str:
    
    skin_model = SkinSelectionModel()
    
    # Load current skin from settings
    skin_model.set_skin_by_id(settings_model.player_skin)
    
    clock = pygame.time.Clock()
    running = True
    return_to = 'back'  # Default: return to options menu

    # Priming draw so hit-test rects are available before the first event is processed
    back_rect, skin_hit_rects = draw_skin_selection_menu(screen, skin_model, background_surf, background_rect, fonts)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            # Handle universal quit via X button
            if event.type == pygame.QUIT:
                logger.debug("'X' click detected in skin selection menu, global quit shown")
                if show_confirm_quit(screen, model):
                    logger.debug("Click detected, global quit from skin selection menu")
                    pygame.quit()
                    sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                # Handle ESC key for universal quit
                if event.key == pygame.K_ESCAPE:
                    logger.debug("Escape key detected in skin selection menu, global quit shown")
                    if show_confirm_quit(screen, model):
                        logger.debug("Enter/space key detected, global quit from skin selection menu")
                        pygame.quit()
                        sys.exit()
                
                # Handle UP/DOWN navigation between skins and Back button
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if skin_model.back_button_selected:
                        # Move from Back button to last skin
                        skin_model.deselect_back_button()
                        logger.debug(f"Up key: Moved to skins, selected {skin_model.get_selected_skin().display_name}")
                
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if not skin_model.back_button_selected:
                        # Move from skins to Back button
                        skin_model.select_back_button()
                        logger.debug("Down key: Selected Back button")
                
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if not skin_model.back_button_selected:
                        # Move to previous skin (only when not on Back button)
                        skin_model.select_previous_skin()
                        logger.debug(f"Left/A key: Selected {skin_model.get_selected_skin().display_name}")
                
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if not skin_model.back_button_selected:
                        # Move to next skin (only when not on Back button)
                        skin_model.select_next_skin()
                        logger.debug(f"Right/D key: Selected {skin_model.get_selected_skin().display_name}")
                
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if skin_model.back_button_selected:
                        # Back button is selected, go back to options
                        logger.debug("Enter/Space on Back button: Returning to options menu")
                        return_to = 'back'
                        running = False
                    else:
                        # Confirm skin selection (persisted by the caller once this menu returns)
                        selected_skin = skin_model.get_selected_skin()
                        settings_model.player_skin = selected_skin.skin_id
                        logger.debug(f"Enter/Space key: Skin changed to {selected_skin.display_name}")
                        return_to = 'main_menu'
                        running = False
            
            # Handle mouse hover to highlight skins
            elif event.type == pygame.MOUSEMOTION:
                if back_rect and back_rect.collidepoint(event.pos):
                    skin_model.select_back_button()
                else:
                    skin_model.deselect_back_button()

                    # Check if hovering over any skin, using the View-computed hit-test rects
                    for i, rect in enumerate(skin_hit_rects):
                        if rect.collidepoint(event.pos):
                            skin_model.selected_index = i
                            break # Stop checking after first match
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                # Use the actual back_rect from view
                if back_rect and back_rect.collidepoint(event.pos):
                    logger.debug("Back button clicked, returning to options")
                    return_to = 'back'
                    running = False
                    break
                # Check if player clicked on a skin preview, using the View-computed hit-test rects
                for i, rect in enumerate(skin_hit_rects):
                    if rect.collidepoint(event.pos):
                        skin_model.selected_index = i
                        skin_model.current_skin_id = skin_model.available_skins[i].skin_id

                        # Confirm selection on click (persisted by the caller once this menu returns)
                        selected_skin = skin_model.get_selected_skin()
                        settings_model.player_skin = selected_skin.skin_id
                        logger.debug(f"Mouse click: Skin changed to {selected_skin.display_name}")
                        return_to = 'main_menu'
                        running = False
                        break
        
        # Draw and get the actual back_rect and skin hit-test rects
        back_rect, skin_hit_rects = draw_skin_selection_menu(screen, skin_model, background_surf, background_rect, fonts)
        pygame.display.flip()
        clock.tick(60)
        
    return return_to
