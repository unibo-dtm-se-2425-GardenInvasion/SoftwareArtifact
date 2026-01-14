import pygame
from ..Utilities.constants import Brown, Lighter_Brown, Even_Lighter_Brown
from .sound_manager_model import SoundManager

class WallNut(pygame.sprite.Sprite): # Model for a defensive wall-nut that protects the player.
    def __init__(self, position: tuple, slot_index: int, sound_manager: SoundManager = None):
        super().__init__()
        self.slot_index = slot_index  # Which of the 4 wall-nut slots (0-3)
        self.health = 2  # CHANGED: Wall-nut now has 2 life points (was 3)
        self.max_health = 2  # CHANGED: Max health is now 2

        self.sound_manager = sound_manager  # Sound manager for playing sounds

        # Define wall-nut size (width, height)
        self.wallnut_size = (60, 60)
        
        try:
            # Load original sprites
            sprite_full=pygame.image.load(r"GardenInvasion/Assets/images/Wallnut_body_Undamaged.png").convert_alpha() # Full health
            sprite_dmg1=pygame.image.load(r"GardenInvasion/Assets/images/Wallnut_Body_cracked1.png").convert_alpha()  # 1 hit taken
            sprite_dmg2=pygame.image.load(r"GardenInvasion/Assets/images/Wallnut_body_cracked2.png").convert_alpha()  # 2 hits taken (will be unused)
            
            # Scale sprites to desired size above
            # CHANGED: Now only use 2 states (2 and 1 life points)
            self.sprites = {
                2: pygame.transform.smoothscale(sprite_full, self.wallnut_size),  # Full health (2 life points)
                1: pygame.transform.smoothscale(sprite_dmg1, self.wallnut_size),  # Damaged (1 life point)
                # Note: sprite_dmg2 is unused now since we only have 2 life points
            }
        except pygame.error as e:
            print(f"Error loading wallnut sprites: {e}")
            # Create placeholder colored rectangles if images don't exist
            self.sprites = {
                2: self._create_placeholder(self.wallnut_size, Brown),
                1: self._create_placeholder(self.wallnut_size, Lighter_Brown),
                # No need for Even_Lighter_Brown since we only have 2 states
            }
        
        # Set initial sprite to full health
        self.image = self.sprites[self.health]
        self.rect = self.image.get_rect()
        self.rect.center = position  # Position of wall-nut
        
    def take_damage(self):
        # Reduces health by 1 and updates sprite.
        # Returns True if wall-nut is destroyed, False otherwise.
        if self.health > 0:  # Prevent negative health
            self.health -= 1  # Decrease health
        
        if self.health <= 0:
            if self.sound_manager:
                self.sound_manager.play_sound('wallnut_destroyed') # Play destruction sound
            
            self.kill()  # Remove from sprite groups
            return True  # Wall-nut destroyed
        else:
            self.image = self.sprites[self.health]  # Update sprite to show damage
            return False  # Wall-nut still standing
    
    # ... rest of the class remains the same ...

class WallNutManager:
    # ... this class remains unchanged except we should update the place_wallnut method
    # ... to pass the sound_manager if available
    
    def place_wallnut(self, slot_index: int, sound_manager: SoundManager = None) -> bool:
        # Place a wall-nut in the specified slot (0-3).
        # Returns True if placement successful, False if slot occupied.
        
        if slot_index < 0 or slot_index >= self.max_wallnuts:
            return False  # Invalid slot index
        
        if self.slot_occupied[slot_index]:
            return False  # Slot already has a wall-nut
        
        # Create new wall-nut at the slot position
        position = self.slot_positions[slot_index]
        new_wallnut = WallNut(position, slot_index, sound_manager)  # Pass sound_manager
        self.wallnuts.add(new_wallnut)
        self.slot_occupied[slot_index] = True
        return True
    
    # ... rest of WallNutManager remains the same ...
