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
    
class WallNutManager:
    # Manages the 4 wall-nut slots in front of the player.
    # Handles placement, removal, and collision detection.
    def __init__(self, player_position: tuple, screen_width: int, screen_height: int, sound_manager: SoundManager = None):
        self.player_position = player_position  # Player's position
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.sound_manager = sound_manager  # Sound manager for playing sounds

        self.wallnuts = pygame.sprite.Group()  # Group containing all active wall-nuts
        self.max_wallnuts = 4  # Maximum number of wall-nuts
        
        # Calculate positions for 4 wall-nut slots in front of player
        self.slot_positions = self._calculate_slot_positions()
        self.slot_occupied = [False] * self.max_wallnuts  # Track which slots are filled
    
    def _calculate_slot_positions(self):
        # Calculate the 4 positions where wall-nuts can be placed.
        player_x, player_y = self.player_position
        
        # Adjusted positioning values
        offset_y = -150  # Distance above player (negative = higher up)
        total_width = self.screen_width * 0.9  # Wall-nuts span % of screen width
        spacing = total_width / 3  # Space between wall-nuts
        # Starting x position (left side)
        start_x = player_x - (total_width / 2)
        
        positions = []
        # Create 4 positions: left, middle-left, middle-right, right
        for i in range(4):
            x = start_x + (i * spacing)
            y = player_y + offset_y
            positions.append((x, y))
        
        return positions
    
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
    
    def check_projectile_collision(self, projectile_group: pygame.sprite.Group):
        # Check if any player projectiles collide with wall-nuts.
        # Projectiles are blocked (removed) but wall-nuts are not damaged by friendly fire.
        
        collisions = pygame.sprite.groupcollide(
            projectile_group,  # Player's projectiles
            self.wallnuts,  # Wall-nuts
            True,  # Remove projectile on collision
            False  # Don't remove wall-nut (it blocks, not takes damage from player)
        )
        return collisions

    def update(self):
        # Update all wall-nuts.
        self.wallnuts.update()
    
    def get_wallnuts(self):
        # Returns the sprite group containing all wall-nuts for rendering.
        return self.wallnuts
    
    def place_all_wallnuts(self):
        # place wall-nuts in all 4 slots at game start.
        for i in range(self.max_wallnuts):
            print("Placing wallnut in slot", i)
            self.place_wallnut(i)