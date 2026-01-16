import pygame
from ..Utilities.constants import *

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


def draw_options_menu(screen, model, background_surf, background_rect, fonts):
    if background_surf:
        screen.fill((0, 0, 0))  # Fills screen with black before drawing background
        screen.blit(background_surf, background_rect)  # Draws custom background
    else:
        screen.fill((0, 0, 50))  # Fills with a default dark blue otherwise

    item_font, inst_font, title_font = fonts  # Unpacks tuple of fonts

    # Create smaller font used for options menu items
    options_font = pygame.font.SysFont("Arial", 20)
    # Draws the "Options" header at the top of the menu
    title_text = render_text_with_outline(title_font, "Options", GREEN_SI, BLACK, 3) # Renders title text
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.25)) # Centers title
    screen.blit(title_text, title_rect)

    # Rendering each menu option (Volume, Contact Us, Back)
    label_rects = []
    for idx, label in enumerate(model.options_items):
        text_surf = render_text_with_outline(options_font, label, GREEN_SI, BLACK, 2)  # Renders menu item text
        rect = text_surf.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.35 + idx * SCREEN_HEIGHT * 0.08))
        # Positions each option vertically
        label_rects.append(rect)  # Appends this option's placement for later reference
        screen.blit(text_surf, rect)  # Draws the option text to the screen

        # If current index is selected, draw arrows around it
        if idx == model.selected_index:
            draw_selection_arrows(screen, rect, color=GREEN_SI)

    # Displays control instructions near the bottom
    inst_text = render_text_with_outline(inst_font, "Press ESC or close window to exit", WHITE_Instruction, BLACK, 1)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65))
    screen.blit(inst_text, inst_rect)
    return label_rects

def draw_volume_menu(screen, volume_model, background_surf, background_rect, fonts):
    
    if background_surf:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(background_surf, background_rect)  # Draws background image
    else:
        screen.fill((0, 0, 50))  # Fallback blue background

    item_font, inst_font, title_font = fonts  # Uses given fonts

    # Volume menu title
    title_text = render_text_with_outline(title_font, "Volume", GREEN_SI, BLACK, 3)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.25))
    screen.blit(title_text, title_rect)

    # Current volume percentage, displayed below title
    percentage_font = pygame.font.SysFont("Arial", 28)
    volume_text = render_text_with_outline(percentage_font, f"{volume_model.volume}%", GREEN_SI, BLACK, 2)
    volume_rect = volume_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.38))
    screen.blit(volume_text, volume_rect)

    # Coordinates and dimensions for slider (visual bar)
    slider_width = 250
    slider_height = 16
    slider_x = SCREEN_WIDTH * 0.5 - slider_width // 2
    slider_y = SCREEN_HEIGHT * 0.44

    # Draws the filled slider background
    pygame.draw.rect(screen, (50, 50, 50), (slider_x, slider_y, slider_width, slider_height), border_radius=5)

    # Draws volume-proportional fill
    filled_width = int((volume_model.volume / 100) * slider_width)
    pygame.draw.rect(screen, GREEN_SI, (slider_x, slider_y, filled_width, slider_height), border_radius=5)

    # Slider border for clarity
    pygame.draw.rect(screen, WHITE_Instruction, (slider_x, slider_y, slider_width, slider_height), width=2, border_radius=5)

    # Directions beneath the slider for adjusting volume
    adjust_font = pygame.font.SysFont("Arial", 16)
    adjust_text = render_text_with_outline(adjust_font, "Use LEFT/RIGHT arrows to adjust volume", WHITE_Instruction, BLACK, 1)
    adjust_rect = adjust_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.52))
    screen.blit(adjust_text, adjust_rect)

    # Draws the back button below the slider
    back_font = pygame.font.SysFont("Arial", 18)
    back_text = render_text_with_outline(back_font, "Back", GREEN_SI, BLACK, 2)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.585))
    screen.blit(back_text, back_rect)

    draw_selection_arrows(screen, back_rect, color=GREEN_SI)

    # Instructions at the very bottom
    inst_text = render_text_with_outline(inst_font, "Press ESC or close window to exit", WHITE_Instruction, BLACK, 1)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65))
    screen.blit(inst_text, inst_rect)

    return back_rect  # Used by controller to detect user clicks

