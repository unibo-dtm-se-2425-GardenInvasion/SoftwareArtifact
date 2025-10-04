def draw_game(screen, game_background, player_group, projectile_group):
    # Draw background
    if game_background.surface:
        screen.fill((0, 0, 0))
        screen.blit(game_background.surface, game_background.rect)
    else:
        screen.fill((0, 0, 0))  # Fallback to black
    
    # Draw sprites
    player_group.draw(screen)
    projectile_group.draw(screen)
