import unittest
from GardenInvasion.Model.game_over_model import GameOverModel

class TestGameOverModel(unittest.TestCase):

    def setUp(self):
        self.game_over_model = GameOverModel()

    def test_initialization(self):
        # Test that GameOverModel initializes with correct default values
        self.assertEqual(self.game_over_model.options, ["Start Again", "Main Menu"])
        self.assertEqual(self.game_over_model.selected_index, 0)
        print("GameOverModel initialized correctly")

    def test_select_next(self):
        # Test moving selection to the right

        # Start at index 0
        self.assertEqual(self.game_over_model.selected_index, 0)
        # Move right to index 1
        self.game_over_model.select_next()
        self.assertEqual(self.game_over_model.selected_index, 1)

        # Move right again - should wrap to index 0
        self.game_over_model.select_next()
        self.assertEqual(self.game_over_model.selected_index, 0)
        print("select_next works correctly with wrapping")

    def test_select_previous(self):
        # Test moving selection to the left

        # Start at index 0
        self.assertEqual(self.game_over_model.selected_index, 0)
        # Move left - should wrap to index 1
        self.game_over_model.select_previous()
        self.assertEqual(self.game_over_model.selected_index, 1)

        # Move left to index 0
        self.game_over_model.select_previous()
        self.assertEqual(self.game_over_model.selected_index, 0)
        print("select_previous works correctly with wrapping")

    def test_get_selected_option_start_again(self):
        # Test getting 'Start Again' option text

        self.game_over_model.selected_index = 0
        self.assertEqual(self.game_over_model.get_selected_option(), "Start Again")
        print("get_selected_option returns 'Start Again' at index 0")

    def test_get_selected_option_main_menu(self):
        # Test getting 'Main Menu' option text

        self.game_over_model.selected_index = 1
        self.assertEqual(self.game_over_model.get_selected_option(), "Main Menu")
        print("get_selected_option returns 'Main Menu' at index 1")

    def test_reset(self):
        # Test that reset() returns selection to the first option

        self.game_over_model.selected_index = 1
        self.game_over_model.reset()
        self.assertEqual(self.game_over_model.selected_index, 0)
        print("reset() returns selection to index 0")

if __name__ == '__main__':
    unittest.main()
