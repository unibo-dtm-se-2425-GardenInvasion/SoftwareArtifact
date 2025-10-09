import pygame
from ..Model.projectile_model import Projectile

def handle_player_input(player, projectile_group):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right()
    # move the plant left or right based on key press

    if player.can_shoot(): # check if the player can shoot based on cooldown
        projectile = Projectile(player.rect.midtop) # create a new projectile at the top center of the player
        projectile_group.add(projectile) # add the new projectile to the group
    