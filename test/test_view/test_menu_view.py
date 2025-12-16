import unittest
import pygame
import os
from GardenInvasion.View.menu_view import draw_menu, draw_pause_modal, get_pause_menu_button_rects, draw_modal
from GardenInvasion.Model.menu_model import MenuModel
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TestMenuView(unittest.TestCase):
    """Test suite for menu view rendering functions"""

    @classmethod
    def setUpClass(cls):
        #Initialize pygame once for all tests
        os.environ['SDL_VIDEODRIVER'] = 'dummy' # Use dummy video driver for headless testing
        pygame.init()
        cls.display = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

    @classmethod
    def tearDownClass(cls):
        #Quit pygame after all tests
        pygame.quit()

    def setUp(self):
        #Set up test fixtures before each test
        self.screen = self.display # Main display surface
        self.model = MenuModel()
        self.background_surf = pygame.Surface((SCREEN_HEIGHT, SCREEN_WIDTH)) # Mock background surface
        self.background_rect = self.background_surf.get_rect()
        self.fonts = (
            pygame.font.SysFont("Arial", 30),  # item_font
            pygame.font.SysFont("Arial", 16),  # inst_font
            pygame.font.SysFont("Arial", 72)   # title_font
        )

    def test_draw_menu_does_not_crash(self):
        """Test that draw_menu executes without raising exceptions"""
        try:
            draw_menu(self.screen, self.model, self.background_surf, self.background_rect, self.fonts)
            print("✅ draw_menu executed successfully without errors")
        except Exception as e:
            self.fail(f"❌ draw_menu raised an exception: {e}")

    def test_draw_menu_with_background_surface(self):
        """Test draw_menu renders correctly when background surface is provided"""
        label_rects = draw_menu(self.screen, self.model, self.background_surf, self.background_rect, self.fonts)
        # Should return a list of rects
        self.assertIsInstance(label_rects, list) # Check return type is list
        # Number of rects should match number of menu items
        self.assertEqual(len(label_rects), len(self.model.menu_items)) # Check correct number of rects
        print(f"✅ draw_menu returned {len(label_rects)} label rects as expected")

    def test_draw_pause_modal_does_not_crash(self):
        """Test that draw_pause_modal executes without exceptions"""
        try:
            draw_pause_modal(self.screen, selected_button=1) # Test with 'Resume' button selected
            print("✅ draw_pause_modal executed successfully")
        except Exception as e:
            self.fail(f"❌ draw_pause_modal raised an exception: {e}")

    def test_draw_pause_modal_renders_buttons(self):
        """Test that draw_pause_modal renders all button elements"""
        # Should execute successfully with different selected buttons
        for button_index in range(3):  # 0=Main Menu, 1=Resume, 2=Quit
            try:
                draw_pause_modal(self.screen, selected_button=button_index)
            except Exception as e:
                self.fail(f"❌ draw_pause_modal failed with selected_button={button_index}: {e}")
        print("✅ All 3 pause modal buttons rendered successfully")

    def test_draw_modal_does_not_crash(self):
        """Test that draw_modal executes without exceptions"""
        try:
            draw_modal(self.screen, selected_button=1) # Test with 'No' button selected
            print("✅ draw_modal executed successfully")
        except Exception as e:
            self.fail(f"❌ draw_modal raised an exception: {e}")

    def test_draw_modal_renders_message(self):
        """Test that draw_modal displays confirmation message"""
        # Should execute successfully with different button selections
        for button_index in range(2):  # 0=Yes, 1=No
            try:
                draw_modal(self.screen, selected_button=button_index)
            except Exception as e:
                self.fail(f"❌ draw_modal failed with selected_button={button_index}: {e}")
        print("✅ draw_modal rendered both button states successfully")

if __name__ == '__main__':
    unittest.main()
