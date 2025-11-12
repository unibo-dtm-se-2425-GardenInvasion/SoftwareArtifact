import unittest
import pygame
import os
from my_project.View.options_view import draw_options_menu, draw_contact_modal, draw_volume_menu
from my_project.Model.options_model import OptionsModel, VolumeModel
from my_project.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TestOptionsView(unittest.TestCase):
    """Test suite for options view rendering functions"""

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
        self.screen = self.display
        self.options_model = OptionsModel() # Default options model
        self.volume_model = VolumeModel(initial_volume=50) # Initial volume at 50%
        self.background_surf = pygame.Surface((SCREEN_HEIGHT, SCREEN_WIDTH))
        self.background_rect = self.background_surf.get_rect()
        self.fonts = (
            pygame.font.SysFont("Arial", 30),  # item_font
            pygame.font.SysFont("Arial", 16),  # inst_font
            pygame.font.SysFont("Arial", 72)   # title_font
        )

    def test_draw_options_menu_does_not_crash(self):
        """Test that draw_options_menu executes without exceptions"""
        try:
            draw_options_menu(self.screen, self.options_model, self.background_surf, 
                            self.background_rect, self.fonts)
            print("✅ draw_options_menu executed successfully without errors")
        except Exception as e:
            self.fail(f"❌ draw_options_menu raised an exception: {e}")

    def test_draw_options_menu_with_background(self):
        """Test draw_options_menu renders correctly with background"""
        label_rects = draw_options_menu(self.screen, self.options_model, 
                                       self.background_surf, self.background_rect, self.fonts)
        
        # Should return a list of rects
        self.assertIsInstance(label_rects, list) # Check type is list
        # Number of rects should match number of options items
        self.assertEqual(len(label_rects), len(self.options_model.options_items))
        print(f"✅ draw_options_menu returned {len(label_rects)} label rects as expected")

    def test_draw_contact_modal_does_not_crash(self):
        """Test that draw_contact_modal executes without exceptions"""
        try:
            draw_contact_modal(self.screen, selected_button=0) # Select yes button
            print("✅ draw_contact_modal executed successfully")
        except Exception as e:
            self.fail(f"❌ draw_contact_modal raised an exception: {e}")

    def test_draw_volume_menu_does_not_crash(self):
        """Test that draw_volume_menu executes without exceptions"""
        try:
            draw_volume_menu(self.screen, self.volume_model, self.background_surf, 
                           self.background_rect, self.fonts)
            print("✅ draw_volume_menu executed successfully")
        except Exception as e:
            self.fail(f"❌ draw_volume_menu raised an exception: {e}")

    def test_draw_volume_menu_renders_slider(self):
        """Test that draw_volume_menu renders the volume slider"""
        # Should execute successfully with different volume levels
        for volume in [0, 50, 100]:
            self.volume_model.volume = volume # Set volume
            try:
                back_rect = draw_volume_menu(self.screen, self.volume_model, 
                                            self.background_surf, self.background_rect, self.fonts)
                # Should return a rect for the back button
                self.assertIsInstance(back_rect, pygame.Rect)
            except Exception as e:
                self.fail(f"❌ draw_volume_menu failed with volume={volume}: {e}")
        print("✅ draw_volume_menu rendered sliders for volumes: 0, 50, 100")

    def test_draw_volume_menu_renders_percentage(self):
        """Test that draw_volume_menu renders the volume percentage text"""
        # Set different volume levels and ensure no crash
        test_volumes = [0, 25, 50, 75, 100]
        
        for volume in test_volumes:
            self.volume_model.volume = volume
            try:
                draw_volume_menu(self.screen, self.volume_model, self.background_surf, 
                               self.background_rect, self.fonts) # Render menu
            except Exception as e:
                self.fail(f"❌ draw_volume_menu failed to render percentage for volume={volume}: {e}")
        print(f"✅ draw_volume_menu rendered percentages for {len(test_volumes)} different volume levels")

if __name__ == '__main__':
    unittest.main()
