import unittest
import pygame
from unittest.mock import patch, MagicMock, call
import sys

pygame.init()
pygame.display.set_mode((1, 1))

from GardenInvasion.Controller.NewGame_controller import show_pause_menu, run_game
from GardenInvasion.Model.menu_model import MenuModel
from GardenInvasion.Model.setting_volume_model import SettingsModel

class TestNewGameController(unittest.TestCase):
    # Test suite for NewGame controller

    def setUp(self):
        # Set up test fixtures
        self.mock_surface = pygame.Surface((100, 100))
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.image_patcher.start()

        self.screen = pygame.Surface((600, 600))
        self.menu_model = MenuModel()
        self.settings_model = SettingsModel()

    def tearDown(self):
        self.image_patcher.stop()
        pygame.event.clear()

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_escape_opens_pause_menu(self, mock_flip, mock_draw):
        # Test that ESC shows pause modal

        # Simulate ESC key, then Resume
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Resume
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'resume')
        print("✅ ESC opens pause menu")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_resume_continues_game(self, mock_flip, mock_draw):
        # Test that Resume returns to gameplay

        # Select Resume (default selection is 1)
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'resume')
        print("✅ Resume continues gameplay")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_main_menu_exits(self, mock_flip, mock_draw):
        # Test that Main Menu exits game loop

        # Navigate left to Main Menu (index 0) and select
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'menu')
        print("✅ Main Menu exits game loop")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_quit_exits_application(self, mock_flip, mock_draw):
        # Test that Quit closes game

        # Navigate right to Quit (index 2) and select
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'quit')
        print("✅ Quit exits application")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_left_right_navigation_in_pause(self, mock_flip, mock_draw):
        # Test navigating pause menu buttons with LEFT/RIGHT

        # Navigate left, then right, then select
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],   # To Main Menu
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],  # To Resume
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],  # To Quit
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],   # Back to Resume
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})], # Select Resume
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'resume')
        print("✅ LEFT/RIGHT navigation works in pause menu")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('GardenInvasion.Controller.NewGame_controller.get_pause_menu_button_rects')
    @patch('pygame.display.flip')
    def test_mouse_click_resume(self, mock_flip, mock_rects, mock_draw):
        # Test clicking Resume button

        # Mock button rects
        resume_rect = pygame.Rect(230, 300, 140, 50)
        mock_rects.return_value = (pygame.Rect(0, 0, 140, 50), resume_rect, pygame.Rect(0, 0, 140, 50))

        # Simulate mouse motion over Resume, then click
        events_sequence = [
            [pygame.event.Event(pygame.MOUSEMOTION, {'pos': (300, 325)})],
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (300, 325)})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'resume')
        print("✅ Mouse click on Resume works")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('GardenInvasion.Controller.NewGame_controller.get_pause_menu_button_rects')
    @patch('pygame.display.flip')
    def test_mouse_click_quit(self, mock_flip, mock_rects, mock_draw):
        # Test clicking Quit button
        
        # Mock button rects
        quit_rect = pygame.Rect(390, 300, 140, 50)
        mock_rects.return_value = (pygame.Rect(0, 0, 140, 50), pygame.Rect(0, 0, 140, 50), quit_rect)

        # Simulate mouse motion over Quit, then click
        events_sequence = [
            [pygame.event.Event(pygame.MOUSEMOTION, {'pos': (460, 325)})],
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (460, 325)})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'quit')
        print("✅ Mouse click on Quit works")

if __name__ == '__main__':
    unittest.main()