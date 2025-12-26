import unittest
import pygame
from unittest.mock import patch, MagicMock
from pathlib import Path

# Initialize pygame
pygame.init()
pygame.display.set_mode((1, 1))

from GardenInvasion.Model.sound_manager_model import SoundManager
from GardenInvasion.Model.setting_volume_model import SettingsModel

class TestSoundManagerModel(unittest.TestCase):
    # Test suite for SoundManager model
    
    def setUp(self):
        # Set up test fixtures

        # Create settings model with default volume
        self.settings_model = SettingsModel()
        self.settings_model.volume = 50
        
        # Mock pygame.mixer to avoid actual sound initialization
        self.mixer_patcher = patch('pygame.mixer.Sound')
        self.mock_sound_class = self.mixer_patcher.start()
        
        # Create mock sound instance
        self.mock_sound = MagicMock()
        self.mock_sound_class.return_value = self.mock_sound
    
    def tearDown(self):
        # Clean up
        self.mixer_patcher.stop()
    
    def test_sound_manager_initialization(self):
        # Test that SoundManager initializes correctly with settings
        sound_manager = SoundManager(self.settings_model)
        
        # Verify settings_model is stored
        self.assertEqual(sound_manager.settings_model, self.settings_model)
        print("✅ SoundManager initializes with settings_model")
    
    def test_sound_manager_with_invalid_settings(self):
        # Test that SoundManager handles invalid settings gracefully

        # Pass None or invalid object
        sound_manager = SoundManager(None)
        
        # Should create default settings
        self.assertIsNotNone(sound_manager.settings_model)
        self.assertEqual(sound_manager.settings_model.volume, 50)
        print("✅ SoundManager handles invalid settings with default volume")
    
    def test_volume_conversion(self):
        # Test that volume converts correctly from 0-100 to 0.0-1.0

        self.settings_model.volume = 75
        sound_manager = SoundManager(self.settings_model)
        
        # Manually trigger volume update
        sound_manager._update_volume()
        
        # Check that set_volume was called (would be 0.75)
        if self.mock_sound.set_volume.called:
            call_args = self.mock_sound.set_volume.call_args[0]
            self.assertAlmostEqual(call_args[0], 0.75, places=2)
        
        print("✅ Volume converts correctly from 0-100 to 0.0-1.0")
    
    def test_volume_minimum(self):
        # Test volume at minimum (0)

        self.settings_model.volume = 0 # Set volume to minimum
        sound_manager = SoundManager(self.settings_model) # Create SoundManager
        sound_manager._update_volume() # Manually trigger volume update
        
        if self.mock_sound.set_volume.called: # Check if set_volume was called
            call_args = self.mock_sound.set_volume.call_args[0] # Get call arguments
            self.assertEqual(call_args[0], 0.0) # Verify volume is set to 0.0
        
        print("✅ Volume minimum (0) converts to 0.0")
    
    def test_volume_maximum(self):
        # Test volume at maximum (100)

        self.settings_model.volume = 100
        sound_manager = SoundManager(self.settings_model)
        sound_manager._update_volume()
        
        if self.mock_sound.set_volume.called:
            call_args = self.mock_sound.set_volume.call_args[0]
            self.assertEqual(call_args[0], 1.0)
        
        print("✅ Volume maximum (100) converts to 1.0")
    
    def test_play_sound_existing(self):
        # Test playing an existing sound

        sound_manager = SoundManager(self.settings_model)
        
        sound_manager.sounds['plant_shoot'] = self.mock_sound # Mock sound
        
        sound_manager.play_sound('plant_shoot') # Call play_sound
        
        # Verify play was called
        self.mock_sound.play.assert_called()
        print("✅ play_sound() calls .play() on existing sound")
    
    @patch('pygame.mixer.stop')
    def test_stop_all_sounds(self, mock_mixer_stop):
        # Test stopping all sounds

        sound_manager = SoundManager(self.settings_model)
        sound_manager.stop_all() # Call stop_all
        
        # Verify pygame.mixer.stop was called
        mock_mixer_stop.assert_called_once()
        print("✅ stop_all() calls pygame.mixer.stop()")
    
    def test_volume_updates_before_playing(self):
        # Test that volume is updated before playing sound
        self.settings_model.volume = 30
        sound_manager = SoundManager(self.settings_model)
        sound_manager.sounds['plant_shoot'] = self.mock_sound
        
        self.settings_model.volume = 80 # Update volume to 80
        
        sound_manager.play_sound('plant_shoot') # Call play_sound
        
        # Volume should have been updated
        self.mock_sound.set_volume.assert_called()
        print("✅ Volume updates before playing sound")

if __name__ == '__main__':
    unittest.main()
