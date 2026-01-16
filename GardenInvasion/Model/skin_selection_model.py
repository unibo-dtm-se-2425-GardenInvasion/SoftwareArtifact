import pygame
from pathlib import Path
from typing import List, Dict


class SkinOption:
    def __init__(self, skin_id: str, display_name: str, sprite_path: str, preview_path: str = None):
        self.skin_id = skin_id # used as key in settings file
        self.display_name = display_name # shown in selection menu
        self.sprite_path = sprite_path # path to full sprite image
        self.preview_path = preview_path if preview_path else sprite_path # path to preview image
        
        # Load preview image for selection menu
        try:
            self.preview_image = pygame.image.load(sprite_path).convert_alpha()
            # Scale preview to consistent size
            self.preview_image = pygame.transform.smoothscale(self.preview_image, (80, 80))
        except pygame.error:
            # Create placeholder if image doesn't exist
            self.preview_image = pygame.Surface((80, 80))
            self.preview_image.fill((100, 200, 100))  # Green placeholder


class SkinSelectionModel:
    def __init__(self):
        self.available_skins: List[SkinOption] = [] # List of available skins
        self.selected_index = 0  # Index of currently selected skin
        self.current_skin_id = "default"  # ID of active skin
        self.back_button_selected = False  #Track if Back button is selected
        # Initialize available skins
        self._load_available_skins()
    
    def _load_available_skins(self):
        # Load all available player skins.
        
        pkg_root = Path(__file__).resolve().parent.parent
        assets_path = pkg_root / "Assets" / "images"
        # Define available skins (expand this list as you add more skins)
        self.available_skins = [
            SkinOption(
                skin_id="default",
                display_name="Classic Plant",
                sprite_path=str(assets_path / "BasePlant01.png")
            ),
            SkinOption(
                skin_id="Carnivorous",
                display_name="Carnivorous Plant",
                sprite_path=str(assets_path / "BasePlant02.png")
            ),
            SkinOption(
                skin_id="Cactus",
                display_name="Cactus Plant",
                sprite_path=str(assets_path / "BasePlant03.png")
            )
        ]
    
    def get_selected_skin(self) -> SkinOption:
        # Returns the currently selected skin option.
        return self.available_skins[self.selected_index]
    
    def get_skin_by_id(self, skin_id: str) -> SkinOption:
        # Get a specific skin by its ID.
        for skin in self.available_skins:
            if skin.skin_id == skin_id:
                return skin
        return self.available_skins[0]  # Return default if not found
    
    def select_next_skin(self):
        # Move selection to next skin
        if not self.back_button_selected: # Only change skin if not on Back button
            self.selected_index = (self.selected_index + 1) % len(self.available_skins)
            self.current_skin_id = self.available_skins[self.selected_index].skin_id
    
    def select_previous_skin(self):
        # Move selection to previous skin
        if not self.back_button_selected: # Only change skin if not on Back button
            self.selected_index = (self.selected_index - 1) % len(self.available_skins)
            self.current_skin_id = self.available_skins[self.selected_index].skin_id
    
    def select_back_button(self):
        self.back_button_selected = True
    
    def deselect_back_button(self):
        self.back_button_selected = False
    
    def set_skin_by_id(self, skin_id: str):
        # Set the current skin by its ID.
        for i, skin in enumerate(self.available_skins): # Iterate to find skin
            if skin.skin_id == skin_id:
                self.selected_index = i
                self.current_skin_id = skin_id
                return True # Successfully set skin
        return False  # Skin ID not found
    
    def get_total_skins(self) -> int:
        # Returns total number of available skins.
        return len(self.available_skins)
