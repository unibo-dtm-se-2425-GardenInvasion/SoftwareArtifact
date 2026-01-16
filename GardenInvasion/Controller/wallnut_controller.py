import pygame
from ..Model.wallnut_model import WallNutManager

def handle_wallnut_placement(keys, wallnut_manager: WallNutManager):
    # Keys 1-4 to place wall-nuts in slots 0-3
    if keys[pygame.K_1]:
        wallnut_manager.place_wallnut(0)
    elif keys[pygame.K_2]:
        wallnut_manager.place_wallnut(1)
    elif keys[pygame.K_3]:
        wallnut_manager.place_wallnut(2)
    elif keys[pygame.K_4]:
        wallnut_manager.place_wallnut(3)


def handle_wallnut_collisions(wallnut_manager: WallNutManager, 
                               player_projectiles: pygame.sprite.Group):
    # Block player projectiles (they can't pass through wall-nuts)
    wallnut_manager.check_projectile_collision(player_projectiles)
