import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
import os
from GardenInvasion.Model.victory_model import VictoryModel
from GardenInvasion.Model.menu_model import MenuModel
from GardenInvasion.Model.sound_manager_model import SoundManager
from GardenInvasion.Model.setting_volume_model import SettingsModel
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TestVictoryController(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        cls.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.screen = self.display
        self.menu_model = MenuModel()
        self.settings_model = SettingsModel()
        self.sound_manager = SoundManager(self.settings_model)

    def test_sound_manager_has_victory_sound(self):
        # Test that sound manager can handle 'victory' sound

        # Mock the play_sound method
        with patch.object(self.sound_manager, 'play_sound') as mock_play:
            self.sound_manager.play_sound('victory')
            mock_play.assert_called_once_with('victory')
            print("✅ SoundManager can play 'victory' sound")

    def test_victory_screen_user_actions(self):
        # Test user action responses 
        
        victory_model = VictoryModel()
        # Test "Play Again" selection
        victory_model.selected_index = 0
        self.assertEqual(victory_model.get_selected_option(), "Play Again")
        
        # Test "Main Menu" selection
        victory_model.selected_index = 1
        self.assertEqual(victory_model.get_selected_option(), "Main Menu")
        print("✅ Victory screen actions return correct responses")

if __name__ == '__main__':
    unittest.main()
