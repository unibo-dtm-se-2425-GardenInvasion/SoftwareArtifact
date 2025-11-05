import pygame
from ..Utilities.constants import *

def draw_pause_modal(screen, selected_button=1):

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))  # Draw overlay to screen
    
    box_width, box_height = int(SCREEN_WIDTH * 0.7), int(SCREEN_HEIGHT * 0.35)  # Calculate dialog box dimensions
    box_rect = pygame.Rect(0, 0, box_width, box_height)  # Create rectangle for dialog box
    box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Center the dialog box on screen
    
    # Draw dialog box background and border
    pygame.draw.rect(screen, (230, 230, 230), box_rect, border_radius=10)  # Light gray background
    pygame.draw.rect(screen, (40, 40, 40), box_rect, width=3, border_radius=10)  # Dark border outline
    
    # Title text
    font_title = pygame.font.SysFont("Arial", 30)  # Create font for title
    text_surface = font_title.render("Game Paused", True, (40, 40, 40))  # Render title text
    text_rect = text_surface.get_rect(center=(box_rect.centerx, box_rect.top + box_height * 0.3))  # Position title
    screen.blit(text_surface, text_rect)  # Draw title to screen
    
    # Three button rectangles for pause menu options
    font_btn = pygame.font.SysFont("Arial", 24)  # Create font for button labels
    btn_w, btn_h = 140, 50  # Button dimensions
    
    menu_rect = pygame.Rect(0, 0, btn_w, btn_h)  # Main Menu button rectangle
    resume_rect = pygame.Rect(0, 0, btn_w, btn_h)  # Resume button rectangle
    quit_rect = pygame.Rect(0, 0, btn_w, btn_h)  # Quit button rectangle
    
    buttons_y = box_rect.top + int(box_height * 0.65)  
    menu_rect.center = (box_rect.centerx - 160, buttons_y)  
    resume_rect.center = (box_rect.centerx, buttons_y) 
    quit_rect.center = (box_rect.centerx + 160, buttons_y)
    
    # Button colors based on which is currently selected (highlighted)
    menu_color = (180, 220, 180) if selected_button == 0 else (210, 210, 210)  # Green if selected, gray otherwise
    resume_color = (180, 220, 180) if selected_button == 1 else (210, 210, 210) 
    quit_color = (180, 220, 180) if selected_button == 2 else (210, 210, 210)  
    
    # Draw button backgrounds with appropriate colors
    pygame.draw.rect(screen, menu_color, menu_rect, border_radius=8)  # Main Menu button background
    pygame.draw.rect(screen, resume_color, resume_rect, border_radius=8)  
    pygame.draw.rect(screen, quit_color, quit_rect, border_radius=8)  
    
    # Draw button borders (outlines)
    pygame.draw.rect(screen, (40, 40, 40), menu_rect, width=2, border_radius=8)  # Main Menu border
    pygame.draw.rect(screen, (40, 40, 40), resume_rect, width=2, border_radius=8) 
    pygame.draw.rect(screen, (40, 40, 40), quit_rect, width=2, border_radius=8)  
    
    # Button text labels
    menu_label = font_btn.render("Main Menu", True, (20, 20, 20))  # Render "Main Menu" text
    resume_label = font_btn.render("Resume", True, (20, 20, 20)) 
    quit_label = font_btn.render("Quit", True, (20, 20, 20))  
    
    # Draw button labels centered on their respective buttons
    screen.blit(menu_label, menu_label.get_rect(center=menu_rect.center))  # Draw Main Menu label
    screen.blit(resume_label, resume_label.get_rect(center=resume_rect.center))  
    screen.blit(quit_label, quit_label.get_rect(center=quit_rect.center))  

def get_pause_menu_button_rects():
    btn_w, btn_h = 140, 50  # Define button dimensions
    menu_rect = pygame.Rect(0, 0, btn_w, btn_h)  # Create Main Menu button rect
    resume_rect = pygame.Rect(0, 0, btn_w, btn_h)  
    quit_rect = pygame.Rect(0, 0, btn_w, btn_h)  
    return menu_rect, resume_rect, quit_rect  # Return all three rects to controller

