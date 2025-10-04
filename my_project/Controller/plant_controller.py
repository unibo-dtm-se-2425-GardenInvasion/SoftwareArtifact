import pygame
from ..Model.projectile_model import Projectile

def handle_player_input(player, projectile_group):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right()
    # move the plant left or right based on key press
    for event in pygame.event.get(pygame.KEYDOWN):
        if event.key == pygame.K_SPACE: # spacebar is trigger event
            # Shoot projectile from center top of player
            projectile = Projectile(player.rect.midtop)
            projectile_group.add(projectile)
    