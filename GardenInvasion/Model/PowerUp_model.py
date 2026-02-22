import os
import pygame
import random
from .zombie_projectile_model import ZombieProjectile
from .wallnut_model import WallNutManager

_ZOMBIE_PROJECTILE_SIZE = None

def get_zombie_projectile_size(): # helper to get the size of zombie projectiles for scaling power-up images accordingly
    global _ZOMBIE_PROJECTILE_SIZE
    if _ZOMBIE_PROJECTILE_SIZE is not None:
        return _ZOMBIE_PROJECTILE_SIZE

    dummy = ZombieProjectile((0, 0))                 
    _ZOMBIE_PROJECTILE_SIZE = dummy.image.get_size() # get the size of the projectile image
    dummy.kill()
                    
    return _ZOMBIE_PROJECTILE_SIZE

class PowerUp(pygame.sprite.Sprite):
    # Base class for power-ups dropped in the game world.

    def __init__(self, pos, image: pygame.Surface, target_size=None):
        super().__init__()

        if target_size is not None:
            image = pygame.transform.smoothscale(image, target_size)

        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_y = 1.5  # slow falling speed

    def update(self):
        # Default behavior: slowly fall down the screen.
        self.rect.y += self.speed_y

    def apply(self, player) -> None:
        raise NotImplementedError # Each specific power-up will implement its own effect on the player.


class IncreasingFirePU(PowerUp):

    def __init__(self, pos, duration_ms: int = 5000, cooldown_multiplier: float = 0.6, target_size=None):
        img_path = os.path.join("GardenInvasion", "Assets", "images", "IncreaseFirePU.png")
        image = pygame.image.load(img_path).convert_alpha()
        super().__init__(pos, image, target_size=target_size)

        self.duration_ms = duration_ms
        self.cooldown_multiplier = cooldown_multiplier

    def apply(self, player) -> None:
        # Player is the plant (Player model)
        player.apply_fire_rate_boost(
            cooldown_multiplier=self.cooldown_multiplier,
            duration_ms=self.duration_ms
        )

class RepairWallnutPU(PowerUp):
    
    def __init__(self, pos, target_size=None):
        img_path = os.path.join("GardenInvasion", "Assets", "images", "RepairWallnutPU.png")
        image = pygame.image.load(img_path).convert_alpha()
        super().__init__(pos, image, target_size=target_size)

    def apply(self, wallnut_manager) -> None:
        wallnut_manager.repair_all_wallnuts()

class PowerUpManager:
    # Small helper to spawn and keep track of power-ups.

    def __init__(self):
        self.powerup_group = pygame.sprite.Group()
        self.target_size = get_zombie_projectile_size()

    def spawn_increasing_fire(self, pos):
        self.powerup_group.add(IncreasingFirePU(pos, target_size=self.target_size))

    def spawn_repair_wallnut(self, pos):
        self.powerup_group.add(RepairWallnutPU(pos, target_size=self.target_size))

    def spawn_random_powerup(self, pos): # Randomly decide which power-up to spawn at the given position
        if random.random() < 0.5:
            self.spawn_increasing_fire(pos)
        else:
            self.spawn_repair_wallnut(pos)

    def update(self):
        self.powerup_group.update()