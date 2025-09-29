import pygame
from ..Utilities.constants import *

def draw_menu(screen, model, background_surf, background_rect, fonts):
    # Draw the main menu screense n

    if background_surf:
        screen.fill((0, 0, 0))
        screen.blit(background_surf, background_rect)
    else:
        screen.fill((0, 0, 50))
    # fill screen with dark blue if no background 

    item_font, inst_font, title_font = fonts # unpack fonts tuple
    title_text = title_font.render("Garden Invasion", True, GREEN_SI)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.25))
    screen.blit(title_text, title_rect)
    # renders and draws title
    
    label_rects = []  # Collect rects for controller usage
    for idx, label in enumerate(model.menu_items):
        text_surf = item_font.render(label, True, GREEN_SI)
        rect = text_surf.get_rect(center=(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.4 + idx*SCREEN_HEIGHT*0.1))
        label_rects.append(rect)   # Save rect for hit detection
        screen.blit(text_surf, rect)
        if idx == model.selected_index:
            draw_selection_arrows(screen, rect, color=GREEN_SI) 
            # if this item is selected, draw arrows around it
    # renders and draws menu items, with arrows around selected item
    inst_text = inst_font.render("Press ESC or close window to exit", True, WHITE_Instruction)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.65))
    screen.blit(inst_text, inst_rect)
    # renders and draws instructions text

    pygame.display.flip() # Update the full display Surface to the screen
    return label_rects  # Return rects to controller to test hover/click


def draw_selection_arrows(screen, target_rect, color=(98, 222, 109)):
    left_x = target_rect.left - 30
    mid_y  = target_rect.centery
    left_arrow = [(left_x, mid_y), (left_x + 12, mid_y - 8), (left_x + 12, mid_y + 8)]
    pygame.draw.polygon(screen, color, left_arrow)
    right_x = target_rect.right + 30
    right_arrow = [(right_x, mid_y), (right_x - 12, mid_y - 8), (right_x - 12, mid_y + 8)]
    pygame.draw.polygon(screen, color, right_arrow)
    # Draws arrows to the left and right of the target rectangle


def draw_modal(screen, selected_button=1):
    # Draws a modal dialog box asking if the user wants to quit
    # selected_button: 0 for "Yes", 1 for "No"
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # semi-transparent black
    screen.blit(overlay, (0, 0)) 
    # create and draw semi-transparent overlay

    box_width, box_height = int(SCREEN_WIDTH * 0.7), int(SCREEN_HEIGHT * 0.35)
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    # Draw dialog box

    pygame.draw.rect(screen, (230, 230, 230), box_rect, border_radius=10) # light gray box
    pygame.draw.rect(screen, (40, 40, 40), box_rect, width=3, border_radius=10) # dark border

    font_title = pygame.font.SysFont("Arial", 30)
    text_surface = font_title.render("Do you want to close the game?", True, WHITE_Instruction)
    text_rect = text_surface.get_rect(center=(box_rect.centerx, box_rect.top + box_height * 0.3))
    screen.blit(text_surface, text_rect)
    # render of the confirmation text

    font_btn = pygame.font.SysFont("Arial", 28) # font for buttons
    btn_w, btn_h, gap = 140, 50, 40
    yes_rect = pygame.Rect(0, 0, btn_w, btn_h)
    no_rect = pygame.Rect(0, 0, btn_w, btn_h)
    yes_rect.center = (box_rect.centerx - (btn_w // 2 + gap), box_rect.top + int(box_height * 0.65))
    no_rect.center = (box_rect.centerx + (btn_w // 2 + gap), box_rect.top + int(box_height * 0.65))
    # creation of yes/no button rectangles

    yes_color = (180, 220, 180) if selected_button == 0 else (210, 210, 210)
    no_color = (180, 220, 180) if selected_button == 1 else (210, 210, 210)
    pygame.draw.rect(screen, yes_color, yes_rect, border_radius=8)
    pygame.draw.rect(screen, no_color, no_rect, border_radius=8)
    pygame.draw.rect(screen, (40, 40, 40), yes_rect, width=2, border_radius=8)
    pygame.draw.rect(screen, (40, 40, 40), no_rect, width=2, border_radius=8)
    # draw yes/no buttons with highlighting for selected

    yes_label = font_btn.render("Yes", True, (20, 20, 20))
    no_label = font_btn.render("No", True, (20, 20, 20))
    # render button labels
    screen.blit(yes_label, yes_label.get_rect(center=yes_rect.center))
    screen.blit(no_label, no_label.get_rect(center=no_rect.center))
    # draw button labels