import pygame
import sys
import webbrowser # Added import for webbrowser later used for the email
from pathlib import Path

from .menu_controller_utilities import show_confirm_quit
from ..Model.menu_model import MenuModel
from ..Model.options_model import OptionsModel, VolumeModel
from ..Model.setting_volume_model import SettingsModel
from ..View.options_view import draw_options_menu, draw_contact_modal, draw_volume_menu
from ..Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .skin_selection_controller import run_skin_selection

def show_contact_confirmation(screen: pygame.Surface, options_model: OptionsModel) -> bool:
    clock = pygame.time.Clock()
    background_copy = screen.copy()
    small_size = (screen.get_width() // 3, screen.get_height() // 3)
    blurred = pygame.transform.smoothscale(background_copy, small_size)
    blurred = pygame.transform.smoothscale(blurred, screen.get_size())
    # create a blurred background screen for the pop up regarding the contact us option
    options_model.modal_selected_button = 0 # set default selected button to "Open Email Client"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Handle quit event
                #print ("Quit event detected in contact confirmation modal")
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    # print ("Left key detected in contact confirmation modal, open email client")
                    options_model.modal_selected_button = 0 # Select "Open Email Client"
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    # print ("Right key detected in contact confirmation modal, back to options menu")
                    options_model.modal_selected_button = 1 # Select "Back"
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # print ("Enter/Space key detected in contact confirmation modal, open email client")
                    return options_model.modal_selected_button == 0 # Return True if "Open Email Client" is selected
                elif event.key == pygame.K_ESCAPE:
                    # print ("Escape key detected in contact confirmation modal, back to options menu")
                    return False
                
            elif event.type == pygame.MOUSEMOTION: # Handle mouse hover over buttons
                open_rect = pygame.Rect(0, 0, 120, 45)
                back_rect = pygame.Rect(0, 0, 120, 45)
                box_height = int(SCREEN_HEIGHT * 0.4)
                buttons_y = SCREEN_HEIGHT // 2 + int(box_height * 0.23)

                open_rect.center = (SCREEN_WIDTH // 2 - 80, buttons_y) # "Open Email" button to the left
                back_rect.center = (SCREEN_WIDTH // 2 + 80, buttons_y) # "Back" button to the right

                if open_rect.collidepoint(event.pos):
                    options_model.modal_selected_button = 0 # Hovering over "Open Email Client"
                elif back_rect.collidepoint(event.pos):
                    options_model.modal_selected_button = 1 # Hovering over "Back"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return options_model.modal_selected_button == 0 # Return True if "Open Email Client" is selected

        screen.blit(blurred, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA) 
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0)) # Darken the background
        draw_contact_modal(screen, options_model.modal_selected_button)
        pygame.display.flip()
        clock.tick(60)

def run_volume_menu(screen: pygame.Surface, 
                    model: MenuModel,
                    background_surf, 
                    background_rect, 
                    fonts,
                    initial_volume: int) -> int:
   #Volume menu loop
    volume_model = VolumeModel(initial_volume) # Initialize volume model with the current volume
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Show quit confirmation
                print ("'X' Click detected, global quit shown in volume submenu")
                if show_confirm_quit(screen, model):
                    print("Click detected, global quit from volume submenu")
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    volume_model.volume = max(0, volume_model.volume - 5) # Adjust volume left
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    volume_model.volume = min(100, volume_model.volume + 5) # adjust volume right
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    print ("Enter/Space key detected in volume submenu, exiting volume menu")
                    running = False # Exit volume menu
                elif event.key == pygame.K_ESCAPE:
                    print ("Escape key detected in volume submenu, global quit shown")
                    if show_confirm_quit(screen, model):
                        print("Enter/space key detected, Global quit from volume submenu")
                        pygame.quit()
                        sys.exit()
                        
            if event.type == pygame.MOUSEMOTION:
                # Get back button rect for hover detection
                back_rect = pygame.Rect(0, 0, 60, 30)
                back_rect.center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.61)
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Get back button rect for click detection
                back_rect = pygame.Rect(0, 0, 60, 30)
                back_rect.center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.61)
                
                if back_rect.collidepoint(event.pos):
                    print ("Back button clicked in volume menu, exiting volume menu")
                    running = False # Exit volume menu
        back_rect = draw_volume_menu(screen, volume_model, background_surf, background_rect, fonts)
        pygame.display.flip()
        clock.tick(60)
    
    return volume_model.volume

