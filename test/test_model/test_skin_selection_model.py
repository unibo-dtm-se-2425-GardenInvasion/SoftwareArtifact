import unittest
import pygame
from unittest.mock import patch, MagicMock
from pathlib import Path

from GardenInvasion.Model.skin_selection_model import SkinOption, SkinSelectionModel
pygame.init()

class TestSkinOption(unittest.TestCase):
    def setUp(self):
        # Create a mock surface to simulate a loaded image
        self.mock_surface = pygame.Surface((100, 100))
        self.mock_surface.fill((255, 0, 0))  # Red color for visibility
    
    def test_skin_option_initialization(self):
        # Test that SkinOption initializes with correct attributes
        with patch('pygame.image.load', return_value=self.mock_surface):
            skin = SkinOption(
                skin_id="test_skin",
                display_name="Test Skin",
                sprite_path="fake/path/test.png"
            )
        
        # Verify all attributes are set correctly
        self.assertEqual(skin.skin_id, "test_skin")
        self.assertEqual(skin.display_name, "Test Skin")
        self.assertEqual(skin.sprite_path, "fake/path/test.png")
        self.assertEqual(skin.preview_path, "fake/path/test.png")  # Should default to sprite_path
        
        print("✅ SkinOption initializes with correct attributes")
    
    def test_skin_option_preview_image_loaded_and_scaled(self):
        # Test that preview image is loaded and scaled to 80x80
        with patch('pygame.image.load', return_value=self.mock_surface):
            skin = SkinOption(
                skin_id="test_skin",
                display_name="Test Skin",
                sprite_path="fake/path/test.png"
            )
        # Verify preview image exists and is scaled correctly
        self.assertIsNotNone(skin.preview_image)
        self.assertIsInstance(skin.preview_image, pygame.Surface)
        self.assertEqual(skin.preview_image.get_size(), (80, 80))
        
        print("✅ Preview image loaded and scaled to 80x80")
    
    def test_skin_option_handles_missing_image(self):
        #Test that SkinOption creates placeholder when image fails to load
        # Simulate pygame.error when loading image
        with patch('pygame.image.load', side_effect=pygame.error("File not found")):
            skin = SkinOption(
                skin_id="test_skin",
                display_name="Test Skin",
                sprite_path="fake/path/missing.png"
            )
        
        # Verify placeholder was created
        self.assertIsNotNone(skin.preview_image)
        self.assertEqual(skin.preview_image.get_size(), (80, 80))
        # Check that it's a green placeholder (100, 200, 100)
        color = skin.preview_image.get_at((40, 40))  # Check center pixel
        self.assertEqual(color[:3], (100, 200, 100))
        
        print("✅ SkinOption creates green placeholder for missing images")


class TestSkinSelectionModel(unittest.TestCase):
    def setUp(self):
        # Mock pygame.image.load to avoid file I/O
        self.mock_surface = pygame.Surface((100, 100))
        self.patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.patcher.start()
        
        # Create a fresh model for each test
        self.model = SkinSelectionModel()
    
    def tearDown(self):
        """Clean up after each test"""
        self.patcher.stop()
    
    def test_model_initialization(self):
        """Test that SkinSelectionModel initializes with correct defaults"""
        self.assertIsInstance(self.model.available_skins, list)
        self.assertGreater(len(self.model.available_skins), 0)  # Should have at least 1 skin
        self.assertEqual(self.model.selected_index, 0)  # Should start at first skin
        self.assertEqual(self.model.current_skin_id, "default")
        self.assertFalse(self.model.back_button_selected)  # Should start in skin selection mode
        
        print("✅ SkinSelectionModel initializes with correct defaults")
    
    def test_get_selected_skin(self):
        # Test that get_selected_skin returns the correct skin
        selected_skin = self.model.get_selected_skin()
        
        # Should return the skin at selected_index
        self.assertEqual(selected_skin, self.model.available_skins[self.model.selected_index])
        self.assertEqual(selected_skin.skin_id, "default")  # First skin is default
        
        print("✅ get_selected_skin returns correct skin")
    
    def test_select_next_skin(self):
        # Test that select_next_skin moves forward through skins
        # Start at index 0 (default)
        self.assertEqual(self.model.selected_index, 0)
        
        # Move to next skin (index 1)
        self.model.select_next_skin()
        self.assertEqual(self.model.selected_index, 1)
        self.assertEqual(self.model.current_skin_id, self.model.available_skins[1].skin_id)
        # Move to next skin (index 2)
        self.model.select_next_skin()
        self.assertEqual(self.model.selected_index, 2)
        
        print("✅ select_next_skin moves forward through skins")

    def test_select_previous_skin(self):
        # Test that select_previous_skin moves backward through skins
        # Start at index 2
        self.model.selected_index = 2
        self.model.current_skin_id = self.model.available_skins[2].skin_id
        
        # Move to previous skin (index 1)
        self.model.select_previous_skin()
        self.assertEqual(self.model.selected_index, 1)
        # Move to previous skin (index 0)
        self.model.select_previous_skin()
        self.assertEqual(self.model.selected_index, 0)
        
        print("✅ select_previous_skin moves backward through skins")

    def test_navigation_disabled_when_back_button_selected(self):
        # Test that skin navigation is disabled when Back button is selected
        # Select Back button
        self.model.select_back_button()
        self.assertTrue(self.model.back_button_selected)
        
        # Try to navigate (should not change selected_index)
        original_index = self.model.selected_index
        self.model.select_next_skin()
        self.assertEqual(self.model.selected_index, original_index)
        
        self.model.select_previous_skin()
        self.assertEqual(self.model.selected_index, original_index)
        
        print("✅ Skin navigation disabled when Back button selected")
    
    def test_back_button_selection_toggle(self):
        # Test selecting and deselecting Back button
        # Initially not selected
        self.assertFalse(self.model.back_button_selected)
        
        # Select Back button
        self.model.select_back_button()
        self.assertTrue(self.model.back_button_selected)
        
        # Deselect Back button
        self.model.deselect_back_button()
        self.assertFalse(self.model.back_button_selected)
        
        print("✅ Back button selection toggles correctly")

if __name__ == '__main__':
    unittest.main()
