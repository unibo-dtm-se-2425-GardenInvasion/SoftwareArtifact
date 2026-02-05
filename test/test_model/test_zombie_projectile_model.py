import unittest
import pygame
import sys
import os
from GardenInvasion.Model.zombie_projectile_model import ZombieProjectile
from GardenInvasion.Utilities.constants import SCREEN_HEIGHT

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GardenInvasion_path = os.path.join(project_root, 'GardenInvasion')
sys.path.insert(0, GardenInvasion_path)

class TestZombieProjectileModel(unittest.TestCase):
    def setUp(self):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
    def tearDown(self):
        # clean up pygame
        pygame.quit()
    
    def test_projectile_creation(self):
        # creation of projectile
        projectile = ZombieProjectile((100, 200))
        
        self.assertEqual(projectile.speed, 5)
        self.assertEqual(projectile.rect.midbottom, (100, 200))
        
        # Verify image exists
        self.assertIsNotNone(projectile.image)
        self.assertGreater(projectile.image.get_width(), 0)
        self.assertGreater(projectile.image.get_height(), 0)
    
    def test_projectile_movement(self):
        # projectile movement downwards
        start_pos = (100, 200)
        projectile = ZombieProjectile(start_pos)
        
        initial_midbottom = projectile.rect.midbottom
        projectile.update()
        self.assertEqual(projectile.rect.midbottom[0], initial_midbottom[0])  # X unchanged
        self.assertEqual(projectile.rect.midbottom[1], initial_midbottom[1] + projectile.speed)  # Y increases
    
    def test_projectile_boundary_detection(self):
        # verify projectile goes off screen
        
        projectile = ZombieProjectile((100, SCREEN_HEIGHT - 50)) # starts near bottom
        
        self.assertLess(projectile.rect.top, SCREEN_HEIGHT)
        
        for _ in range(20):
            projectile.update()
        self.assertGreater(projectile.rect.top, SCREEN_HEIGHT)
    
    def test_multiple_updates(self):
        # test multiple updates and position
        projectile = ZombieProjectile((100, 100))
        initial_midbottom_y = projectile.rect.midbottom[1]
        
        for i in range(10):
            projectile.update()
        
        expected_y = initial_midbottom_y + (projectile.speed * 10)
        self.assertEqual(projectile.rect.midbottom[1], expected_y)
    
    def test_projectile_consistency(self):
        # test that projectile maintains consistent horizontal position
        spawn_pos = (150, 300)
        projectile = ZombieProjectile(spawn_pos)
        
        self.assertEqual(projectile.rect.midbottom[0], 150) # initial x position
        
        projectile.update()
        self.assertEqual(projectile.rect.midbottom[0], 150) # x position after update

if __name__ == '__main__':
    unittest.main(verbosity=2)
