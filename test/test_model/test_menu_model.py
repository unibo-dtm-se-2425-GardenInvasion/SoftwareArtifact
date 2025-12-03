import unittest
from unittest.mock import Mock, patch
import pygame
import os
from pathlib import Path
import tempfile
from my_project.Model.menu_model import MenuModel, BackgroundModel, load_background_keep_ratio


class TestMenuModel(unittest.TestCase):
    """Test suite for MenuModel class"""

    def test_initial_menu_items(self):
        # Create a new MenuModel instance
        model = MenuModel()
        expected_items = ["New Game", "Options"]
        self.assertEqual(model.menu_items, expected_items)
        # Verify menu_items contains the expected items
        print(f"✅ MenuModel initialized with correct menu items: {model.menu_items}")


class TestBackgroundModel(unittest.TestCase):
    """Test suite for BackgroundModel class"""

    @classmethod
    def setUpClass(cls):
        os.environ['SDL_VIDEODRIVER'] = 'dummy' # Set SDL to use dummy video driver (no window needed)
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        #Quit pygame after all tests
        pygame.quit()

    def setUp(self):
        """Set up test fixtures before each test"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        # Create a valid test image (1x1 pixel PNG)
        self.valid_image_path = Path(self.test_dir) / "test_image.png"
        # Create a minimal 10x10 surface for testing
        test_surface = pygame.Surface((10, 10))
        # Save it as a PNG file
        pygame.image.save(test_surface, str(self.valid_image_path))

    def tearDown(self):
        """Clean up after each test"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_background_loads_with_valid_path(self):
        #Test that BackgroundModel successfully loads with a valid image path
        
        # Create BackgroundModel with valid image path
        background = BackgroundModel(self.valid_image_path)
        # Verify surface and rect are not None
        self.assertIsNotNone(background.surface)
        self.assertIsNotNone(background.rect)
        print("✅ BackgroundModel loaded successfully with valid image path")

    def test_background_returns_none_with_missing_file(self):
        #Test that BackgroundModel handles missing file gracefully

        # Create a path to a file that definitely doesn't exist
        missing_path = Path("/absolutely/nonexistent/path/image.png")
        background = BackgroundModel(missing_path)
        # Verify both surface and rect are None
        self.assertIsNone(background.surface)
        self.assertIsNone(background.rect)
        print("✅ BackgroundModel handled missing file gracefully")


class TestLoadBackgroundKeepRatio(unittest.TestCase):
    """Test suite for load_background_keep_ratio function"""

    @classmethod
    def setUpClass(cls):
        """Initialize pygame once for all tests"""
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        #Quit pygame after all tests
        pygame.quit()

    def setUp(self):
        """Set up test fixtures before each test"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up after each test"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_returns_none_for_nonexistent_file(self):
        #Test that function returns (None, None) for nonexistent file
        
        nonexistent_path = Path(self.test_dir) / "does_not_exist.png"
        surface, rect = load_background_keep_ratio(nonexistent_path)
        # Verify both return values are None
        self.assertIsNone(surface)
        self.assertIsNone(rect)
        print("✅ load_background_keep_ratio returned (None, None) for nonexistent file")

if __name__ == '__main__':
    unittest.main()
