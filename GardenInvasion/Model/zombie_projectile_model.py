import pygame
from pathlib import Path
from ..Utilities.constants import SCREEN_HEIGHT

class ZombieProjectile(pygame.sprite.Sprite):
    # projectile launched by zombies 02
    
    def __init__(self, pos):
        super().__init__()
        self._load_sprite()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 5

    def _load_sprite(self):
        # Load zombie projectile sprite
        pkg_root = Path(__file__).resolve().parent.parent
        sprite_file = pkg_root / "Assets" / "images" / "zombie_projectile.png"
        
        try:
            # Load and scale sprite
            original_image = pygame.image.load(str(sprite_file)).convert_alpha()
            # Get original dimensions to preserve aspect ratio
            original_width, original_height = original_image.get_size()
            
            # Define target size maintaining aspect ratio
            target_height = 40
            aspect_ratio = original_width / original_height
            target_width = int(target_height * aspect_ratio)
            
            # Use rotozoom for best quality
            scale_factor = target_height / original_height
            self.image = pygame.transform.rotozoom(original_image, 0, scale_factor)
            
            print(f"Projectile sprite loaded")
                        
        except (pygame.error, FileNotFoundError):
            # Fallback to colored surface
            print(f"Warning: Could not load sprite {sprite_file}, using yellow rectangle")
            self.image = pygame.Surface((20, 30))
            self.image.fill((255, 255, 0))

    def update(self):
        # Update projectile position
        self.rect.y += self.speed
        
        # Rimuovi se esce dallo schermo in basso
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            