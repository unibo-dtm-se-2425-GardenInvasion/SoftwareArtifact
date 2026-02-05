import pygame
import sys
import os
from GardenInvasion.Model.setting_volume_model import SettingsModel

# Aggiungi GardenInvasion al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'GardenInvasion'))

# Ora importa
from GardenInvasion.Model.wave_model import WaveManager
from GardenInvasion.Model.plant_model import Player
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def test_zombies_visual():
    # Test visivo degli zombie nel gioco
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test Zombie Visual")
    clock = pygame.time.Clock()
    
    # create wave manager and spawn wave 1
    wave_manager = WaveManager()
    wave_manager.current_wave = 1
    wave_manager.wave_complete = False
    wave_manager._wave_1()  # Spawna wave 1
    
    # Create player with settings_model
    settings_model = SettingsModel()
    player = Player((SCREEN_WIDTH//2, SCREEN_HEIGHT*0.95), settings_model)
    player_group = pygame.sprite.GroupSingle(player)
   
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        # update
        player_group.update()
        wave_manager.update()
        
        # draw
        screen.fill((0, 0, 0))  # Sfondo nero
        
        # draw zombies
        wave_manager.zombie_group.draw(screen)
        
        if wave_manager.zombie_projectile_group:
            wave_manager.zombie_projectile_group.draw(screen)

        # draw player
        player_group.draw(screen)
        
        font = pygame.font.SysFont("Arial", 20)
        info_text = f"Zombie: {len(wave_manager.zombie_group)} - Premi ESC per uscire"
        text_surface = font.render(info_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("Visual test completed.")

if __name__ == "__main__":
    test_zombies_visual()