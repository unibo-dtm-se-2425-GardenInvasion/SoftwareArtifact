import unittest
import pygame
from unittest.mock import patch, MagicMock
import sys

# Initialize pygame for event handling tests
pygame.init()
pygame.display.set_mode((1, 1))  # Dummy display

from GardenInvasion.Controller.options_controller import run_volume_menu
from GardenInvasion.Model.menu_model import MenuModel

class TestVolumeController(unittest.TestCase):
    # Test suite for volume submenu controller
    
    def setUp(self):
        # Set up test fixtures before each test
        self.mock_surface = pygame.Surface((100, 100))
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.image_patcher.start()
        
        self.screen = pygame.Surface((600, 600))
        self.menu_model = MenuModel()
        self.background_surf = pygame.Surface((600, 600))
        self.background_rect = self.background_surf.get_rect()
        
        self.title_font = pygame.font.SysFont("Arial", 72)
        self.item_font = pygame.font.SysFont("Arial", 30)
        self.inst_font = pygame.font.SysFont("Arial", 16)
        self.fonts = (self.item_font, self.inst_font, self.title_font)
    
    def tearDown(self):
        self.image_patcher.stop()
        pygame.event.clear()
    
    def create_event_generator(self, events_sequence):
        # Create an event generator that yields events then empty lists indefinitely
        def generator():
            for events in events_sequence:
                yield events
            # After all events, yield empty lists forever
            while True:
                yield []
        
        return generator()
    
    @patch('GardenInvasion.Controller.options_controller.draw_volume_menu')
    @patch('pygame.display.flip')
    @patch('pygame.time.Clock')
    def test_left_arrow_decreases_volume(self, mock_clock, mock_flip, mock_draw):
        # Test that left arrow decreases volume by 5
        mock_draw.return_value = pygame.Rect(0, 0, 60, 30) # Dummy rect
        mock_clock.return_value.tick.return_value = None
        
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],
            [],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            [],
        ]
        
        with patch('pygame.event.get', side_effect=self.create_event_generator(events_sequence)):
            final_volume = run_volume_menu(self.screen, self.menu_model, 
                                          self.background_surf, self.background_rect, 
                                          self.fonts, 50) # Start at volume 50
        
        self.assertEqual(final_volume, 45) # Expect volume to be 45
        print("✅ Left arrow decreases volume by 5")
    
    @patch('GardenInvasion.Controller.options_controller.draw_volume_menu')
    @patch('pygame.display.flip')
    @patch('pygame.time.Clock')
    def test_right_arrow_increases_volume(self, mock_clock, mock_flip, mock_draw):
        # Test that right arrow increases volume by 5

        mock_draw.return_value = pygame.Rect(0, 0, 60, 30)
        mock_clock.return_value.tick.return_value = None
        
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],
            [],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            [],
        ]
        
        with patch('pygame.event.get', side_effect=self.create_event_generator(events_sequence)):
            final_volume = run_volume_menu(self.screen, self.menu_model, 
                                          self.background_surf, self.background_rect, 
                                          self.fonts, 50)
        
        self.assertEqual(final_volume, 55)
        print("✅ Right arrow increases volume by 5")
    
    @patch('GardenInvasion.Controller.options_controller.draw_volume_menu')
    @patch('pygame.display.flip')
    @patch('pygame.time.Clock')
    def test_volume_minimum_limit(self, mock_clock, mock_flip, mock_draw):

        # Test that volume cannot go below 0
        mock_draw.return_value = pygame.Rect(0, 0, 60, 30)
        mock_clock.return_value.tick.return_value = None
        
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],
            [],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],
            [],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            [],
        ]
        
        with patch('pygame.event.get', side_effect=self.create_event_generator(events_sequence)):
            final_volume = run_volume_menu(self.screen, self.menu_model, 
                                          self.background_surf, self.background_rect, 
                                          self.fonts, 5)
        
        self.assertEqual(final_volume, 0)
        print("✅ Volume cannot go below 0")
    
    @patch('GardenInvasion.Controller.options_controller.draw_volume_menu')
    @patch('pygame.display.flip')
    @patch('pygame.time.Clock')
    def test_volume_maximum_limit(self, mock_clock, mock_flip, mock_draw):
        # Test that volume cannot exceed 100

        mock_draw.return_value = pygame.Rect(0, 0, 60, 30)
        mock_clock.return_value.tick.return_value = None
        
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],
            [],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],
            [],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            [],
        ]
        
        with patch('pygame.event.get', side_effect=self.create_event_generator(events_sequence)):
            final_volume = run_volume_menu(self.screen, self.menu_model, 
                                          self.background_surf, self.background_rect, 
                                          self.fonts, 95)
        
        self.assertEqual(final_volume, 100)
        print("✅ Volume cannot exceed 100")
    
    @patch('GardenInvasion.Controller.options_controller.draw_volume_menu')
    @patch('pygame.display.flip')
    @patch('pygame.time.Clock')
    def test_back_button_click_exits(self, mock_clock, mock_flip, mock_draw):
        # Test that clicking Back exits volume menu

        back_rect = pygame.Rect(270, 351, 60, 30)
        mock_draw.return_value = back_rect
        mock_clock.return_value.tick.return_value = None
        
        events_sequence = [
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (300, 365)})],
            [],
        ]
        
        with patch('pygame.event.get', side_effect=self.create_event_generator(events_sequence)):
            final_volume = run_volume_menu(self.screen, self.menu_model, 
                                          self.background_surf, self.background_rect, 
                                          self.fonts, 50)
        
        self.assertEqual(final_volume, 50)
        print("✅ Back button click exits volume menu")
    
    @patch('GardenInvasion.Controller.options_controller.show_confirm_quit')
    @patch('GardenInvasion.Controller.options_controller.draw_volume_menu')
    @patch('pygame.display.flip')
    @patch('pygame.time.Clock')
    def test_escape_shows_quit_confirmation(self, mock_clock, mock_flip, mock_draw, mock_quit):
        # Test that ESC shows quit confirmation
        
        mock_draw.return_value = pygame.Rect(0, 0, 60, 30)
        mock_clock.return_value.tick.return_value = None
        mock_quit.return_value = True
        
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})],
            [],
        ]
        
        # Mock sys.exit to raise SystemExit
        def mock_exit_func(*args):
            raise SystemExit()
        
        with patch('pygame.event.get', side_effect=self.create_event_generator(events_sequence)):
            with patch('pygame.quit'):
                with patch('sys.exit', side_effect=mock_exit_func):
                    with self.assertRaises(SystemExit):
                        run_volume_menu(self.screen, self.menu_model, 
                                      self.background_surf, self.background_rect, 
                                      self.fonts, 50)
        
        mock_quit.assert_called_once()
        print("✅ ESC shows quit confirmation in volume menu")

if __name__ == '__main__':
    unittest.main()
