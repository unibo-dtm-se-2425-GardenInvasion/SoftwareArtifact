import pygame
import sys
from pathlib import Path
from ..Model.menu_model import MenuModel, BackgroundModel
from ..View.menu_view import draw_pause_modal, get_pause_menu_button_rects
from ..Utilities.constants import*
from ..Model.plant_model import Player
from ..Model.wallnut_model import WallNutManager
from ..Model.wave_model import WaveManager
from .plant_controller import handle_player_input
from .wallnut_controller import handle_wallnut_placement
from ..View.RunGame_view import draw_game
from .menu_controller_utilities import show_confirm_quit
from ..Model.setting_volume_model import SettingsModel
from ..Model.sound_manager_model import SoundManager
from ..Model.game_over_model import GameOverModel
from ..View.game_over_view import draw_game_over_screen

# ---------- modal helper ----------
def show_pause_menu(screen: pygame.Surface, model: MenuModel) -> str:
    clock = pygame.time.Clock()
    background_copy = screen.copy()
    small_size = (screen.get_width() // 3, screen.get_height() // 3)
    blurred = pygame.transform.smoothscale(background_copy, small_size)
    blurred = pygame.transform.smoothscale(blurred, screen.get_size())
    # Reset to middle button (Resume) by default
    pause_selected = 1  # 0=Main Menu, 1=Resume, 2=Quit
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ("Quit event detected in pause menu, Bye Bye!")
                return 'quit' # Quit the game
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    pause_selected = (pause_selected - 1) % 3 # Left arrow or A pressed
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    pause_selected = (pause_selected + 1) % 3 # right arrow or D pressed
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if pause_selected == 0:
                        print("Enter/Space key detected, Returning to Main Menu from Pause Menu")
                        return 'menu'
                    elif pause_selected == 1:
                        print("Enter/Space key detected, Resuming Game from Pause Menu")
                        return 'resume'
                    else:
                        print("Enter/Space key detected, Quitting Game from Pause Menu, Bye Bye!")
                        return 'quit'
                elif event.key == pygame.K_ESCAPE:
                    print("Resuming Game from Pause Menu via ESC key")
                    return 'resume'  # ESC in pause menu = resume
                    
            if event.type == pygame.MOUSEMOTION:
                menu_rect, resume_rect, quit_rect = get_pause_menu_button_rects()# get button rects

                # Calculate dialog box position (matching draw_pause_modal positioning)
                box_width, box_height = int(SCREEN_WIDTH * 0.7), int(SCREEN_HEIGHT * 0.35)
                box_rect = pygame.Rect(0, 0, box_width, box_height)
                box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                
                # Position buttons relative to dialog box
                buttons_y = box_rect.top + int(box_height * 0.65)
                menu_rect.center = (box_rect.centerx - 160, buttons_y)
                resume_rect.center = (box_rect.centerx, buttons_y)
                quit_rect.center = (box_rect.centerx + 160, buttons_y)

                if menu_rect.collidepoint(event.pos):
                    pause_selected = 0
                elif resume_rect.collidepoint(event.pos):
                    pause_selected = 1
                elif quit_rect.collidepoint(event.pos):
                    pause_selected = 2
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_rect, resume_rect, quit_rect = get_pause_menu_button_rects()
                if pause_selected == 0:
                    print ("Returning to Main Menu from Pause Menu via Mouse Click")
                    return 'menu'
                elif pause_selected == 1:
                    print ("Resuming Game from Pause Menu via Mouse Click")
                    return 'resume'
                else:
                    print ("Quitting Game from Pause Menu via Mouse Click, Bye Bye!")
                    return 'quit'
        
        screen.blit(blurred, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        draw_pause_modal(screen, pause_selected)
        pygame.display.flip()
        clock.tick(60)

def show_game_over_screen(screen: pygame.Surface, menu_model: MenuModel, sound_manager: SoundManager) -> str:
    # Controller for game over screen with fade-in animation
    
    clock = pygame.time.Clock()
    game_over_model = GameOverModel()
    sound_manager.play_sound('game_over') 

    # Capture and blur the background ONCE before the loop
    background_snapshot = screen.copy() # Capture current screen
    small_size = (screen.get_width() // 8, screen.get_height() // 8) # Reduce size for blurring
    blurred_bg = pygame.transform.smoothscale(background_snapshot, small_size)
    blurred_bg = pygame.transform.smoothscale(blurred_bg, (screen.get_width() // 6, screen.get_height() // 6))
    blurred_bg = pygame.transform.smoothscale(blurred_bg, screen.get_size())
    
    # Store button rects (will be updated after first draw)
    restart_rect = None
    menu_rect = None
    
    # Fade-in animation variables
    fade_alpha = 0  # Start fully transparent
    fade_speed = 5  # Speed of fade (higher = faster)
    fade_complete = False

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
                
            # Only allow input after fade completes
            if fade_complete:
                if event.type == pygame.KEYDOWN: # Handle keyboard input
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        game_over_model.select_previous()
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        game_over_model.select_next()
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        selected = game_over_model.get_selected_option()
                        if selected == "Start Again":
                            print("Restarting game")
                            return 'restart'
                        else:
                            print("Returning to main menu")
                            return 'menu'
                            
                if event.type == pygame.MOUSEMOTION: # Handle mouse hover
                    if restart_rect and menu_rect:
                        if restart_rect.collidepoint(event.pos):
                            game_over_model.selected_index = 0
                        elif menu_rect.collidepoint(event.pos):
                            game_over_model.selected_index = 1
                        
                if event.type == pygame.MOUSEBUTTONDOWN: # Handle mouse clicks
                    selected = game_over_model.get_selected_option()
                    if selected == "Start Again":
                        return 'restart'
                    else:
                        return 'menu'
        
        # Draw blurred background first
        screen.blit(blurred_bg, (0, 0))
        # Draw dark overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Draw game over screen with current fade alpha
        restart_rect, menu_rect = draw_game_over_screen(screen, game_over_model, fade_alpha)
        
        # Update fade-in animation
        if fade_alpha < 255:
            fade_alpha = min(255, fade_alpha + fade_speed)
        else:
            fade_complete = True
        
        pygame.display.flip()
        clock.tick(60)

# ---------- COLLISION HELPERS ----------
# PUNTO 1: Plant projectile → Zombie
def _handle_projectile_zombie_collisions(projectile_group, zombie_group, sound_manager=None):
    # Handle collisions between player projectiles and zombies
    collisions = pygame.sprite.groupcollide(
        projectile_group,  # Player projectiles
        zombie_group,      # Zombies
        True,              # Remove projectile on hit
        False              # Don't remove zombie (it takes damage instead)
    )
    
    # For each collision, make the zombie take damage
    for projectile, zombies_hit in collisions.items():
        for zombie in zombies_hit:
            zombie_destroyed = zombie.take_damage(1)  # Deal 1 damage
            # 🔥 SUONO: Zombie hit sound
            if sound_manager:
                sound_manager.play_sound('zombie_hit')
    
    return len(collisions) > 0  # Return True if any collisions occurred

# PUNTO 2: Zombie projectile → Plant
def _handle_zombie_projectile_plant_collisions(zombie_projectile_group, player, sound_manager=None):
    # Handle collisions between zombie projectiles and plant

    # print(f"DEBUG: Zombie projectiles in group: {len(zombie_projectile_group)}")
    
    # Check collision between zombie projectiles and player
    collisions = pygame.sprite.spritecollide(
        player,                    # The plant/player sprite
        zombie_projectile_group,   # Zombie projectiles group
        True,                      # Remove zombie projectile on hit
        pygame.sprite.collide_rect # Use rectangle collision
    )
    
    # print(f"DEBUG: Collisions detected: {len(collisions)}")
    
    plant_was_destroyed = False
    
    # For each collision, make the plant take damage
    for projectile in collisions:
        print(f"DEBUG: Plant taking damage from zombie projectile!")
        
        # 🔥 SUONO: Plant hit by projectile
        if sound_manager:
            sound_manager.play_sound('plant_hit')
        
        plant_destroyed = player.take_damage()
        
        # print(f"DEBUG: Plant destroyed? {plant_destroyed}")
        
        # Check if plant was destroyed
        if plant_destroyed:
            print("💀 PLANT DESTROYED BY PROJECTILE! GAME OVER!")
            plant_was_destroyed = True
            # Break early since plant is already destroyed
            break
    
    # Return True only if plant was actually destroyed, not just hit
    return plant_was_destroyed

# PUNTO 3: Zombie projectile → Wallnut
def _handle_zombie_projectile_wallnut_collisions(zombie_projectile_group, wallnut_manager, sound_manager=None):
    # Handle collisions between zombie projectiles and wallnuts
    # Get the wallnut sprite group
    wallnut_group = wallnut_manager.get_wallnuts()
    
    # Check collisions between zombie projectiles and wallnuts
    collisions = pygame.sprite.groupcollide(
        zombie_projectile_group,  # Zombie projectiles
        wallnut_group,            # Wallnut sprites
        True,                     # Remove zombie projectile on hit
        False                     # Don't remove wallnut (it takes damage instead)
    )
    
    wallnut_destroyed_count = 0
    
    # For each collision, make the wallnut take damage
    for projectile, wallnuts_hit in collisions.items():
        for wallnut in wallnuts_hit:
            wallnut_destroyed = wallnut.take_damage()
            if wallnut_destroyed:
                wallnut_destroyed_count += 1
                print(f"💥 Wallnut {wallnut.slot_index} destroyed by zombie projectile!")
            else:
                print(f"💥 Wallnut {wallnut.slot_index} hit by zombie projectile! Health: {wallnut.health}")
    
    return len(collisions) > 0  # Return True if any collisions occurred

# PUNTO 4: Zombie → Wallnut
def _handle_zombie_wallnut_collisions(zombie_group, wallnut_manager, sound_manager=None):
    # Handle collisions between zombies and wallnuts
    # Zombie is destroyed on contact, wallnut takes damage
    
    wallnut_group = wallnut_manager.get_wallnuts()
    
    # Check collisions between zombies and wallnuts
    # True = remove zombie on collision (it gets destroyed)
    # False = don't auto-remove wallnut (it takes damage via take_damage())
    collisions = pygame.sprite.groupcollide(
        zombie_group,      # Zombies
        wallnut_group,     # Wallnut sprites
        True,              # REMOVE zombie on collision (destroyed)
        False              # DON'T auto-remove wallnut (it takes damage instead)
    )
    
    wallnut_destroyed_count = 0
    
    # For each collision, make the wallnut take damage
    for zombie, wallnuts_hit in collisions.items():
        for wallnut in wallnuts_hit:
            wallnut_destroyed = wallnut.take_damage()
            if wallnut_destroyed:
                wallnut_destroyed_count += 1
                print(f"Wallnut {wallnut.slot_index} destroyed by zombie!")
            else:
                print(f"Zombie destroyed by wallnut {wallnut.slot_index}! Wallnut health: {wallnut.health}")
    
    return len(collisions) > 0  # Return True if any collisions occurred

# PUNTO 5: Zombie → Plant
def _handle_zombie_plant_collisions(zombie_group, player, sound_manager=None):
    """Handle collisions between zombies and the plant.
    Zombie is destroyed on contact, plant takes damage."""
    
    print(f"\n🔍 DEBUG ZOMBIE-PLANT: ========== CHECKING COLLISION ==========")
    print(f"🔍 DEBUG ZOMBIE-PLANT: Checking {len(zombie_group)} zombies against plant at {player.rect.center}")
    print(f"🔍 DEBUG ZOMBIE-PLANT: Plant life: {player.life_points}/{player.max_life_points}")
    print(f"🔍 DEBUG ZOMBIE-PLANT: Plant rect: {player.rect}")
    
    # Check collisions between zombies and player
    # True = remove zombie on collision (it gets destroyed)
    collisions = pygame.sprite.spritecollide(
        player,              # The plant/player sprite
        zombie_group,        # Zombies group
        True,                # REMOVE zombie on collision (destroyed)
        pygame.sprite.collide_rect  # Use rectangle collision
    )
    
    print(f"🔍 DEBUG ZOMBIE-PLANT: Collisions detected: {len(collisions)}")
    
    if len(collisions) > 0:
        for i, zombie in enumerate(collisions):
            print(f"🔍 DEBUG ZOMBIE-PLANT: Zombie {i+1} rect: {zombie.rect}")
    
    plant_was_destroyed = False
    
    # For each collision, make the plant take damage
    for zombie in collisions:
        print(f"💥 Zombie hits plant! Plant life before: {player.life_points}")
        
        # 🔥 SUONO: Plant hit by zombie
        if sound_manager:
            sound_manager.play_sound('plant_hit')
        
        plant_destroyed = player.take_damage()
        print(f"💥 Plant life after: {player.life_points}")
        
        if plant_destroyed:
            print("💀 PLANT DESTROYED BY ZOMBIE! GAME OVER!")
            plant_was_destroyed = True
        else:
            print(f"🌱 Plant health: {player.life_points}/{player.max_life_points}")
    
    print(f"🔍 DEBUG ZOMBIE-PLANT: ========== END CHECK ==========\n")
    return plant_was_destroyed  # Return True if plant was destroyed

# ---------- game + options scenes ----------
def run_game(screen: pygame.Surface, model: MenuModel, settings_model: SettingsModel, sound_manager: SoundManager) -> None:
    #placeholder for actual game loop until the user quits

    clock = pygame.time.Clock()

    pkg_root = Path(__file__).resolve().parent.parent
    RunGame_bg_path = pkg_root / "Assets" / "images" / "RunGame01.png"
    RunGame_background = BackgroundModel(RunGame_bg_path)

    heart_path = pkg_root / "Assets" / "images" / "HeartShape.png"
    try:
        heart_image = pygame.image.load(heart_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading heart image: {e}")
        # Create a fallback red heart rectangle if image not found
        heart_image = pygame.Surface((40, 40))
        heart_image.fill((255, 0, 0))

    sound_manager = SoundManager(settings_model)

    # Create player with selected skin
    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.95), settings_model)
    player_group = pygame.sprite.GroupSingle(player)
    projectile_group = pygame.sprite.Group()

    # create wall-nut manager with 4 wall-nut slots
    wallnut_manager = WallNutManager(
        player_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.95),
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        sound_manager=sound_manager
    )

    wallnut_manager.place_all_wallnuts()
    
    # Create wave manager
    wave_manager = WaveManager()
    wave_manager.start_first_wave()
    
    sound_manager.play_music('gameplay', loops=-1, fade_ms=1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ("Quit event detected in game loop")
                if show_confirm_quit(screen, model):
                    sound_manager.stop_music(fade_ms=500)
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Escape key pressed, Pause Menu shown")
                sound_manager.pause_music()
                action = show_pause_menu(screen, model)
                if action == 'quit':
                    sound_manager.stop_music(fade_ms=500)
                    pygame.quit()
                    sys.exit()
                elif action == 'menu':
                    sound_manager.stop_music(fade_ms=1000)
                    running = False
                else:
                    sound_manager.unpause_music()
        
        handle_player_input(player, projectile_group, sound_manager)
        keys = pygame.key.get_pressed()
        handle_wallnut_placement(keys, wallnut_manager)

        # Update all entities
        player_group.update()
        projectile_group.update()
        wallnut_manager.update()
        wave_manager.update()
        
        # ---------- HANDLE ALL COLLISIONS ----------
        
        # PUNTO 1: Player projectiles → zombies
        _handle_projectile_zombie_collisions(projectile_group, wave_manager.zombie_group, sound_manager)
        
        # PUNTO 2: Zombie projectiles → plant
        plant_destroyed_by_projectile = _handle_zombie_projectile_plant_collisions(
            wave_manager.zombie_projectile_group, 
            player, 
            sound_manager
        )
        
        # PUNTO 3: Zombie projectiles → wallnuts
        _handle_zombie_projectile_wallnut_collisions(
            wave_manager.zombie_projectile_group,
            wallnut_manager,
            sound_manager
        )
        
        # PUNTO 5: Zombies → plant (PRIMA - priorità massima!)
        print(f"\n🔍 DEBUG: Before zombie-plant collision - {len(wave_manager.zombie_group)} zombies alive")
        plant_destroyed_by_zombie = _handle_zombie_plant_collisions(
            wave_manager.zombie_group,
            player,
            sound_manager
        )
        print(f"🔍 DEBUG: After zombie-plant collision - {len(wave_manager.zombie_group)} zombies alive")
        
        # PUNTO 4: Zombies → wallnuts (DOPO - solo zombie sopravvissuti)
        _handle_zombie_wallnut_collisions(
            wave_manager.zombie_group,
            wallnut_manager,
            sound_manager
        )
        
        # Combined plant destruction check (from any source)
        plant_destroyed = plant_destroyed_by_projectile or plant_destroyed_by_zombie
        
        # Draw everything ONCE per frame
        draw_game(screen, RunGame_background, player_group, projectile_group, 
                  wallnut_manager.get_wallnuts(),
                  player.life_points,
                  heart_image,
                  wave_manager.zombie_group,
                  wave_manager.zombie_projectile_group)
        
        # Update display BEFORE checking game over
        pygame.display.flip()
        
        # Check if plant was destroyed (game over)
        if plant_destroyed:
            print("💀 GAME OVER - Plant destroyed!")
            sound_manager.stop_music(fade_ms=500)
            # Show game over screen
            action = show_game_over_screen(screen, model, sound_manager)
            
            if action == 'restart': # Restart game
                run_game(screen, model, settings_model, sound_manager)
                return
            elif action == 'menu': # return to main menu
                running = False
            else:  # quit
                pygame.quit()
                sys.exit()

        clock.tick(60)