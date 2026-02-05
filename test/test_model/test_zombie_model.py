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
    
    def setUp(self):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
    def tearDown(self):
        pygame.quit()
    
    def test_red_zombie_creation(self):
        # creation zombie base 1
        zombie = RedZombie((100, 50), 'straight', 'A')
        
        self.assertEqual(zombie.health, 1)
        self.assertEqual(zombie.speed_y, 2)
        self.assertEqual(zombie.movement_pattern, 'straight')
        self.assertFalse(zombie.can_shoot)
        self.assertEqual(zombie.spawn_point, 'A')
        self.assertIsNotNone(zombie.image)
        self.assertIsNotNone(zombie.rect)
    
    def test_orange_zombie_creation(self):
        # creation zombie base 2
        zombie = OrangeZombie((200, 100), 'B')
        
        self.assertEqual(zombie.health, 2)
        self.assertEqual(zombie.speed_y, 1.5)
        self.assertEqual(zombie.movement_pattern, 'zigzag')
        self.assertTrue(zombie.can_shoot)
        self.assertEqual(zombie.spawn_point, 'B')
        self.assertIsNotNone(zombie.image)
    
    def test_zombie_take_damage(self):
        # test for taking damage
        red_zombie = RedZombie((100, 50), 'straight', 'A')
        orange_zombie = OrangeZombie((200, 100), 'B')
        
        # zombie base 1 gets 1 hit
        is_dead = red_zombie.take_damage()
        self.assertTrue(is_dead)
        
        # zombie base 2 gest 2 hits
        is_dead = orange_zombie.take_damage()
        self.assertFalse(is_dead)
        self.assertEqual(orange_zombie.health, 1)
        is_dead = orange_zombie.take_damage()
        self.assertTrue(is_dead)
    
    def test_zombie_movement_straight(self):
        
        zombie = RedZombie((100, 50), 'straight', 'A')
        initial_y = zombie.rect.y
        initial_midtop_x = zombie.rect.midtop[0]
        
        zombie.update()
        
        self.assertEqual(zombie.rect.y, initial_y + zombie.speed_y)
        self.assertEqual(zombie.rect.midtop[0], initial_midtop_x) # No horizontal movement
    
    def test_red_zombie_zigzag_movement(self):
        zombie_b = RedZombie((SCREEN_WIDTH // 3, 50), 'zigzag', 'B')
        zombie_c = RedZombie((SCREEN_WIDTH * 2 // 3, 50), 'zigzag', 'C')
        
        initial_x_b = zombie_b.rect.x
        initial_x_c = zombie_c.rect.x
        
        for _ in range(10):
            zombie_b.update()
            zombie_c.update()
        
        self.assertNotEqual(zombie_b.rect.x, initial_x_b) # verify horizontal movement
        self.assertNotEqual(zombie_c.rect.x, initial_x_c)
        
        self.assertLess(zombie_b.rect.x, SCREEN_WIDTH // 2) # zombie B should move left
        self.assertGreater(zombie_c.rect.x, SCREEN_WIDTH // 2) # zombie C should move right
    
    def test_orange_zombie_full_screen_movement(self):
        
        zombie_b = OrangeZombie((SCREEN_WIDTH // 3, 50), 'B')
        zombie_c = OrangeZombie((SCREEN_WIDTH * 2 // 3, 50), 'C')
        
        initial_x_b = zombie_b.rect.x
        initial_x_c = zombie_c.rect.x
        
        for _ in range(50):
            zombie_b.update()
            zombie_c.update()
        
        # assess horizontal movement within screen bounds
        self.assertNotEqual(zombie_b.rect.x, initial_x_b)
        self.assertNotEqual(zombie_c.rect.x, initial_x_c)
        
        # assess they stay within screen bounds
        self.assertGreaterEqual(zombie_b.rect.x, 0)
        self.assertLessEqual(zombie_b.rect.x, SCREEN_WIDTH - 50)
        self.assertGreaterEqual(zombie_c.rect.x, 0)
        self.assertLessEqual(zombie_c.rect.x, SCREEN_WIDTH - 50)
    
    def test_zombie_wave_delay(self):
        zombie = RedZombie((100, 50), 'straight', 'A', wave_delay=1000)
        
        self.assertFalse(zombie.active)
        
        zombie.spawn_time = pygame.time.get_ticks() - 1500
        zombie.update()
        
        # Now it should be active
        self.assertTrue(zombie.active)
    
    def test_zombie_boundary_removal(self):
        zombie = RedZombie((SCREEN_WIDTH // 2, SCREEN_HEIGHT + 100), 'straight', 'A')
        zombie.update()
        
class TestZombieIntegration(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()
    
    def test_multiple_zombies_movement(self):
        # assess multiple zombies moving simultaneously
        zombies = [
            RedZombie((SCREEN_WIDTH // 3, 50), 'zigzag', 'B'),
            RedZombie((SCREEN_WIDTH * 2 // 3, 50), 'zigzag', 'C'),
            OrangeZombie((SCREEN_WIDTH // 4, 100), 'B'),
            OrangeZombie((SCREEN_WIDTH * 3 // 4, 100), 'C')
        ]
        
        for _ in range(30):
            for zombie in zombies:
                zombie.update()
        
        for zombie in zombies: # verify they have moved
            self.assertNotEqual(zombie.rect.y, 50 if zombie.color == (255,0,0) else 100)

if __name__ == '__main__':
    unittest.main(verbosity=2)