def draw_selection_arrows(screen, target_rect, color=(98, 222, 109)):
    left_x = target_rect.left - 30 # Positions left arrow to the left of target
    mid_y = target_rect.centery
    left_arrow = [(left_x, mid_y), (left_x + 12, mid_y - 8), (left_x + 12, mid_y + 8)]
    pygame.draw.polygon(screen, color, left_arrow)  # Draws left-pointing arrow

    right_x = target_rect.right + 30 # Positions right arrow to the right of target
    right_arrow = [(right_x, mid_y), (right_x - 12, mid_y - 8), (right_x - 12, mid_y + 8)]
    pygame.draw.polygon(screen, color, right_arrow)  # Draws right-pointing arrow

def draw_contact_modal(screen, selected_button=0):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  # Creates transparent overlay
    overlay.fill((0, 0, 0, 150))  # Applies semi-transparent black overlay
    screen.blit(overlay, (0, 0))  # Covers screen to force focus

    box_width, box_height = int(SCREEN_WIDTH * 0.6), int(SCREEN_HEIGHT * 0.4)
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Centers the dialog box

    # Draws modal box and border
    pygame.draw.rect(screen, (230, 230, 230), box_rect, border_radius=10)
    pygame.draw.rect(screen, (40, 40, 40), box_rect, width=3, border_radius=10)

    # Modal title
    font_title = pygame.font.SysFont("Arial", 24)
    text_surface = font_title.render("Contact Us", True, (40, 40, 40))
    text_rect = text_surface.get_rect(center=(box_rect.centerx, box_rect.top + box_height * 0.15))
    screen.blit(text_surface, text_rect)

    # Displayed email address
    font_info = pygame.font.SysFont("Arial", 18)
    email_surface = font_info.render("Email: GardenInvasion@email.com", True, (40, 40, 40))
    email_rect = email_surface.get_rect(center=(box_rect.centerx, box_rect.top + box_height * 0.35))
    screen.blit(email_surface, email_rect)

    # Confirmation prompt
    question_surface = font_info.render("Open your default email client?", True, (60, 60, 60))
    question_rect = question_surface.get_rect(center=(box_rect.centerx, box_rect.top + box_height * 0.55))
    screen.blit(question_surface, question_rect)

    # Two modal buttons ("Open Email", "Cancel")
    font_btn = pygame.font.SysFont("Arial", 20)
    btn_w, btn_h = 120, 45
    open_rect = pygame.Rect(0, 0, btn_w, btn_h)
    cancel_rect = pygame.Rect(0, 0, btn_w, btn_h)

    buttons_y = box_rect.top + int(box_height * 0.78)  # Vertically positions buttons below text

    open_rect.center = (box_rect.centerx - 80, buttons_y)    # "Open Email" button to the left
    cancel_rect.center = (box_rect.centerx + 80, buttons_y)  # "Cancel" button to the right

    open_color = (100, 200, 100) if selected_button == 0 else (180, 180, 180)    # Highlight if chosen
    cancel_color = (100, 200, 100) if selected_button == 1 else (180, 180, 180)  # Highlight if chosen

    # Draws the button rectangles and outlines
    pygame.draw.rect(screen, open_color, open_rect, border_radius=8)
    pygame.draw.rect(screen, cancel_color, cancel_rect, border_radius=8)
    pygame.draw.rect(screen, (40, 40, 40), open_rect, width=2, border_radius=8)
    pygame.draw.rect(screen, (40, 40, 40), cancel_rect, width=2, border_radius=8)

    # Button text labels
    open_label = font_btn.render("Open Email", True, (20, 20, 20))
    cancel_label = font_btn.render("Back", True, (20, 20, 20))
    screen.blit(open_label, open_label.get_rect(center=open_rect.center))
    screen.blit(cancel_label, cancel_label.get_rect(center=cancel_rect.center))

    # Return both button rects so the controller can handle mouse hover/click detection
    return open_rect, cancel_rect