import pygame
from ..Model.skin_selection_model import SkinSelectionModel
from ..Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GREEN_SI, WHITE_Instruction, BLACK

def render_text_with_outline(font, text, color, outline_color=BLACK, outline_width=2):
    # Render text with a dark outline for better visibility on dark backgrounds.
    
    # Create outline surface
    outline_text = font.render(text, True, outline_color) # Renders outline text
    text_width = outline_text.get_width()
    text_height = outline_text.get_height()
    
    # Create a surface large enough for outline
    text_surface = pygame.Surface(
        (text_width + outline_width * 2, text_height + outline_width * 2),
        pygame.SRCALPHA
    )
    
    # Draw outline in all 8 directions
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0: # Skip center position
                text_surface.blit(outline_text, (dx + outline_width, dy + outline_width)) # Blit outline text
    
    # Draw main text on top
    main_text = font.render(text, True, color)
    text_surface.blit(main_text, (outline_width, outline_width))
    
    return text_surface


def draw_skin_selection_menu(screen: pygame.Surface,
                              skin_model: SkinSelectionModel,
                              background_surf,
                              background_rect,
                              fonts):

    title_font, item_font, inst_font = fonts
    if background_surf: # check the background image
        screen.fill((0, 0, 0))
        screen.blit(background_surf, background_rect)
    else:
        screen.fill((20, 20, 40))
    
    title_text = render_text_with_outline(title_font, "Skin Personalization", GREEN_SI, BLACK, 3)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.25))
    screen.blit(title_text, title_rect)

    # Skin preview and settings
    total_skins = skin_model.get_total_skins()
    spacing = SCREEN_WIDTH * 0.7 / (total_skins + 1)
    start_x = SCREEN_WIDTH * 0.15
    skin_y = SCREEN_HEIGHT * 0.42
    
    # loop through the skins and show the preview
    for i, skin in enumerate(skin_model.available_skins): 
        x = start_x + spacing * (i + 1)
        # Draw skin preview image
        preview_rect = skin.preview_image.get_rect(center=(x, skin_y))
        screen.blit(skin.preview_image, preview_rect)
        # Draw selection indicator if the skin is selected
        if i == skin_model.selected_index and not skin_model.back_button_selected:
            
            border_rect = preview_rect.inflate(20, 20) # Gold border around selected skin
            pygame.draw.rect(screen, (255, 215, 0), border_rect, 4)
            
            # Arrow above selected skin
            arrow_text = render_text_with_outline(title_font, "▼", (255, 215, 0), BLACK, 2)
            arrow_rect = arrow_text.get_rect(center=(x, skin_y - 70))
            screen.blit(arrow_text, arrow_rect)
        
        # Draw skin name below preview
        name_text = render_text_with_outline(item_font, skin.display_name, (255, 255, 255), BLACK, 1)
        name_rect = name_text.get_rect(center=(x, skin_y + 70))
        screen.blit(name_text, name_rect)
    
    back_font = pygame.font.SysFont("Arial", 18)
    back_text = render_text_with_outline(back_font, "Back", GREEN_SI, BLACK, 2)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.585))
    screen.blit(back_text, back_rect)
    
    # Draw selection arrows around Back button if selected
    if skin_model.back_button_selected:
        draw_selection_arrows(screen, back_rect, color=GREEN_SI)
    
    inst_text = render_text_with_outline(item_font, "Press ESC or close window to exit", WHITE_Instruction, BLACK, 1)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65))
    screen.blit(inst_text, inst_rect)
    
    return back_rect


def draw_selection_arrows(screen, target_rect, color=GREEN_SI):
    # Draw left and right arrows around a selected menu item.
    left_x = target_rect.left - 30
    mid_y = target_rect.centery
    left_arrow = [(left_x, mid_y), (left_x + 12, mid_y - 8), (left_x + 12, mid_y + 8)]
    pygame.draw.polygon(screen, color, left_arrow)
    
    right_x = target_rect.right + 30
    right_arrow = [(right_x, mid_y), (right_x - 12, mid_y - 8), (right_x - 12, mid_y + 8)]
    pygame.draw.polygon(screen, color, right_arrow)
