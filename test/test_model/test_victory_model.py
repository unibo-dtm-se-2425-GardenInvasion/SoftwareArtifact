import unittest
from GardenInvasion.Model.victory_model import VictoryModel

class TestVictoryModel(unittest.TestCase):

    def setUp(self):
        self.victory_model = VictoryModel()

    def test_initialization(self):
        # Test that VictoryModel initializes with correct default values
        self.assertEqual(self.victory_model.options, ["Play Again", "Main Menu"])
        self.assertEqual(self.victory_model.selected_index, 0)
        print("✅ VictoryModel initialized correctly")

    def test_select_next(self):
        # Test moving selection to the right

        # Start at index 0
        self.assertEqual(self.victory_model.selected_index, 0)
        # Move right to index 1
        self.victory_model.select_next()
        self.assertEqual(self.victory_model.selected_index, 1)
        
        # Move right again - should wrap to index 0
        self.victory_model.select_next()
        self.assertEqual(self.victory_model.selected_index, 0)
        print("✅ select_next works correctly with wrapping")

    def test_select_previous(self):
        # Test moving selection to the left

        # Start at index 0
        self.assertEqual(self.victory_model.selected_index, 0)
        # Move left - should wrap to index 1
        self.victory_model.select_previous()
        self.assertEqual(self.victory_model.selected_index, 1)
        
        # Move left to index 0
        self.victory_model.select_previous()
        self.assertEqual(self.victory_model.selected_index, 0)
        print("✅ select_previous works correctly with wrapping")

    def test_get_selected_option_play_again(self):
        # Test getting 'Play Again' option text

        self.victory_model.selected_index = 0
        self.assertEqual(self.victory_model.get_selected_option(), "Play Again")
        print("✅ get_selected_option returns 'Play Again' at index 0")

    def test_get_selected_option_main_menu(self):
        # Test getting 'Main Menu' option text

        self.victory_model.selected_index = 1
        self.assertEqual(self.victory_model.get_selected_option(), "Main Menu")
        print("✅ get_selected_option returns 'Main Menu' at index 1")

if __name__ == '__main__':
    unittest.main()
