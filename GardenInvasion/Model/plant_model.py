import pygame
from pathlib import Path
from ..Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .setting_volume_model import SettingsModel 

class Player(pygame.sprite.Sprite): 
    def __init__(self, pos:tuple, settings_model: SettingsModel=None):
        super().__init__() 
        
        # Determine which sprite to load
        if settings_model:
            # Import here to avoid circular dependency
            from ..Model.skin_selection_model import SkinSelectionModel
            skin_model = SkinSelectionModel()
            selected_skin = skin_model.get_skin_by_id(settings_model.player_skin) # get selected skin
            sprite_path = Path(selected_skin.sprite_path) # get path to the sprite
        else:
            # Default fallback
            pkg_root = Path(__file__).resolve().parent.parent
            sprite_path = pkg_root / "Assets" / "images" / "BasePlant01.png"
        
        try: # load and scale the image
            original_image = pygame.image.load(str(sprite_path)).convert_alpha()
            self.scale_factor = 0.15
            new_size = (
                max(1, int(original_image.get_width() * self.scale_factor)),
                max(1, int(original_image.get_height() * self.scale_factor))
            )
            self.image = pygame.transform.smoothscale(original_image, new_size)
        except (pygame.error, FileNotFoundError):
            # Create placeholder if image doesn't exist
            self.image = pygame.Surface((50, 50))
            self.image.fill((100, 200, 100))
        
        self.rect = self.image.get_rect(midbottom=pos)
        
        # get original image of the plant and change its size keeping the aspect ratio
        self.speed = 5 # movement speed

        self.shoot_SecondTime = 500  # 0.5 seconds
        self.last_shot = pygame.time.get_ticks()# track time of last shot
        
        # NEW: Life points system (2 life points)
        self.life_points = 2  # Start with 2 life points
        self.max_life_points = 2

    def move_left(self): # move left
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0 # prevent moving out of screen on the left side

    def move_right(self): # move right
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH # prevent moving out of screen on the right side

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_SecondTime:
            self.last_shot = current_time
            return True
        return False
    
    # NEW: Damage handling method
    def take_damage(self):
        """Reduce life points by 1 when hit.
        Returns True if plant is destroyed, False otherwise."""
        if self.life_points > 0:  # Only reduce if still alive
            self.life_points -= 1
        
        # You can add visual/sound feedback here later
        if self.life_points <= 0:
            return True  # Plant destroyed
        return False  # Plant still alive
    
    # NEW: Check if plant is alive
    def is_alive(self):
        """Check if plant still has life points"""
        return self.life_points > 0
