import unittest
import pygame
import os
from GardenInvasion.View.victory_view import draw_victory_screen
from GardenInvasion.Model.victory_model import VictoryModel
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TestVictoryView(unittest.TestCase):

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
        self.victory_model = VictoryModel()

    def test_draw_victory_screen_does_not_crash(self):
        # Test that draw_victory_screen executes without exceptions
        try:
            play_again_rect, menu_rect = draw_victory_screen(
                self.screen, 
                self.victory_model
            )
            print("✅ draw_victory_screen executed successfully")
        except Exception as e:
            self.fail(f"❌ draw_victory_screen raised an exception: {e}")

    def test_draw_victory_screen_with_play_again_selected(self):
        # Test rendering with 'Play Again' button selected

        self.victory_model.selected_index = 0
        try:
            play_again_rect, menu_rect = draw_victory_screen(
                self.screen, 
                self.victory_model
            )
            self.assertEqual(self.victory_model.get_selected_option(), "Play Again")
            print("✅ Victory screen renders correctly with 'Play Again' selected")
        except Exception as e:
            self.fail(f"❌ Failed with 'Play Again' selected: {e}")

    def test_draw_victory_screen_with_main_menu_selected(self):
        # Test rendering with 'Main Menu' button selected

        self.victory_model.selected_index = 1
        try:
            play_again_rect, menu_rect = draw_victory_screen(
                self.screen, 
                self.victory_model
            )
            self.assertEqual(self.victory_model.get_selected_option(), "Main Menu")
            print("✅ Victory screen renders correctly with 'Main Menu' selected")
        except Exception as e:
            self.fail(f"❌ Failed with 'Main Menu' selected: {e}")

    def test_button_rects_positioned_correctly(self):
        # Test that buttons are positioned within screen bounds

        play_again_rect, menu_rect = draw_victory_screen(
            self.screen, 
            self.victory_model
        )
        
        # Check buttons are within screen bounds
        self.assertGreaterEqual(play_again_rect.left, 0)
        self.assertLessEqual(play_again_rect.right, SCREEN_WIDTH)
        self.assertGreaterEqual(menu_rect.left, 0)
        self.assertLessEqual(menu_rect.right, SCREEN_WIDTH)
        print("✅ Buttons positioned within screen bounds")

if __name__ == '__main__':
    unittest.main()
