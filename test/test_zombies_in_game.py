# To successfully run this visual test go to file: SoftwareArtifact/GardenInvasion/Model/plant_model.py and substitute line 2 with: from Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import sys
import os

# Aggiungi GardenInvasion al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'GardenInvasion'))

# Ora importa
from Model.wave_model import WaveManager
from Model.plant_model import Player
from Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def test_zombies_visual():
    """Test visivo degli zombie nel gioco"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test Zombie Visual")
    clock = pygame.time.Clock()
    
    # Crea wave manager e avvia ondata 1 immediatamente
    wave_manager = WaveManager()
    wave_manager.current_wave = 1
    wave_manager.wave_complete = False
    wave_manager._wave_1()  # Spawna ondata 1
    
    # Crea giocatore
    player = Player((SCREEN_WIDTH//2, SCREEN_HEIGHT*0.95))
    player_group = pygame.sprite.GroupSingle(player)
    
    print("🧪 TEST VISIVO ZOMBIE")
    print("Controlla che:")
    print("  - Zombie rossi (rettangoli rossi) siano visibili")
    print("  - Zombie si muovano verso il basso")
    print("  - Zombie arancioni (rettangoli arancioni) siano visibili")
    print("  - Zombie arancioni si muovano a zigzag")
    print("Premi ESC per uscire")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        # Aggiorna
        player_group.update()
        wave_manager.update()
        
        # Disegna
        screen.fill((0, 0, 0))  # Sfondo nero
        
        # Disegna zombie
        wave_manager.zombie_group.draw(screen)
        
        # Disegna giocatore
        player_group.draw(screen)
        
        # Info testo
        font = pygame.font.SysFont("Arial", 20)
        info_text = f"Zombie: {len(wave_manager.zombie_group)} - Premi ESC per uscire"
        text_surface = font.render(info_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("✅ Test visivo completato!")

if __name__ == "__main__":
    test_zombies_visual()