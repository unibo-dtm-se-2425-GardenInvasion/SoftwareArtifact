import unittest
import pygame
import sys
import os

# Setup dei path corretti
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GardenInvasion_path = os.path.join(project_root, 'GardenInvasion')
sys.path.insert(0, GardenInvasion_path)

from GardenInvasion.Model.wave_model import WaveManager
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class TestWaveModel(unittest.TestCase):
    
    def setUp(self):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
    def tearDown(self):
        pygame.quit()
    
    def test_wave_manager_creation(self):
        wave_manager = WaveManager()
        
        self.assertEqual(wave_manager.current_wave, 0)
        self.assertEqual(wave_manager.total_waves, 5)
        self.assertTrue(wave_manager.wave_complete)
        self.assertEqual(len(wave_manager.zombie_group), 0)
        self.assertEqual(len(wave_manager.zombie_projectile_group), 0)
    
    def test_spawn_points(self):
        wave_manager = WaveManager()
        # assess spawn points
        expected_points = ['A', 'B', 'C', 'D', 'E']
        for point in expected_points:
            self.assertIn(point, wave_manager.spawn_points)
        
        self.assertEqual(wave_manager.spawn_points['A'][0], SCREEN_WIDTH // 2)
        self.assertEqual(wave_manager.spawn_points['B'][0], SCREEN_WIDTH // 3)
        self.assertEqual(wave_manager.spawn_points['C'][0], SCREEN_WIDTH * 2 // 3)
        self.assertEqual(wave_manager.spawn_points['D'][0], SCREEN_WIDTH // 4)
        self.assertEqual(wave_manager.spawn_points['E'][0], SCREEN_WIDTH * 3 // 4)
        
        for point in wave_manager.spawn_points.values(): # verify y-coordinate
            self.assertEqual(point[1], -50)
    
    def test_first_wave_start(self):
        wave_manager = WaveManager()
        
        wave_manager.start_first_wave()
        self.assertTrue(wave_manager.waiting_for_next_wave)
        self.assertGreater(wave_manager.next_wave_timer, 0)
    
    def test_wave_1_spawn(self):
        
        wave_manager = WaveManager()
        wave_manager.current_wave = 1
        wave_manager._wave_1()
        
        self.assertEqual(len(wave_manager.zombie_group), 1) # wave 1 should spawn 1 zombie base 1
    
    def test_wave_2_spawn(self):
        wave_manager = WaveManager()
        wave_manager.current_wave = 2
        wave_manager._wave_2()
        
        self.assertEqual(len(wave_manager.zombie_group), 2) # wave 2 should spawn 2 zigzag zombies base 1
    
    def test_wave_3_spawn(self):
        wave_manager = WaveManager()
        wave_manager.current_wave = 3
        wave_manager._wave_3()
        
        self.assertEqual(len(wave_manager.zombie_group), 2) # wave 3 should spawn 2 zombies base 2
        
        for zombie in wave_manager.zombie_group:
            self.assertEqual(zombie.health, 2)
    
    def test_wave_4_spawn(self):
        wave_manager = WaveManager()
        wave_manager.current_wave = 4
        wave_manager._wave_4()
        
        self.assertEqual(len(wave_manager.zombie_group), 3) # wave 4 should spawn 3 zigzag zombies base 1
    
    def test_wave_5_spawn(self):
        wave_manager = WaveManager()
        wave_manager.current_wave = 5
        wave_manager._wave_5()
        
        self.assertEqual(len(wave_manager.zombie_group), 3) # wave 5 phase 1 should spawn 3 zombies base 1
        self.assertEqual(len(wave_manager.wave_timers), 2)  
    
    def test_wave_5_phase2(self):
        wave_manager = WaveManager()
        wave_manager._wave_5_phase2()
        
        self.assertEqual(len(wave_manager.zombie_group), 2) # wave 5 phase 2 should spawn 2 zigzag zombies base 1
    
    def test_wave_5_phase3(self):
        wave_manager = WaveManager()
        wave_manager._wave_5_phase3()
        
        self.assertEqual(len(wave_manager.zombie_group), 2) # wave 5 phase 3 should spawn 2 zombies base 2
        
        for zombie in wave_manager.zombie_group:
            self.assertEqual(zombie.health, 2)
    
    def test_wave_completion_detection(self):
        wave_manager = WaveManager()
        wave_manager.current_wave = 1
        wave_manager.wave_complete = False
        wave_manager.waiting_for_next_wave = False
        
        wave_manager._spawn_red('A', 'straight') # Spawn one more zombie
        self.assertEqual(len(wave_manager.zombie_group), 1)
        
        for zombie in wave_manager.zombie_group:
            zombie.kill() # simulate all zombies being killed
        
        wave_manager.update()
        self.assertTrue(wave_manager.wave_complete)
    
    def test_all_waves_completed(self):
        wave_manager = WaveManager()
        
        wave_manager.current_wave = 5 
        wave_manager.wave_complete = True
        self.assertTrue(wave_manager.all_waves_completed()) # assess all waves completed
        
        wave_manager.current_wave = 3
        self.assertFalse(wave_manager.all_waves_completed()) # assess not all waves completed
    
    def test_wave_delay_spawn(self):
        wave_manager = WaveManager()
        
        wave_manager._spawn_red('A', 'straight', wave_delay=1000)
        wave_manager._spawn_orange('B', wave_delay=500)
        
        self.assertEqual(len(wave_manager.zombie_group), 2) # should have 2 zombies scheduled to spawn

class TestWaveIntegration(unittest.TestCase):
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()
    
    def test_multiple_waves_sequence(self):
        wave_manager = WaveManager()
        
        wave_manager.start_first_wave()
        
        wave_manager.next_wave_timer = pygame.time.get_ticks() - 1000
        wave_manager.update()
        
        self.assertEqual(wave_manager.current_wave, 1) # first wave started
        self.assertFalse(wave_manager.wave_complete)
    
    def test_zombie_movement_in_wave(self):
        wave_manager = WaveManager()
        wave_manager.current_wave = 2
        wave_manager._wave_2()
        
        initial_positions = [] # check initial positions
        for zombie in wave_manager.zombie_group: # store initial positions
            initial_positions.append((zombie.rect.x, zombie.rect.y))
        
        wave_manager.update()
        for i, zombie in enumerate(wave_manager.zombie_group): # check positions after update
            self.assertGreater(zombie.rect.y, initial_positions[i][1]) 
            self.assertNotEqual(zombie.rect.x, initial_positions[i][0])

if __name__ == '__main__':
    unittest.main(verbosity=2)