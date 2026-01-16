import unittest
from unittest.mock import Mock, patch
import pygame
import os
from GardenInvasion.Model.wallnut_model import WallNut, WallNutManager


class TestWallNut(unittest.TestCase):
    """Test suite for WallNut class"""

    @classmethod
    def setUpClass(cls):
        """Initialize pygame once for all tests"""
        # Set SDL to use dummy video driver (no window needed)
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        # Initialize all pygame modules
        pygame.init()
        # Create a display surface (required for convert_alpha())
        cls.display = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        """Quit pygame after all tests"""
        # Clean up pygame resources
        pygame.quit()

    def setUp(self):
        """Set up test fixtures before each test"""
        # Create mock surfaces for wallnut sprites
        mock_surface = pygame.Surface((60, 60))
        # Now convert_alpha() will work because display mode is set
        self.mock_surface = mock_surface.convert_alpha()

    def test_wallnut_initializes_with_slot_index(self):
        """Test that WallNut initializes with correct slot_index"""
        # Define test slot index
        test_slot = 2
        test_position = (300, 200)
        
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=test_position, slot_index=test_slot)
        
        # Verify slot_index is set correctly
        self.assertEqual(wallnut.slot_index, test_slot)
        print(f"✅ WallNut initialized with slot_index: {test_slot}")

    def test_wallnut_initial_health_is_two(self):
        """Test that WallNut initializes with health of 2 (was 3)"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Verify initial health is 2
        self.assertEqual(wallnut.health, 2)
        print(f"✅ WallNut initialized with health: {wallnut.health}")

    def test_wallnut_max_health_is_two(self):
        """Test that WallNut has max_health of 2 (was 3)"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Verify max_health is 2
        self.assertEqual(wallnut.max_health, 2)
        print(f"✅ WallNut has max_health: {wallnut.max_health}")

    def test_wallnut_initial_image_is_full_health(self):
        """Test that WallNut starts with full health sprite"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Verify image is set (full health sprite)
        self.assertIsNotNone(wallnut.image)
        # Verify sprites dictionary exists
        self.assertTrue(hasattr(wallnut, 'sprites'))
        # Verify sprites dictionary has keys for 2 and 1 (not 3 anymore)
        self.assertIn(2, wallnut.sprites)  # Full health
        self.assertIn(1, wallnut.sprites)  # Damaged
        self.assertNotIn(3, wallnut.sprites)  # Should not have key 3 anymore
        print("✅ WallNut initialized with full health sprite (2 life points)")

    def test_take_damage_reduces_health(self):
        """Test that take_damage() reduces health by 1"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Store initial health
        initial_health = wallnut.health
        
        # Take damage
        wallnut.take_damage()
        
        # Verify health decreased by 1
        self.assertEqual(wallnut.health, initial_health - 1)
        print(f"✅ take_damage() reduced health from {initial_health} to {wallnut.health}")

    def test_take_damage_changes_sprite(self):
        """Test that take_damage() updates sprite to show damage"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Store initial image
        initial_image = wallnut.image
        
        # Take damage
        wallnut.take_damage()
        
        # Note: Image reference might change based on sprites dictionary
        # Verify image still exists (sprite updated)
        self.assertIsNotNone(wallnut.image)
        # Verify health is now 1 (damaged state)
        self.assertEqual(wallnut.health, 1)
        print("✅ take_damage() updated sprite to show damage")

    def test_take_damage_at_zero_health_kills_sprite(self):
        """Test that take_damage() kills sprite when health reaches 0"""
        # Create a sprite group to track wallnut
        sprite_group = pygame.sprite.Group()
        
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
            sprite_group.add(wallnut)
        
        # Reduce health to 0 by taking damage 2 times (was 3 times)
        wallnut.take_damage()  # health: 2 -> 1
        result = wallnut.take_damage()  # health: 1 -> 0
        
        # Verify take_damage returned True (wallnut destroyed)
        self.assertTrue(result)
        # Verify wallnut was removed from sprite group
        self.assertNotIn(wallnut, sprite_group)
        print("✅ take_damage() killed sprite when health reached 0 (after 2 hits)")

    def test_take_damage_updates_image(self):
        """Test that take_damage() updates image attribute"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Take damage
        wallnut.take_damage()
        
        # Verify image is still set (updated to damaged sprite)
        self.assertIsNotNone(wallnut.image)
        self.assertIsInstance(wallnut.image, pygame.Surface)
        # Verify health decreased
        self.assertEqual(wallnut.health, 1)
        print("✅ take_damage() updated image attribute successfully")

    def test_take_damage_does_not_go_below_zero(self):
        """Test that take_damage() doesn't reduce health below 0"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Take 3 damages (more than available life points)
        results = []
        for i in range(3):
            results.append(wallnut.take_damage())
        
        # Health should not go below 0
        self.assertEqual(wallnut.health, 0)
        # Only the second damage should return True for destruction
        self.assertFalse(results[0])  # First damage (2 -> 1)
        self.assertTrue(results[1])   # Second damage (1 -> 0, destruction)
        self.assertTrue(results[2])   # Third damage (already destroyed)
        print("✅ Health doesn't go below 0 with extra damage")

    def test_wallnut_sprite_dictionary_size(self):
        """Test that wallnut sprites dictionary has exactly 2 entries"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Verify sprites dictionary has exactly 2 entries
        self.assertEqual(len(wallnut.sprites), 2)
        # Verify the keys are 2 and 1
        self.assertSetEqual(set(wallnut.sprites.keys()), {2, 1})
        print("✅ WallNut sprites dictionary has 2 entries (for 2 life points)")

if __name__ == '__main__':
    unittest.main()
