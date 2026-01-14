import unittest
from unittest.mock import MagicMock, Mock, patch
import pygame
import os
from GardenInvasion.Model.plant_model import Player

class TestPlayer(unittest.TestCase):
    """Test suite for Player class"""

    @classmethod
    def setUpClass(cls):
        # Initialize pygame once for all tests
        os.environ['SDL_VIDEODRIVER'] = 'dummy' # Set SDL to use dummy video driver (no window needed)
        pygame.init()
        cls.display = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        # Quit pygame after all tests
        pygame.quit()

    def setUp(self):
        # Set up test fixtures before each test
        mock_surface = pygame.Surface((100, 100)) # Create a mock surface to return when pygame.image.load is called
        self.mock_surface = mock_surface.convert_alpha()

    def test_player_initializes_with_position(self):
        # Test that Player initializes at the specified position
        test_position = (400, 500) # Define test position
        
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=test_position) # Create Player with mocked image loading
        
        self.assertEqual(player.rect.midbottom, test_position) # Verify player's midbottom matches the position
        print(f"✅ Player initialized at position: {test_position}")

    def test_player_has_last_shot_timestamp(self):
        # Test that Player has last_shot timestamp attribute
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
       
        self.assertTrue(hasattr(player, 'last_shot'))
        self.assertIsInstance(player.last_shot, (int, float))  # Verify last_shot attribute exists and is a number
        print("✅ Player has last_shot timestamp attribute")

    def test_player_image_loaded_and_scaled(self):
        # Test that Player image is loaded and scaled correctly
        # Mock the settings model with default skin
        mock_settings = MagicMock()
        mock_settings.player_skin = "default"
        # Mock pygame.image.load to return our mock surface
        with patch('pygame.image.load', return_value=self.mock_surface):
            # Mock Path.exists() to return True (so it doesn't try fallback path)
            with patch('pathlib.Path.exists', return_value=True):
                # Create player with mocked settings
                player = Player(pos=(400, 500), settings_model=mock_settings)
        
        # Verify image attribute exists and is a pygame.Surface
        self.assertTrue(hasattr(player, 'image'))
        self.assertIsNotNone(player.image)
        self.assertIsInstance(player.image, pygame.Surface)
        # Verify scale_factor is set correctly (now internal to Player class)
        self.assertTrue(hasattr(player, 'scale_factor'))
        self.assertEqual(player.scale_factor, 0.15)
        print("✅ Player image loaded and scaled successfully")

    def test_player_has_life_points(self):
        """Test that Player initializes with 2 life points"""
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        # Check life points attributes exist
        self.assertTrue(hasattr(player, 'life_points'))
        self.assertTrue(hasattr(player, 'max_life_points'))
        
        # Verify initial values are 2
        self.assertEqual(player.life_points, 2)
        self.assertEqual(player.max_life_points, 2)
        print("✅ Player initialized with 2 life points")

    def test_player_take_damage_reduces_life_points(self):
        """Test that take_damage() reduces life points by 1"""
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        initial_life = player.life_points
        is_destroyed = player.take_damage()
        
        # Life should decrease by 1
        self.assertEqual(player.life_points, initial_life - 1)
        # Plant should not be destroyed after first hit
        self.assertFalse(is_destroyed)
        print(f"✅ take_damage() reduced life from {initial_life} to {player.life_points}")

    def test_player_is_alive_after_one_damage(self):
        """Test that plant is still alive after taking 1 damage"""
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        player.take_damage()
        
        # Check is_alive() method
        self.assertTrue(player.is_alive())
        self.assertEqual(player.life_points, 1)
        print("✅ Plant is alive after 1 damage")

    def test_player_destroyed_after_two_damages(self):
        """Test that plant is destroyed after taking 2 damages"""
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        # First damage
        first_destroyed = player.take_damage()
        self.assertFalse(first_destroyed)
        self.assertEqual(player.life_points, 1)
        
        # Second damage
        second_destroyed = player.take_damage()
        self.assertTrue(second_destroyed)
        self.assertEqual(player.life_points, 0)
        
        # Plant should not be alive
        self.assertFalse(player.is_alive())
        print("✅ Plant is destroyed after 2 damages")

    def test_player_take_damage_below_zero(self):
        """Test that take_damage() doesn't go below 0 life points"""
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        # Take 3 damages (more than available)
        results = []
        for i in range(3):
            results.append(player.take_damage())
        
        # Life points should not go below 0
        self.assertEqual(player.life_points, 0)
        # Only the second damage should return True for destruction
        self.assertFalse(results[0])  # First damage
        self.assertTrue(results[1])   # Second damage (destruction)
        self.assertTrue(results[2])   # Third damage (already destroyed)
        print("✅ Life points don't go below 0")

    def test_move_left_decreases_x_position(self):
        # Test that move_left() decreases player's x position
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        initial_x = player.rect.x # Store initial x position
        player.move_left()
        
        self.assertLess(player.rect.x, initial_x)
        print(f"✅ move_left() decreased x from {initial_x} to {player.rect.x}") # Verify x position decreased

    def test_move_right_increases_x_position(self):
        # Test that move_right() increases player's x position
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        
        initial_x = player.rect.x # Store initial x position
        player.move_right()
        
        self.assertGreater(player.rect.x, initial_x)
        print(f"✅ move_right() increased x from {initial_x} to {player.rect.x}") # Verify x position increased

    def test_can_shoot_returns_true_after_cooldown(self):
        # Test that can_shoot() returns True after cooldown period
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        current_time = pygame.time.get_ticks() # Simulate time passing by setting last_shot to the past
        player.last_shot = current_time - 1000 # Set last_shot to 1 second ago
                
        can_shoot = player.can_shoot() # Check if can shoot (cooldown is 500ms, so should be True)
        self.assertTrue(can_shoot)
        print("✅ can_shoot() returned True after cooldown period") # Verify can_shoot returns True

if __name__ == '__main__':
    unittest.main()