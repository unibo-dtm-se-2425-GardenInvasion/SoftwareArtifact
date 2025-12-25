import unittest
import pygame
from unittest.mock import patch, MagicMock
import sys

# Initialize pygame for event handling tests
pygame.init()
pygame.display.set_mode((1, 1))  # Dummy display

from GardenInvasion.Controller.menu_controller import main_menu_loop
from GardenInvasion.Model.menu_model import MenuModel

class TestMenuController(unittest.TestCase):
    # Test suite for menu controller
    
    def setUp(self):
        # Set up test fixtures before each test
        # Mock pygame.image.load
        self.mock_surface = pygame.Surface((100, 100))
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.image_patcher.start()
        
        # Create test objects
        self.screen = pygame.Surface((600, 600))
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
    
    @patch('GardenInvasion.Controller.menu_controller.run_game') # Mock run_game function
    @patch('GardenInvasion.Controller.menu_controller._global_quit', return_value=False) # Mock global quit check
    @patch('GardenInvasion.Controller.menu_controller.draw_menu') # Mock draw_menu function
    @patch('pygame.display.flip') # Mock pygame display flip
    def test_enter_key_starts_new_game(self, mock_flip, mock_draw, mock_global_quit, mock_run_game):
        # Test that Enter key starts New Game when selected

        # After run_game is called, trigger quit to exit the loop
        def run_game_side_effect(*args): 
            mock_global_quit.return_value = True # Exit loop after starting game
        
        mock_run_game.side_effect = run_game_side_effect # Simulate run_game side effect
        
        # Simulate Enter key press on "New Game" (index 0)
        events_sequence = [ # Sequence of event lists to simulate
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})], # Press Enter
            [pygame.event.Event(pygame.QUIT)], # Quit event to exit loop
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            main_menu_loop(self.screen, self.background_surf, self.background_rect, self.fonts)
        
        # Verify run_game was called
        mock_run_game.assert_called_once()
        print("✅ Enter key starts new game")
    
    @patch('GardenInvasion.Controller.menu_controller.run_options')
    @patch('GardenInvasion.Controller.menu_controller._global_quit', return_value=False)
    @patch('GardenInvasion.Controller.menu_controller.draw_menu')
    @patch('pygame.display.flip')
    def test_space_key_opens_options(self, mock_flip, mock_draw, mock_global_quit, mock_run_options):
        # Test that Space key opens Options when selected

        # After run_options is called, trigger quit to exit the loop
        def run_options_side_effect(*args):
            mock_global_quit.return_value = True
        
        mock_run_options.side_effect = run_options_side_effect
        
        # Navigate down to Options (index 1), then press Space
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})],
            [pygame.event.Event(pygame.QUIT)],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            main_menu_loop(self.screen, self.background_surf, self.background_rect, self.fonts)
        
        # Verify run_options was called
        mock_run_options.assert_called_once()
        print("✅ Space key opens options")

    @patch('GardenInvasion.Controller.menu_controller.run_game')
    @patch('GardenInvasion.Controller.menu_controller._global_quit', return_value=False)
    @patch('GardenInvasion.Controller.menu_controller.draw_menu')
    @patch('pygame.display.flip')
    def test_mouse_click_on_new_game(self, mock_flip, mock_draw, mock_global_quit, mock_run_game):
        # Test clicking New Game launches the game

        # After run_game is called, trigger quit to exit the loop
        def run_game_side_effect(*args):
            mock_global_quit.return_value = True
        
        mock_run_game.side_effect = run_game_side_effect
        
        # Click on New Game area (y around 240)
        events_sequence = [
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (300, 240)})],
            [pygame.event.Event(pygame.QUIT)],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            main_menu_loop(self.screen, self.background_surf, self.background_rect, self.fonts)
        
        mock_run_game.assert_called_once()
        print("✅ Mouse click on New Game launches game")
    
    @patch('GardenInvasion.Controller.menu_controller.run_options')
    @patch('GardenInvasion.Controller.menu_controller._global_quit', return_value=False)
    @patch('GardenInvasion.Controller.menu_controller.draw_menu')
    @patch('pygame.display.flip')
    def test_mouse_click_on_options(self, mock_flip, mock_draw, mock_global_quit, mock_run_options):
        # Test clicking Options opens options menu

        # After run_options is called, trigger quit to exit the loop
        def run_options_side_effect(*args):
            mock_global_quit.return_value = True
        
        mock_run_options.side_effect = run_options_side_effect
        
        # Click on Options area (y around 300)
        events_sequence = [
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (300, 300)})],
            [pygame.event.Event(pygame.QUIT)],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            main_menu_loop(self.screen, self.background_surf, self.background_rect, self.fonts)
        
        mock_run_options.assert_called_once()
        print("✅ Mouse click on Options opens options menu")
    
    @patch('GardenInvasion.Controller.menu_controller._global_quit')
    @patch('GardenInvasion.Controller.menu_controller.draw_menu')
    @patch('pygame.display.flip')
    def test_escape_shows_quit_confirmation(self, mock_flip, mock_draw, mock_global_quit):
        # Test that ESC triggers quit confirmation modal

        # First call returns True (user confirms quit)
        mock_global_quit.return_value = True
        
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})],
            []
        ]
        
        with patch('pygame.event.get', side_effect=events_sequence):
            main_menu_loop(self.screen, self.background_surf, self.background_rect, self.fonts)
        
        mock_global_quit.assert_called_once()
        print("✅ ESC shows quit confirmation modal")

if __name__ == '__main__':
    unittest.main()