def draw_menu(screen, model, background_surf, background_rect, fonts):
    if background_surf:
        screen.fill((0, 0, 0))  # Fill screen with black
        screen.blit(background_surf, background_rect)  # Draw background image
    else:
        screen.fill((0, 0, 50))  # Fill with dark blue if no background image available

    item_font, inst_font, title_font = fonts  # Unpack font tuple (item, instruction, title fonts)
    title_text = title_font.render("Garden Invasion", True, GREEN_SI)  # Render game title
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.25))  # Position title at top center
    screen.blit(title_text, title_rect)  # Draw title to screen
    
    label_rects = []  # List to store menu item rectangles for click detection
    for idx, label in enumerate(model.menu_items):  # Loop through menu items (e.g., "New Game", "Options")
        text_surf = item_font.render(label, True, GREEN_SI)  # Render menu item text
        rect = text_surf.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.4 + idx * SCREEN_HEIGHT * 0.1))  # Position item vertically
        label_rects.append(rect)  # Store rect for controller to detect clicks/hovers
        screen.blit(text_surf, rect)  # Draw menu item text to screen
        if idx == model.selected_index:  # If this item is currently selected
            draw_selection_arrows(screen, rect, color=GREEN_SI)  # Draw arrows around selected item

    inst_text = inst_font.render("Press ESC or close window to exit", True, BLACK)  # Render instruction text
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65))  # Position instructions at bottom
    screen.blit(inst_text, inst_rect)  # Draw instructions to screen

    pygame.display.flip()  # Update the display to show all drawn elements
    return label_rects  # Return menu item rects to controller for input detection

def draw_selection_arrows(screen, target_rect, color=(98, 222, 109)):
    left_x = target_rect.left - 30  # Position left arrow
    mid_y = target_rect.centery  # Vertical center of the item
    left_arrow = [(left_x, mid_y), (left_x + 12, mid_y - 8), (left_x + 12, mid_y + 8)]  # Left-pointing triangle
    pygame.draw.polygon(screen, color, left_arrow)  # Draw left arrow
    
    right_x = target_rect.right + 30  # Position right arrow
    right_arrow = [(right_x, mid_y), (right_x - 12, mid_y - 8), (right_x - 12, mid_y + 8)]  # Right-pointing triangle
    pygame.draw.polygon(screen, color, right_arrow)  # Draw right arrow

def draw_modal(screen, selected_button=1):
    # Draws a quit confirmation modal dialog with Yes/No buttons.
    # selected_button: 0 = Yes, 1 = No
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  # Create transparent overlay surface
    overlay.fill((0, 0, 0, 150))  # Semi-transparent black overlay to darken background
    screen.blit(overlay, (0, 0))  # Draw overlay to screen

    box_width, box_height = int(SCREEN_WIDTH * 0.7), int(SCREEN_HEIGHT * 0.35)
    box_rect = pygame.Rect(0, 0, box_width, box_height)  # Create rectangle for dialog box
    box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Center dialog box on screen

    pygame.draw.rect(screen, (230, 230, 230), box_rect, border_radius=10)  # Draw light gray dialog box background
    pygame.draw.rect(screen, (40, 40, 40), box_rect, width=3, border_radius=10)  # Draw dark border around dialog

    font_title = pygame.font.SysFont("Arial", 30)  # Create font for confirmation question
    text_surface = font_title.render("Do you want to close the game?", True, BLACK)  # Render question text
    text_rect = text_surface.get_rect(center=(box_rect.centerx, box_rect.top + box_height * 0.3))  # Position question
    screen.blit(text_surface, text_rect)  # Draw question text to screen

    font_btn = pygame.font.SysFont("Arial", 28)  # Create font for button labels
    btn_w, btn_h, gap = 140, 50, 40  # Button dimensions and gap between buttons
    yes_rect = pygame.Rect(0, 0, btn_w, btn_h)  # Create Yes button rectangle
    no_rect = pygame.Rect(0, 0, btn_w, btn_h)  # Create No button rectangle
    yes_rect.center = (box_rect.centerx - (btn_w // 2 + gap), box_rect.top + int(box_height * 0.65))  # Position Yes button left
    no_rect.center = (box_rect.centerx + (btn_w // 2 + gap), box_rect.top + int(box_height * 0.65))  # Position No button right

    yes_color = (180, 220, 180) if selected_button == 0 else (210, 210, 210)  # Green if selected, gray otherwise
    no_color = (180, 220, 180) if selected_button == 1 else (210, 210, 210) 
    
    # Draw button backgrounds with selection highlighting
    pygame.draw.rect(screen, yes_color, yes_rect, border_radius=8)  # Yes button background
    pygame.draw.rect(screen, no_color, no_rect, border_radius=8)  # No button background
    
    # Draw button borders
    pygame.draw.rect(screen, (40, 40, 40), yes_rect, width=2, border_radius=8)  # Yes button border
    pygame.draw.rect(screen, (40, 40, 40), no_rect, width=2, border_radius=8)  # No button border

    yes_label = font_btn.render("Yes", True, (20, 20, 20))  # Render "Yes" label
    no_label = font_btn.render("No", True, (20, 20, 20))  # Render "No" label
    
    # Draw button labels centered on their respective buttons
    screen.blit(yes_label, yes_label.get_rect(center=yes_rect.center))  # Draw Yes label
    screen.blit(no_label, no_label.get_rect(center=no_rect.center))  # Draw No label
