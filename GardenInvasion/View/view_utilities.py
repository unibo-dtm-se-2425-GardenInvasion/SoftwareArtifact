import pygame
from ..Utilities.constants import BLACK, GREEN_SI

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

def draw_selection_arrows(screen, target_rect, color=GREEN_SI):
    # Draw left and right arrows around a selected menu item.
    left_x = target_rect.left - 30
    mid_y = target_rect.centery
    left_arrow = [(left_x, mid_y), (left_x + 12, mid_y - 8), (left_x + 12, mid_y + 8)]
    pygame.draw.polygon(screen, color, left_arrow)

    right_x = target_rect.right + 30
    right_arrow = [(right_x, mid_y), (right_x - 12, mid_y - 8), (right_x - 12, mid_y + 8)]
    pygame.draw.polygon(screen, color, right_arrow)
