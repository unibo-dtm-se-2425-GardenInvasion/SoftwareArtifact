import pygame
import sys
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
    # Run the skin selection menu loop

    skin_model = SkinSelectionModel()
    # Load current skin from settings
    skin_model.set_skin_by_id(settings_model.player_skin)
    
    clock = pygame.time.Clock()
    running = True
    return_to = 'back'  # Default: return to options menu
    back_rect = None # To store the Back button rect for mouse interaction
    
    while running:
        for event in pygame.event.get():
            # Handle universal quit via X button
            if event.type == pygame.QUIT:
                print("'X' click detected in skin selection menu, global quit shown")
                if show_confirm_quit(screen, model):
                    print("Click detected, global quit from skin selection menu")
                    pygame.quit()
                    sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                # Handle ESC key for universal quit
                if event.key == pygame.K_ESCAPE:
                    print("Escape key detected in skin selection menu, global quit shown")
                    if show_confirm_quit(screen, model):
                        print("Enter/space key detected, global quit from skin selection menu")
                        pygame.quit()
                        sys.exit()
                
                # Handle UP/DOWN navigation between skins and Back button
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if skin_model.back_button_selected:
                        # Move from Back button to last skin
                        skin_model.deselect_back_button()
                        print(f"Up key: Moved to skins, selected {skin_model.get_selected_skin().display_name}")
                
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if not skin_model.back_button_selected:
                        # Move from skins to Back button
                        skin_model.select_back_button()
                        print("Down key: Selected Back button")
                
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if not skin_model.back_button_selected:
                        # Move to previous skin (only when not on Back button)
                        skin_model.select_previous_skin()
                        print(f"Left/A key: Selected {skin_model.get_selected_skin().display_name}")
                
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if not skin_model.back_button_selected:
                        # Move to next skin (only when not on Back button)
                        skin_model.select_next_skin()
                        print(f"Right/D key: Selected {skin_model.get_selected_skin().display_name}")
                
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if skin_model.back_button_selected:
                        # Back button is selected, go back to options
                        print("Enter/Space on Back button: Returning to options menu")
                        return_to = 'back'
                        running = False
                    else:
                        # Confirm skin selection and save
                        selected_skin = skin_model.get_selected_skin()
                        settings_model.player_skin = selected_skin.skin_id
                        settings_model.save()
                        print(f"Enter/Space key: Skin changed to {selected_skin.display_name}")
                        return_to = 'main_menu'
                        running = False
            
            # Handle mouse hover to highlight skins
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos # Mouse coordinates

                if back_rect and back_rect.collidepoint(event.pos):
                    skin_model.select_back_button()
                else:
                    skin_model.deselect_back_button()
                    
                    # Check if hovering over any skin
                    total_skins = skin_model.get_total_skins()
                    spacing = screen.get_width() * 0.7 / (total_skins + 1)
                    start_x = screen.get_width() * 0.15
                    
                    for i in range(total_skins): # Iterate through skins
                        x = start_x + spacing * (i + 1)
                        y = screen.get_height() * 0.45
                        if abs(mx - x) < 50 and abs(my - y) < 50: # Within preview bounds
                            skin_model.selected_index = i
                            break # Stop checking after first match
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                mx, my = event.pos
                # Use the actual back_rect from view
                if back_rect and back_rect.collidepoint(event.pos):
                    print("Back button clicked, returning to options")
                    return_to = 'back'
                    running = False
                    break
                # Check if player clicked on a skin preview
                total_skins = skin_model.get_total_skins()
                spacing = screen.get_width() * 0.7 / (total_skins + 1)
                start_x = screen.get_width() * 0.15
                
                for i in range(total_skins):
                    x = start_x + spacing * (i + 1)
                    y = screen.get_height() * 0.45
                    # Check if click is within preview bounds
                    if abs(mx - x) < 50 and abs(my - y) < 50:
                        skin_model.selected_index = i
                        skin_model.current_skin_id = skin_model.available_skins[i].skin_id
                        
                        # Confirm selection immediately on click
                        selected_skin = skin_model.get_selected_skin()
                        settings_model.player_skin = selected_skin.skin_id
                        settings_model.save()
                        print(f"Mouse click: Skin changed to {selected_skin.display_name}")
                        return_to = 'main_menu'
                        running = False
                        break
        
        # Draw and get the actual back_rect
        back_rect = draw_skin_selection_menu(screen, skin_model, background_surf, background_rect, fonts)
        pygame.display.flip()
        clock.tick(60)
        
    return return_to
