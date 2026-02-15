import pygame
from ..Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_victory_screen(screen: pygame.Surface, victory_model, fade_alpha: int = 255):
    
    box_width = int(SCREEN_WIDTH * 0.90)
    box_height = int(SCREEN_HEIGHT * 0.6)
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Create semi-transparent surface for fade effect
    victory_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    
    # Draw dialog box with rounded corners
    pygame.draw.rect(victory_surface, (50, 150, 50, min(230, fade_alpha)), 
                     victory_surface.get_rect(), border_radius=20)
    pygame.draw.rect(victory_surface, (100, 255, 100, fade_alpha), 
                     victory_surface.get_rect(), width=5, border_radius=20)
    
    try:
        title_font = pygame.font.Font(None, 80)
        subtitle_font = pygame.font.Font(None, 40)
        button_font = pygame.font.Font(None, 30)
    except:
        title_font = pygame.font.SysFont('arial', 80, bold=True)
        subtitle_font = pygame.font.SysFont('arial', 40)
        button_font = pygame.font.SysFont('arial', 30, bold=True)
    
    title_text = title_font.render("VICTORY!", True, (255, 255, 100))
    title_text.set_alpha(fade_alpha)
    title_rect = title_text.get_rect(center=(box_width // 2, int(box_height * 0.25)))
    victory_surface.blit(title_text, title_rect)
    
    subtitle_text = subtitle_font.render("You survived the invasion!", True, (255, 255, 255))
    subtitle_text.set_alpha(fade_alpha)
    subtitle_rect = subtitle_text.get_rect(center=(box_width // 2, int(box_height * 0.45)))
    victory_surface.blit(subtitle_text, subtitle_rect)
    
    # Draw buttons
    buttons_y = int(box_height * 0.7)
    button_spacing = 200
    
    play_again_rect = pygame.Rect(0, 0, 180, 60)
    play_again_rect.center = (box_width // 2 - button_spacing // 2, buttons_y)
    
    menu_rect = pygame.Rect(0, 0, 180, 60)
    menu_rect.center = (box_width // 2 + button_spacing // 2, buttons_y)
    
    # Draw "Play Again" button
    if victory_model.selected_index == 0:
        pygame.draw.rect(victory_surface, (100, 255, 100, fade_alpha), play_again_rect, border_radius=10)
        play_again_color = (0, 100, 0)
    else:
        pygame.draw.rect(victory_surface, (70, 120, 70, fade_alpha), play_again_rect, border_radius=10)
        play_again_color = (200, 200, 200)
    
    pygame.draw.rect(victory_surface, (255, 255, 255, fade_alpha), play_again_rect, width=3, border_radius=10)
    
    play_again_text = button_font.render("Play Again", True, play_again_color)
    play_again_text.set_alpha(fade_alpha)
    play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)
    victory_surface.blit(play_again_text, play_again_text_rect)
    
    # Draw "Main Menu" button
    if victory_model.selected_index == 1:
        pygame.draw.rect(victory_surface, (100, 255, 100, fade_alpha), menu_rect, border_radius=10)
        menu_color = (0, 100, 0)
    else:
        pygame.draw.rect(victory_surface, (70, 120, 70, fade_alpha), menu_rect, border_radius=10)
        menu_color = (200, 200, 200)
    
    pygame.draw.rect(victory_surface, (255, 255, 255, fade_alpha), menu_rect, width=3, border_radius=10)
    
    menu_text = button_font.render("Main Menu", True, menu_color)
    menu_text.set_alpha(fade_alpha)
    menu_text_rect = menu_text.get_rect(center=menu_rect.center)
    victory_surface.blit(menu_text, menu_text_rect)
    
    screen.blit(victory_surface, box_rect.topleft)
    
    # Adjust button rects to screen coordinates for mouse interaction
    play_again_rect.topleft = (box_rect.left + play_again_rect.left, box_rect.top + play_again_rect.top)
    menu_rect.topleft = (box_rect.left + menu_rect.left, box_rect.top + menu_rect.top)
    
    return play_again_rect, menu_rect
