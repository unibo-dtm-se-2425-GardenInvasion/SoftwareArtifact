import pygame

def draw_wallnuts(screen: pygame.Surface, wallnut_group: pygame.sprite.Group):
    # Draws all wall-nuts on the screen.
    wallnut_group.draw(screen)

def draw_game(screen: pygame.Surface, 
              game_background, 
              player_group: pygame.sprite.Group, 
              projectile_group: pygame.sprite.Group,
              wallnut_group: pygame.sprite.Group,
              zombie_group=None):  # NUOVO PARAMETRO: zombie_group
    # Draw background
    if game_background.surface:
        screen.fill((0, 0, 0))
        screen.blit(game_background.surface, game_background.rect) # draw background image for game
    else:
        screen.fill((0, 0, 0))  # Fallback to black
    
    # Draw wall-nuts (behind player for visual layering)
    draw_wallnuts(screen, wallnut_group)
    
    # NUOVO: Draw zombies if provided (behind player, above wallnuts)
    if zombie_group:
        zombie_group.draw(screen)
    
    # Draw player
    player_group.draw(screen)
    # Draw projectiles
    projectile_group.draw(screen)