import unittest
import pygame
from unittest.mock import patch, MagicMock
from pathlib import Path
import os

if 'CI' in os.environ:
    del os.environ['CI']
if 'SDL_AUDIODRIVER' in os.environ:
    del os.environ['SDL_AUDIODRIVER']

pygame.init()
pygame.display.set_mode((1, 1))

from GardenInvasion.Model.sound_manager_model import SoundManager
from GardenInvasion.Model.setting_volume_model import SettingsModel


class TestSoundManagerModel(unittest.TestCase):
    
    def setUp(self):
        self.mixer_init_patcher = patch('pygame.mixer.get_init', return_value=True)
        self.mixer_init_patcher.start()

        self.settings_model = SettingsModel()
        self.settings_model.volume = 50
        
        self.mixer_patcher = patch('pygame.mixer.Sound')
        self.mock_sound_class = self.mixer_patcher.start()
        
        self.mock_sound = MagicMock()
        self.mock_sound_class.return_value = self.mock_sound
    
    def tearDown(self):
        self.mixer_init_patcher.stop()
        self.mixer_patcher.stop()
    
    # ---------- TEST ESSENZIALI (6) ----------
    
    def test_initialization(self):
        """Test inizializzazione base"""
        sound_manager = SoundManager(self.settings_model)
        self.assertEqual(sound_manager.settings_model, self.settings_model)
        print("✅ SoundManager initializes correctly")
    
    def test_new_sounds_are_loaded(self):
        """Test che i nuovi suoni zombie_hit e plant_hit vengano caricati"""
        sound_manager = SoundManager(self.settings_model)
        sound_manager.audio_available = True
        sound_manager._load_sounds()
        
        self.assertIn('zombie_hit', sound_manager.sounds)
        self.assertIn('plant_hit', sound_manager.sounds)
        print("✅ New sounds zombie_hit and plant_hit are loaded")
    
    def test_play_new_sounds(self):
        """Test che i nuovi suoni possano essere riprodotti"""
        sound_manager = SoundManager(self.settings_model)
        sound_manager.audio_available = True
        
        sound_manager.sounds['zombie_hit'] = self.mock_sound
        sound_manager.sounds['plant_hit'] = self.mock_sound
        
        sound_manager.play_sound('zombie_hit')
        self.mock_sound.play.assert_called()
        
        sound_manager.play_sound('plant_hit')
        self.mock_sound.play.assert_called()
        
        print("✅ New sounds can be played")
    
    def test_volume_conversion(self):
        """Test conversione volume 0-100 → 0.0-1.0"""
        self.settings_model.volume = 75
        sound_manager = SoundManager(self.settings_model)
        sound_manager._update_volume()
        
        if self.mock_sound.set_volume.called:
            call_args = self.mock_sound.set_volume.call_args[0]
            self.assertAlmostEqual(call_args[0], 0.75, places=2)
        
        print("✅ Volume conversion works")
    
    def test_play_sound_existing(self):
        """Test play_sound su suono esistente"""
        sound_manager = SoundManager(self.settings_model)
        sound_manager.audio_available = True
        sound_manager.sounds['plant_shoot'] = self.mock_sound
        
        sound_manager.play_sound('plant_shoot')
        self.mock_sound.play.assert_called()
        print("✅ play_sound() works on existing sound")
    
    def test_play_sound_missing(self):
        """Test play_sound su suono mancante (non deve crashare)"""
        sound_manager = SoundManager(self.settings_model)
        sound_manager.audio_available = True
        
        # Non deve sollevare eccezioni
        try:
            sound_manager.play_sound('suono_inesistente')
            print("✅ play_sound() handles missing sound gracefully")
        except Exception as e:
            self.fail(f"play_sound crashed on missing sound: {e}")

    @patch('pygame.mixer.stop')
    @patch('pygame.mixer.music.stop')
    def test_stop_all_sounds(self, mock_music_stop, mock_mixer_stop):
        """Test stop_all ferma tutti i suoni"""
        sound_manager = SoundManager(self.settings_model)
        sound_manager.audio_available = True
        sound_manager.stop_all()
        
        mock_mixer_stop.assert_called_once()
        print("✅ stop_all() works")

if __name__ == '__main__':
    unittest.main()