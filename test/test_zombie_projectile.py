import unittest
import pygame
import sys
import os

# Setup dei path corretti
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GardenInvasion_path = os.path.join(project_root, 'GardenInvasion')
sys.path.insert(0, GardenInvasion_path)

from GardenInvasion.Model.zombie_projectile_model import ZombieProjectile
from GardenInvasion.Utilities.constants import SCREEN_HEIGHT

class TestZombieProjectileModel(unittest.TestCase):
    """Test per la classe ZombieProjectile"""
    
    def setUp(self):
        """Setup prima di ogni test"""
        pygame.init()
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        pygame.quit()
    
    def test_projectile_creation(self):
        """Test creazione proiettile zombie - parte dal centro basso"""
        projectile = ZombieProjectile((100, 200))
        
        # Verifica attributi base
        self.assertEqual(projectile.speed, 5)
        
        # ✅ VERIFICA CORRETTA: midbottom è il punto di riferimento
        self.assertEqual(projectile.rect.midbottom, (100, 200))
        
        # ❌ NON verificare rect.x direttamente - dipende dalle dimensioni
        # rect.x sarà 100 - (width/2) = 100 - 5 = 95
        
        # Verifica dimensioni
        self.assertEqual(projectile.image.get_size(), (10, 20))
        
        # Verifica colore (giallo)
        expected_color = (255, 255, 0)
        actual_color = projectile.image.get_at((5, 10))  # Pixel al centro
        self.assertEqual(actual_color[:3], expected_color)
    
    def test_projectile_movement(self):
        """Test movimento proiettile verso il basso"""
        start_pos = (100, 200)
        projectile = ZombieProjectile(start_pos)
        
        # ✅ Salva il punto di riferimento CORRETTO
        initial_midbottom = projectile.rect.midbottom
        
        # Simula update
        projectile.update()
        
        # ✅ VERIFICA CORRETTA: midbottom si muove verso il basso
        self.assertEqual(projectile.rect.midbottom[0], initial_midbottom[0])  # X invariata
        self.assertEqual(projectile.rect.midbottom[1], initial_midbottom[1] + projectile.speed)  # Y aumenta
    
    def test_projectile_boundary_detection(self):
        """Test che il proiettile rilevi correttamente quando esce dallo schermo"""
        # Crea proiettile che inizialmente è dentro lo schermo
        projectile = ZombieProjectile((100, SCREEN_HEIGHT - 50))
        
        # Dovrebbe essere visibile inizialmente
        self.assertLess(projectile.rect.top, SCREEN_HEIGHT)
        
        # Simula molti update fino a che non esce
        for _ in range(20):  # Abbastanza per uscire
            projectile.update()
        
        # ✅ Ora dovrebbe essere fuori dallo schermo
        self.assertGreater(projectile.rect.top, SCREEN_HEIGHT)
    
    def test_multiple_updates(self):
        """Test movimento prolungato del proiettile"""
        projectile = ZombieProjectile((100, 100))
        initial_midbottom_y = projectile.rect.midbottom[1]
        
        # Simula 10 frame di movimento
        for i in range(10):
            projectile.update()
        
        # ✅ Verifica usando il punto di riferimento corretto
        expected_y = initial_midbottom_y + (projectile.speed * 10)
        self.assertEqual(projectile.rect.midbottom[1], expected_y)
    
    def test_projectile_consistency(self):
        """Test che il punto di sparo (midbottom) rimanga coerente"""
        spawn_pos = (150, 300)
        projectile = ZombieProjectile(spawn_pos)
        
        # ✅ Il punto di sparo dovrebbe rimanere coerente orizzontalmente
        self.assertEqual(projectile.rect.midbottom[0], 150)
        
        # Dopo il movimento, la X del punto di riferimento non cambia
        projectile.update()
        self.assertEqual(projectile.rect.midbottom[0], 150)

if __name__ == '__main__':
    unittest.main(verbosity=2)
