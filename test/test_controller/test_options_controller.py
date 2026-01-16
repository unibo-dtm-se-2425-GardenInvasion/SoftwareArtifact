import unittest
import pygame
from unittest.mock import patch, MagicMock
import sys

# Initialize pygame for event handling tests
pygame.init()
pygame.display.set_mode((1, 1))  # Dummy display

from GardenInvasion.Controller.options_controller import run_options, run_volume_menu
from GardenInvasion.Model.menu_model import MenuModel
from GardenInvasion.Model.setting_volume_model import SettingsModel

class TestOptionsController(unittest.TestCase):
    # Test suite for options controller
    
    def setUp(self):
        # Set up test fixtures before each test

        # Mock pygame.image.load
        self.mock_surface = pygame.Surface((100, 100))
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.image_patcher.start()
        
        # Create test objects
        self.screen = pygame.Surface((600, 600))
        self.menu_model = MenuModel()
        self.settings_model = SettingsModel() # Settings model instance
        self.mock_sound_manager = MagicMock() # Mock sound manager
        self.settings_model.volume = 50
        
        self.background_surf = pygame.Surface((600, 600))
        self.background_rect = self.background_surf.get_rect()
        
        # Create test fonts
        self.title_font = pygame.font.SysFont("Arial", 72)
        self.item_font = pygame.font.SysFont("Arial", 30)
        self.inst_font = pygame.font.SysFont("Arial", 16)
        self.fonts = (self.item_font, self.inst_font, self.title_font)
    
    def tearDown(self):
        self.image_patcher.stop()
        pygame.event.clear()
    
    @patch('GardenInvasion.Controller.options_controller.draw_options_menu')
    @patch('pygame.display.flip')
    def test_up_down_navigation_through_options(self, mock_flip, mock_draw):
        # Test navigating through options with UP/DOWN keys

        mock_draw.return_value = [pygame.Rect(0, 0, 100, 30) for _ in range(4)] # Mock menu item rects
        
        # Navigate down twice, then up once, then select Back
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Select Back
            [],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            run_options(self.screen, self.menu_model, self.background_surf, 
                       self.background_rect, self.fonts, self.settings_model, self.mock_sound_manager)
        
        print("✅ UP/DOWN navigation through options works")
    
    @patch('GardenInvasion.Controller.options_controller.run_volume_menu')
    @patch('GardenInvasion.Controller.options_controller.draw_options_menu')
    @patch('pygame.display.flip')
    def test_enter_opens_volume_submenu(self, mock_flip, mock_draw, mock_volume):
        # Test that Enter opens volume submenu

        mock_draw.return_value = [pygame.Rect(0, 0, 100, 30) for _ in range(4)]
        mock_volume.return_value = 75  # Return new volume
        
        # Select Volume (index 0) and press Enter, then navigate to Back and exit
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Open volume
            [],  # After volume menu returns
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # Navigate to Skin
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # Navigate to Contact
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # Navigate to Back
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Select Back
            [],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            run_options(self.screen, self.menu_model, self.background_surf, 
                       self.background_rect, self.fonts, self.settings_model, self.mock_sound_manager)
        
        mock_volume.assert_called_once()
        print("✅ Enter opens volume submenu")
    
    @patch('GardenInvasion.Controller.options_controller.run_skin_selection')
    @patch('GardenInvasion.Controller.options_controller.draw_options_menu')
    @patch('pygame.display.flip')
    def test_enter_opens_skin_personalization(self, mock_flip, mock_draw, mock_skin):
        # Test that Enter opens skin personalization

        mock_draw.return_value = [pygame.Rect(0, 0, 100, 30) for _ in range(4)]
        mock_skin.return_value = 'back'  # Return to options
        
        # Navigate to Skin Personalization (index 1) and press Enter
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # To Skin
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Open skin
            [],  # After skin selection returns
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # Navigate to Contact
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # Navigate to Back
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Select Back
            [],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            run_options(self.screen, self.menu_model, self.background_surf, 
                       self.background_rect, self.fonts, self.settings_model, self.mock_sound_manager)
        
        mock_skin.assert_called_once()
        print("✅ Enter opens skin personalization")
    
    @patch('GardenInvasion.Controller.options_controller.show_contact_confirmation')
    @patch('GardenInvasion.Controller.options_controller.draw_options_menu')
    @patch('pygame.display.flip')
    def test_enter_opens_contact_modal(self, mock_flip, mock_draw, mock_contact):
        # Test that Enter opens contact modal

        mock_draw.return_value = [pygame.Rect(0, 0, 100, 30) for _ in range(4)]
        mock_contact.return_value = False  # Don't open email
        
        # Navigate to Contact Us (index 2) and press Enter
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # To Skin
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # To Contact
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Open contact
            [],  # After contact modal returns
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # Navigate to Back
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Select Back
            [],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            run_options(self.screen, self.menu_model, self.background_surf, 
                       self.background_rect, self.fonts, self.settings_model, self.mock_sound_manager)
        
        mock_contact.assert_called_once()
        print("✅ Enter opens contact modal")
    
    @patch('GardenInvasion.Controller.options_controller.draw_options_menu')
    @patch('pygame.display.flip')
    def test_back_button_returns_to_menu(self, mock_flip, mock_draw):
        # Test that selecting Back returns to main menu
        
        mock_draw.return_value = [pygame.Rect(0, 0, 100, 30) for _ in range(4)]
        
        # Navigate to Back (index 3) and press Enter
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # To Skin
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # To Contact
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],  # To Back
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Select Back
            [],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            run_options(self.screen, self.menu_model, self.background_surf, 
                       self.background_rect, self.fonts, self.settings_model, self.mock_sound_manager)
        
        print("✅ Back button returns to menu")

if __name__ == '__main__':
    unittest.main()
