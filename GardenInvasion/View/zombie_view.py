def draw_zombie(screen, zombie):
    # Draw a single zombie sprite
    screen.blit(zombie.image, zombie.rect)


def draw_zombies(screen, zombie_group):
    # Draw all zombies in a sprite group
    for zombie in zombie_group:
        draw_zombie(screen, zombie)
