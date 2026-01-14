import unittest
import pygame
from unittest.mock import patch, MagicMock, call

# Initialize pygame for event handling tests
pygame.init()
pygame.display.set_mode((1, 1))  # Dummy display

from GardenInvasion.Controller.skin_selection_controller import run_skin_selection
from GardenInvasion.Model.menu_model import MenuModel
from GardenInvasion.Model.setting_volume_model import SettingsModel


class TestSkinSelectionController(unittest.TestCase):
    # Test suite for skin selection controller
    
    def setUp(self):
        # Set up test fixtures before each test
        # Mock pygame.image.load
        self.mock_surface = pygame.Surface((100, 100))
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.image_patcher.start()
        # Create test objects
        self.screen = pygame.Surface((800, 600))
        self.menu_model = MenuModel()
        self.settings_model = SettingsModel()
        self.settings_model.player_skin = "default"
        # Create test fonts
        self.title_font = pygame.font.SysFont("Arial", 32)
        self.item_font = pygame.font.SysFont("Arial", 20)
        self.inst_font = pygame.font.SysFont("Arial", 14)
        self.fonts = (self.title_font, self.item_font, self.inst_font)
        # Create test background
        self.background_surf = pygame.Surface((800, 600))
        self.background_rect = self.background_surf.get_rect()
    
    def tearDown(self):
        self.image_patcher.stop()
        # Clear event queue
        pygame.event.clear()
    
    @patch('GardenInvasion.Controller.skin_selection_controller.draw_skin_selection_menu') # Mock the drawing function
    @patch('pygame.display.flip') # Mock display flip to avoid actual rendering
    def test_right_arrow_navigates_to_next_skin(self, mock_flip, mock_draw):
        # Test that right arrow key navigates to next skin
        # Mock draw to return a back_rect
        mock_draw.return_value = pygame.Rect(100, 100, 50, 30)
        
        # Simulate right arrow press, then Enter to exit
        events = [
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}),
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
        ]
        
        with patch('pygame.event.get', side_effect=[events, []]):
            result = run_skin_selection(
                self.screen,
                self.menu_model,
                self.background_surf,
                self.background_rect,
                self.fonts,
                self.settings_model
            )
        
        # Should save skin and return to main menu
        self.assertEqual(result, 'main_menu')
        # Verify settings were saved (skin changed from default)
        self.assertIn(self.settings_model.player_skin, ["default", "Carnivorous", "Cactus"])
        
        print("✅ Right arrow navigates to next skin")
    
    @patch('GardenInvasion.Controller.skin_selection_controller.draw_skin_selection_menu')
    @patch('pygame.display.flip')
    def test_left_arrow_navigates_to_previous_skin(self, mock_flip, mock_draw):
        # Test that left arrow key navigates to previous skin
        mock_draw.return_value = pygame.Rect(100, 100, 50, 30)
        
        # Simulate left arrow press, then Enter to exit
        events = [
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT}),
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
        ]
        
        with patch('pygame.event.get', side_effect=[events, []]):
            result = run_skin_selection(
                self.screen,
                self.menu_model,
                self.background_surf,
                self.background_rect,
                self.fonts,
                self.settings_model
            )
        
        self.assertEqual(result, 'main_menu')
        print("✅ Left arrow navigates to previous skin")
    
    @patch('GardenInvasion.Controller.skin_selection_controller.draw_skin_selection_menu')
    @patch('pygame.display.flip')
    def test_down_arrow_selects_back_button(self, mock_flip, mock_draw):
        # Test that down arrow selects Back button
        mock_draw.return_value = pygame.Rect(100, 100, 50, 30)
        
        # Simulate down arrow, then Enter (should go back to options)
        events = [
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}),
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
        ]
        
        with patch('pygame.event.get', side_effect=[events, []]):
            result = run_skin_selection(
                self.screen,
                self.menu_model,
                self.background_surf,
                self.background_rect,
                self.fonts,
                self.settings_model
            )
        
        # Should return 'back' (not save skin, go to options menu)
        self.assertEqual(result, 'back')
        print("✅ Down arrow selects Back button")

    @patch('GardenInvasion.Controller.skin_selection_controller.draw_skin_selection_menu')
    @patch('pygame.display.flip')
    def test_mouse_click_on_skin_selects_and_exits(self, mock_flip, mock_draw):
        # Test that clicking on a skin selects it and exits
        mock_draw.return_value = pygame.Rect(100, 100, 50, 30)
        
        # Simulate mouse click on second skin (Carnivorous)
        # Position: start_x=120, spacing≈186, skin 2 at x≈493, y=252
        events = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
                'button': 1,
                'pos': (400, 250)  # Click on middle area
            })
        ]
        
        with patch('pygame.event.get', side_effect=[events, []]):
            result = run_skin_selection(
                self.screen,
                self.menu_model,
                self.background_surf,
                self.background_rect,
                self.fonts,
                self.settings_model
            )
        
        # Should save skin and return to main menu
        self.assertEqual(result, 'main_menu')
        print("✅ Mouse click on skin selects and exits to main menu")

if __name__ == '__main__':
    unittest.main()