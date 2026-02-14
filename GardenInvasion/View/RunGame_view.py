import pygame
from ..View.zombie_view import draw_zombies
from ..View.zombie_projectile_view import draw_zombie_projectiles

def draw_wallnuts(screen: pygame.Surface, wallnut_group: pygame.sprite.Group):
    # Draws all wall-nuts on the screen.
    wallnut_group.draw(screen)

def draw_hearts(screen: pygame.Surface, player_health: int, heart_image: pygame.Surface):
    # Heart positioning
    heart_size = 40  
    spacing = 10
    margin = 20

    # Calculate starting position (top right)
    start_x = screen.get_width() - margin - (heart_size * player_health) - (spacing * (player_health - 1))
    start_y = margin
    
    # Draw hearts
    for i in range(player_health):
        x_pos = start_x + (i * (heart_size + spacing))
        # Scale heart image if needed
        scaled_heart = pygame.transform.scale(heart_image, (heart_size, heart_size))
        screen.blit(scaled_heart, (x_pos, start_y))


def draw_game(screen: pygame.Surface, 
              game_background, 
              player_group: pygame.sprite.Group, 
              projectile_group: pygame.sprite.Group,
              wallnut_group: pygame.sprite.Group,
              player_health: int,
              heart_image: pygame.Surface,
              zombie_group=None,
              zombie_projectile_group=None):
    
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
        draw_zombies(screen, zombie_group)

    if zombie_projectile_group and len(zombie_projectile_group) > 0:
        # Draw a red circle around each projectile for testing
        for proj in zombie_projectile_group:
            # Draw the projectile itself
            screen.blit(proj.image, proj.rect)
            # ✅ NEW: Draw a red outline circle for visibility testing
            pygame.draw.circle(screen, (255, 0, 0), proj.rect.center, 20, 2)
    
    # Draw player
    player_group.draw(screen)
    # Draw projectiles
    projectile_group.draw(screen)
    # Draw hearts
    draw_hearts(screen, player_health, heart_image)