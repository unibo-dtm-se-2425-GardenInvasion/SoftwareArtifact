def draw_zombie_projectile(screen, projectile):
    # Draw a single zombie projectile sprite
    screen.blit(projectile.image, projectile.rect)


def draw_zombie_projectiles(screen, projectile_group):
    # Draw all zombie projectiles in a sprite group
    for projectile in projectile_group:
        draw_zombie_projectile(screen, projectile)