def run_options(screen: pygame.Surface, 
                model: MenuModel, 
                background_surf, 
                background_rect, 
                fonts,
                settings_model: SettingsModel) -> None:
    # Options menu loop
    options_model = OptionsModel()
    options_model.volume = settings_model.volume
    clock = pygame.time.Clock()
    running = True
    
    label_rects = [] # Store label_rects from draw
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("'X' click detected in options menu, global quit shown")
                if show_confirm_quit(screen, model):
                    print("Click detected, global quit from options menu")
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Escape key detected in options menu, global quit shown")
                if show_confirm_quit(screen, model):
                    print("Enter/space key detected, global quit from options menu")
                    pygame.quit()
                    sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    options_model.selected_index = (options_model.selected_index - 1) % len(options_model.options_items)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    options_model.selected_index = (options_model.selected_index + 1) % len(options_model.options_items)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if options_model.selected_index == 0:  # Volume
                        print("Enter/Space key detected on Volume option, opening volume menu")
                        options_model.volume = run_volume_menu(screen, model, background_surf, background_rect, fonts, options_model.volume)
                        settings_model.volume = options_model.volume
                        settings_model.save()
                    
                    elif options_model.selected_index == 1:  # Skin Personalization
                        print("Enter/Space key detected on Skin Personalization, opening skin selector")
                        result = run_skin_selection(screen, model, background_surf, background_rect, fonts, settings_model)
                        if result == 'main_menu':
                            print("Skin selected, returning to main menu")
                            running = False

                    elif options_model.selected_index == 2:  # Contact Us
                        print("Enter/Space key detected on Contact Us option, showing contact confirmation modal")
                        if show_contact_confirmation(screen, options_model):
                            email = "GardenInvasion@email.com"
                            mailto_url = "mailto:" + email
                            webbrowser.open(mailto_url)
                            print(f"Enter/Space key. Opening email client with URL: {mailto_url}")
                        else:
                            print("Contact Us confirmation modal closed without opening email client")

                    elif options_model.selected_index == 3:  # Back
                        print("Enter/Space key detected on Back option, exiting options menu")
                        running = False
            
            # Mouse hover detection to highlight options
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                # Check which option is being hovered over
                for i, rect in enumerate(label_rects):
                    if rect.collidepoint(event.pos):
                        options_model.selected_index = i  # Highlight hovered option
                        break
            
            # Use actual label_rects from view for click detection
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Check which option was clicked using actual rects
                for i, rect in enumerate(label_rects):
                    if rect.collidepoint(event.pos):
                        options_model.selected_index = i
                        
                        if i == 0:  # Volume
                            print("Volume option clicked, opening volume menu")
                            options_model.volume = run_volume_menu(screen, model, background_surf, background_rect, fonts, options_model.volume)
                            settings_model.volume = options_model.volume
                            settings_model.save()

                        elif i == 1:  # Skin Personalization
                            print("Skin Personalization clicked, opening skin selector")
                            result = run_skin_selection(screen, model, background_surf, background_rect, fonts, settings_model)
                            if result == 'main_menu':
                                print("Skin selected, returning to main menu")
                                running = False

                        elif i == 2:  # Contact Us
                            print("Contact Us option clicked, showing contact confirmation modal")
                            if show_contact_confirmation(screen, options_model):
                                email = "GardenInvasion@email.com"
                                mailto_url = "mailto:" + email
                                webbrowser.open(mailto_url)
                                print(f"Click detected. Opening email client with URL: {mailto_url}")
                            else:
                                print("Contact Us confirmation modal closed without opening email client")

                        elif i == 3:  # Back
                            print("Back option clicked, exiting options menu")
                            running = False
                        break
                if not running: # Exit the loop if "Back" was clicked
                    break
        
        # Get actual label_rects from view
        label_rects = draw_options_menu(screen, options_model, background_surf, background_rect, fonts)
        pygame.display.flip()
        clock.tick(60)