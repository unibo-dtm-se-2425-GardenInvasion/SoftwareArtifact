import unittest
import pygame
import os
from GardenInvasion.Model.wave_model import WaveManager


class TestWaveManagerVictory(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.wave_manager = WaveManager()

    def test_is_victory_method_exists(self):
        # Test that is_victory method exists

        self.assertTrue(hasattr(self.wave_manager, 'is_victory'))
        self.assertTrue(callable(self.wave_manager.is_victory))
        print("✅ is_victory method exists in WaveManager")

    def test_no_victory_at_start(self):
        # Test that victory is False at game start

        self.assertFalse(self.wave_manager.is_victory())
        print("✅ No victory detected at game start")

    def test_no_victory_during_waves(self):
        # Test that victory is False while waves are ongoing

        self.wave_manager.current_wave = 3
        self.assertFalse(self.wave_manager.is_victory())
        print("✅ No victory detected during waves")

    def test_victory_when_all_conditions_met(self):
        # Test that victory is True when all conditions are met

        # Simulate all waves completed
        self.wave_manager.current_wave = 5
        # No zombies alive
        self.wave_manager.zombie_group.empty()
        # No pending spawns
        self.wave_manager.wave_timers = []
        
        self.assertTrue(self.wave_manager.is_victory())
        print("✅ Victory detected when all conditions met")

    def test_victory_after_final_wave(self):
        # Test victory detection after final wave completion

        # Set wave beyond total
        self.wave_manager.current_wave = 6
        self.wave_manager.zombie_group.empty()
        self.wave_manager.wave_timers = []
        
        self.assertTrue(self.wave_manager.is_victory())
        print("✅ Victory detected after all waves completed")

if __name__ == '__main__':
    unittest.main()
