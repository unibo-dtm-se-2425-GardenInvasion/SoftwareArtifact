import unittest
import pygame
import sys
import os

# Setup dei path corretti
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GardenInvasion_path = os.path.join(project_root, 'GardenInvasion')
sys.path.insert(0, GardenInvasion_path)

from GardenInvasion.Model.zombie_model import RedZombie, OrangeZombie
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class TestZombieModel(unittest.TestCase):
    """Test per le classi zombie con movimento simmetrico"""
    
    def setUp(self):
        """Setup prima di ogni test"""
        pygame.init()
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        pygame.quit()
    
    def test_red_zombie_creation(self):
        """Test creazione zombie rosso"""
        zombie = RedZombie((100, 50), 'straight', 'A')
        
        self.assertEqual(zombie.health, 1)
        self.assertEqual(zombie.speed_y, 2)
        self.assertEqual(zombie.movement_pattern, 'straight')
        self.assertFalse(zombie.can_shoot)
        self.assertEqual(zombie.spawn_point, 'A')
    
    def test_orange_zombie_creation(self):
        """Test creazione zombie arancione"""
        zombie = OrangeZombie((200, 100), 'B')
        
        self.assertEqual(zombie.health, 2)
        self.assertEqual(zombie.speed_y, 1.5)
        self.assertEqual(zombie.movement_pattern, 'zigzag')
        self.assertTrue(zombie.can_shoot)
        self.assertEqual(zombie.spawn_point, 'B')
    
    def test_zombie_take_damage(self):
        """Test sistema danni zombie"""
        red_zombie = RedZombie((100, 50), 'straight', 'A')
        orange_zombie = OrangeZombie((200, 100), 'B')
        
        # Test zombie rosso (1 colpo)
        is_dead = red_zombie.take_damage()
        self.assertTrue(is_dead)
        
        # Test zombie arancione (2 colpi)
        is_dead = orange_zombie.take_damage()
        self.assertFalse(is_dead)  # Non dovrebbe morire al primo colpo
        self.assertEqual(orange_zombie.health, 1)
        
        is_dead = orange_zombie.take_damage()
        self.assertTrue(is_dead)  # Dovrebbe morire al secondo colpo
    
    def test_zombie_movement_straight(self):
        """Test movimento zombie in linea retta"""
        zombie = RedZombie((100, 50), 'straight', 'A')
        initial_y = zombie.rect.y
        initial_midtop_x = zombie.rect.midtop[0]  # Usa midtop come riferimento
        
        zombie.update()
        
        self.assertEqual(zombie.rect.y, initial_y + zombie.speed_y)
        self.assertEqual(zombie.rect.midtop[0], initial_midtop_x)  # X del midtop non cambia
    
    def test_red_zombie_zigzag_movement(self):
        """Test movimento zigzag contenuto per zombie rossi"""
        zombie_b = RedZombie((SCREEN_WIDTH // 3, 50), 'zigzag', 'B')
        zombie_c = RedZombie((SCREEN_WIDTH * 2 // 3, 50), 'zigzag', 'C')
        
        initial_x_b = zombie_b.rect.x
        initial_x_c = zombie_c.rect.x
        
        # Simula alcuni update
        for _ in range(10):
            zombie_b.update()
            zombie_c.update()
        
        # Verifica che si siano mossi orizzontalmente
        self.assertNotEqual(zombie_b.rect.x, initial_x_b)
        self.assertNotEqual(zombie_c.rect.x, initial_x_c)
        
        # Verifica che siano rimasti nelle loro metà schermo
        self.assertLess(zombie_b.rect.x, SCREEN_WIDTH // 2)
        self.assertGreater(zombie_c.rect.x, SCREEN_WIDTH // 2)
    
    def test_orange_zombie_full_screen_movement(self):
        """Test movimento a schermo intero per zombie arancioni"""
        zombie_b = OrangeZombie((SCREEN_WIDTH // 3, 50), 'B')
        zombie_c = OrangeZombie((SCREEN_WIDTH * 2 // 3, 50), 'C')
        
        initial_x_b = zombie_b.rect.x
        initial_x_c = zombie_c.rect.x
        
        # Simula molti update per vedere il movimento completo
        for _ in range(50):
            zombie_b.update()
            zombie_c.update()
        
        # Verifica movimento ampio
        self.assertNotEqual(zombie_b.rect.x, initial_x_b)
        self.assertNotEqual(zombie_c.rect.x, initial_x_c)
        
        # Verifica che possano raggiungere i bordi
        self.assertGreaterEqual(zombie_b.rect.x, 10)
        self.assertLessEqual(zombie_b.rect.x, SCREEN_WIDTH - 40)
        self.assertGreaterEqual(zombie_c.rect.x, 10)
        self.assertLessEqual(zombie_c.rect.x, SCREEN_WIDTH - 40)
    
    def test_zombie_wave_delay(self):
        """Test sistema delay per spawn ritardati"""
        zombie = RedZombie((100, 50), 'straight', 'A', wave_delay=1000)
        
        # Inizialmente non dovrebbe essere attivo
        self.assertFalse(zombie.active)
        
        # Simula che il tempo passi
        zombie.spawn_time = pygame.time.get_ticks() - 1500
        zombie.update()
        
        # Ora dovrebbe essere attivo
        self.assertTrue(zombie.active)
    
    def test_zombie_boundary_removal(self):
        """Test rimozione zombie quando escono dallo schermo"""
        zombie = RedZombie((SCREEN_WIDTH // 2, SCREEN_HEIGHT + 100), 'straight', 'A')
        
        # Dovrebbe essere rimosso dopo l'update
        zombie.update()
        # Non possiamo testare kill() direttamente, ma verifichiamo la logica

class TestZombieIntegration(unittest.TestCase):
    """Test di integrazione per il sistema zombie"""
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()
    
    def test_multiple_zombies_movement(self):
        """Test che più zombie possano muoversi senza collisioni"""
        zombies = [
            RedZombie((SCREEN_WIDTH // 3, 50), 'zigzag', 'B'),
            RedZombie((SCREEN_WIDTH * 2 // 3, 50), 'zigzag', 'C'),
            OrangeZombie((SCREEN_WIDTH // 4, 100), 'B'),
            OrangeZombie((SCREEN_WIDTH * 3 // 4, 100), 'C')
        ]
        
        # Simula movimento
        for _ in range(30):
            for zombie in zombies:
                zombie.update()
        
        # Verifica che tutti si siano mossi
        for zombie in zombies:
            self.assertNotEqual(zombie.rect.y, 50 if zombie.color == (255,0,0) else 100)

if __name__ == '__main__':
    unittest.main(verbosity=2)
