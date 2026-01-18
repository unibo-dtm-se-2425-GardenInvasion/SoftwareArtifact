import pygame
from ..Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_game_over_screen(screen: pygame.Surface, model, alpha: int = 255) -> tuple:
    # Draw the game over UI elements with optional fade-in effect
    
    # Calculate dialog box dimensions
    box_width, box_height = int(SCREEN_WIDTH * 0.7), int(SCREEN_HEIGHT * 0.4)
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Create a surface for the entire UI with alpha channel
    ui_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    # Draw dialog box background and border
    pygame.draw.rect(ui_surface, (230, 230, 230, alpha), box_rect, border_radius=10)  # Light gray
    pygame.draw.rect(ui_surface, (40, 40, 40, alpha), box_rect, width=3, border_radius=10)  # Dark border
    
    # Setup fonts
    font_title = pygame.font.SysFont('Arial', 36)
    font_btn = pygame.font.SysFont('Arial', 24)
    # Draw "GAME OVER" title
    title_surface = font_title.render("GAME OVER", True, (200, 50, 50))
    title_surface.set_alpha(alpha)
    title_rect = title_surface.get_rect(center=(box_rect.centerx, box_rect.top + int(box_height * 0.25)))
    ui_surface.blit(title_surface, title_rect)
    
    # Define button positions
    btn_w, btn_h = 140, 50
    buttons_y = box_rect.top + int(box_height * 0.65)
    button_spacing = 120
    
    # Create button rectangles
    restart_rect = pygame.Rect(0, 0, btn_w, btn_h)
    menu_rect = pygame.Rect(0, 0, btn_w, btn_h)
    restart_rect.center = (box_rect.centerx - button_spacing, buttons_y)
    menu_rect.center = (box_rect.centerx + button_spacing, buttons_y)
    
    # Button colors based on selection (with alpha)
    restart_color = (180, 220, 180, alpha) if model.selected_index == 0 else (210, 210, 210, alpha)
    menu_color = (180, 220, 180, alpha) if model.selected_index == 1 else (210, 210, 210, alpha)
    # Draw button backgrounds
    pygame.draw.rect(ui_surface, restart_color, restart_rect, border_radius=8)
    pygame.draw.rect(ui_surface, menu_color, menu_rect, border_radius=8)
    # Draw button borders
    pygame.draw.rect(ui_surface, (40, 40, 40, alpha), restart_rect, width=2, border_radius=8)
    pygame.draw.rect(ui_surface, (40, 40, 40, alpha), menu_rect, width=2, border_radius=8)
    # Draw button labels
    restart_label = font_btn.render("Start Again", True, (20, 20, 20))
    menu_label = font_btn.render("Main Menu", True, (20, 20, 20))
    restart_label.set_alpha(alpha)
    menu_label.set_alpha(alpha)
    
    ui_surface.blit(restart_label, restart_label.get_rect(center=restart_rect.center))
    ui_surface.blit(menu_label, menu_label.get_rect(center=menu_rect.center))
    
    # Blit the entire UI surface to screen
    screen.blit(ui_surface, (0, 0))
    
    return restart_rect, menu_rect
