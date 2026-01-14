import pygame
from pathlib import Path
from ..Utilities.constants import *

def load_background_keep_ratio(image_path: Path):
    # Load an image and scale it to fit the screen while maintaining aspect ratio
    if not image_path.is_file():
        return None, None # Return None if the file does not exist
    image = pygame.image.load(str(image_path)) # Load the image
    iw, ih = image.get_size() # image width and height
    sw, sh = (SCREEN_WIDTH, SCREEN_HEIGHT)
    scale = min(sw / iw, sh / ih)
    new_size = (max(1, round(iw * scale)), max(1, round(ih * scale)))
    # Ensure dimensions are at least 1 pixel
    surf = pygame.transform.smoothscale(image, new_size) # Scale the image
    rect = surf.get_rect(center=(sw // 2, sh // 2))
    # Center the image on the screen
    return surf, rect # Return the scaled surface and its rect

class BackgroundModel:
    def __init__(self, image_path: Path): 
        self.surface, self.rect = load_background_keep_ratio(image_path)
        # when BackgroundModel is created, it loads the background image amnd its rect
        # using the function above
    # surface is None if loading failed

class MenuModel:
    def __init__(self):
        self.menu_items = ["New Game", "Options"]  # List of menu items
        self.selected_index = 0  # Index of currently selected menu item (starts at "New Game")
        
        # Modal-specific state for quit confirmation dialog
        self.modal_open = False  # Whether the modal is currently displayed
        self.modal_selected_button = 1  # Which modal button is selected (0: Yes, 1: No)
