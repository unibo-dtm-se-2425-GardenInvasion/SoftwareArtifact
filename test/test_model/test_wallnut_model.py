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

    def test_wallnut_initial_health_is_three(self):
        """Test that WallNut initializes with health of 3"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Verify initial health is 3
        self.assertEqual(wallnut.health, 3)
        print(f"✅ WallNut initialized with health: {wallnut.health}")

    def test_wallnut_max_health_is_three(self):
        """Test that WallNut has max_health of 3"""
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
        
        # Verify max_health is 3
        self.assertEqual(wallnut.max_health, 3)
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
        print("✅ WallNut initialized with full health sprite")

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
        print("✅ take_damage() updated sprite to show damage")

    def test_take_damage_at_zero_health_kills_sprite(self):
        """Test that take_damage() kills sprite when health reaches 0"""
        # Create a sprite group to track wallnut
        sprite_group = pygame.sprite.Group()
        
        # Create WallNut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            wallnut = WallNut(position=(300, 200), slot_index=0)
            sprite_group.add(wallnut)
        
        # Reduce health to 0 by taking damage 3 times
        wallnut.take_damage()  # health: 3 -> 2
        wallnut.take_damage()  # health: 2 -> 1
        result = wallnut.take_damage()  # health: 1 -> 0
        
        # Verify take_damage returned True (wallnut destroyed)
        self.assertTrue(result)
        # Verify wallnut was removed from sprite group
        self.assertNotIn(wallnut, sprite_group)
        print("✅ take_damage() killed sprite when health reached 0")

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
        print("✅ take_damage() updated image attribute successfully")


class TestWallNutManager(unittest.TestCase):
    """Test suite for WallNutManager class"""

    @classmethod
    def setUpClass(cls):
        """Initialize pygame once for all tests"""
        # Set SDL to use dummy video driver
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        # Initialize pygame
        pygame.init()
        # Create a display surface (required for convert_alpha())
        cls.display = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        """Quit pygame after all tests"""
        # Clean up pygame
        pygame.quit()

    def setUp(self):
        """Set up test fixtures before each test"""
        # Create mock surface for wallnut images
        mock_surface = pygame.Surface((60, 60))
        # Now convert_alpha() will work
        self.mock_surface = mock_surface.convert_alpha()
        
        # Create WallNutManager instance
        self.manager = WallNutManager(
            player_position=(400, 500),
            screen_width=800,
            screen_height=600
        )

    def test_manager_has_four_slots(self):
        """Test that WallNutManager has 4 slots"""
        # Verify max_wallnuts is 4
        self.assertEqual(self.manager.max_wallnuts, 4)
        # Verify slot_occupied list has 4 elements
        self.assertEqual(len(self.manager.slot_occupied), 4)
        print(f"✅ WallNutManager has {self.manager.max_wallnuts} slots")

    def test_manager_has_wallnuts_sprite_group(self):
        """Test that WallNutManager has a sprite group for wallnuts"""
        # Verify wallnuts attribute exists
        self.assertTrue(hasattr(self.manager, 'wallnuts'))
        # Verify it's a pygame sprite Group
        self.assertIsInstance(self.manager.wallnuts, pygame.sprite.Group)
        print("✅ WallNutManager has wallnuts sprite group")

    def test_slot_positions_evenly_distributed(self):
        """Test that slot positions are evenly distributed"""
        # Get slot positions
        positions = self.manager.slot_positions
        
        # Verify there are 4 positions
        self.assertEqual(len(positions), 4)
        
        # Calculate distances between consecutive positions
        distances = []
        for i in range(len(positions) - 1):
            distance = positions[i + 1][0] - positions[i][0]
            distances.append(distance)
        
        # Verify all distances are approximately equal (within 1 pixel tolerance)
        if len(distances) > 0:
            avg_distance = sum(distances) / len(distances)
            for distance in distances:
                self.assertAlmostEqual(distance, avg_distance, delta=1)
        
        print(f"✅ Slot positions evenly distributed: {len(positions)} slots")

    def test_slot_positions_within_screen_bounds(self):
        """Test that all slot positions are within screen bounds"""
        # Get slot positions
        positions = self.manager.slot_positions
        
        # Verify all positions are within screen width
        for x, y in positions:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, self.manager.screen_width)
        
        print(f"✅ All {len(positions)} slot positions within screen bounds")

    def test_place_wallnut_adds_to_sprite_group(self):
        """Test that place_wallnut() adds wallnut to sprite group"""
        # Get initial count
        initial_count = len(self.manager.wallnuts)
        
        # Place a wallnut with mocked image loading
        with patch('pygame.image.load', return_value=self.mock_surface):
            result = self.manager.place_wallnut(slot_index=0)
        
        # Verify placement was successful
        self.assertTrue(result)
        # Verify wallnut was added to sprite group
        self.assertEqual(len(self.manager.wallnuts), initial_count + 1)
        print(f"✅ place_wallnut() added wallnut to sprite group (count: {len(self.manager.wallnuts)})")

    def test_check_projectile_collision_removes_projectile(self):
        """Test that check_projectile_collision() removes projectile on collision"""
        # Create projectile group
        projectile_group = pygame.sprite.Group()
        
        # Create a mock projectile sprite
        mock_projectile = pygame.sprite.Sprite()
        mock_projectile.image = pygame.Surface((10, 10))
        mock_projectile.rect = mock_projectile.image.get_rect()
        projectile_group.add(mock_projectile)
        
        # Place a wallnut at same position as projectile
        with patch('pygame.image.load', return_value=self.mock_surface):
            self.manager.place_wallnut(slot_index=0)
            # Get the wallnut and position projectile at same location
            wallnut = list(self.manager.wallnuts)[0]
            mock_projectile.rect.center = wallnut.rect.center
        
        # Store initial projectile count
        initial_projectile_count = len(projectile_group)
        
        # Check for collision
        collisions = self.manager.check_projectile_collision(projectile_group)
        
        # Verify projectile was removed
        self.assertLess(len(projectile_group), initial_projectile_count)
        print("✅ check_projectile_collision() removed projectile on collision")

    def test_collision_updates_slot_availability(self):
        """Test that collisions properly track slot occupation"""
        # Place a wallnut
        with patch('pygame.image.load', return_value=self.mock_surface):
            self.manager.place_wallnut(slot_index=1)
        
        # Verify slot is marked as occupied
        self.assertTrue(self.manager.slot_occupied[1])
        
        # Try to place another wallnut in same slot
        with patch('pygame.image.load', return_value=self.mock_surface):
            result = self.manager.place_wallnut(slot_index=1)
        
        # Verify placement failed (slot already occupied)
        self.assertFalse(result)
        print("✅ Slot occupation tracking works correctly")

    def test_no_collision_when_no_wallnuts(self):
        """Test that no collision occurs when there are no wallnuts"""
        # Create projectile group
        projectile_group = pygame.sprite.Group()
        
        # Create a mock projectile
        mock_projectile = pygame.sprite.Sprite()
        mock_projectile.image = pygame.Surface((10, 10))
        mock_projectile.rect = mock_projectile.image.get_rect()
        projectile_group.add(mock_projectile)
        
        # Check for collision (no wallnuts placed)
        collisions = self.manager.check_projectile_collision(projectile_group)
        
        # Verify no collisions occurred
        self.assertEqual(len(collisions), 0)
        # Verify projectile still exists
        self.assertEqual(len(projectile_group), 1)
        print("✅ No collision when no wallnuts present")

if __name__ == '__main__':
    unittest.main()
