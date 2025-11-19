import unittest
from unittest.mock import Mock, patch
import pygame
import os
from my_project.Model.plant_model import Player

class TestPlayer(unittest.TestCase):
    """Test suite for Player class"""

    @classmethod
    def setUpClass(cls):
        #Initialize pygame once for all tests
        os.environ['SDL_VIDEODRIVER'] = 'dummy' # Set SDL to use dummy video driver (no window needed)
        pygame.init()
        cls.display = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        #Quit pygame after all tests
        pygame.quit()

    def setUp(self):
        #Set up test fixtures before each test
        mock_surface = pygame.Surface((100, 100)) # Create a mock surface to return when pygame.image.load is called
        self.mock_surface = mock_surface.convert_alpha()

    def test_player_initializes_with_position(self):
        #Test that Player initializes at the specified position
        test_position = (400, 500)# Define test position
        
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=test_position)# Create Player with mocked image loading
        
        self.assertEqual(player.rect.midbottom, test_position) # Verify player's midbottom matches the position
        print(f"✅ Player initialized at position: {test_position}")

    def test_player_has_last_shot_timestamp(self):
        #Test that Player has last_shot timestamp attribute
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
       
        self.assertTrue(hasattr(player, 'last_shot'))
        self.assertIsInstance(player.last_shot, (int, float))  # Verify last_shot attribute exists and is a number
        print("✅ Player has last_shot timestamp attribute")

    def test_player_image_loaded_and_scaled(self):
        #Test that Player image is loaded and scaled correctly
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500), scale_factor=0.15)
        
        self.assertTrue(hasattr(player, 'image'))
        self.assertIsNotNone(player.image)
        self.assertIsInstance(player.image, pygame.Surface)
        print("✅ Player image loaded and scaled successfully") # Verify image attribute extsts and it is a pygame.Surface

    def test_move_left_decreases_x_position(self):
        #Test that move_left() decreases player's x position
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        initial_x = player.rect.x # Store initial x position
        player.move_left()
        
        self.assertLess(player.rect.x, initial_x)
        print(f"✅ move_left() decreased x from {initial_x} to {player.rect.x}") # Verify x position decreased

    def test_move_right_increases_x_position(self):
        #Test that move_right() increases player's x position
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        
        initial_x = player.rect.x # Store initial x position
        player.move_right()
        
        self.assertGreater(player.rect.x, initial_x)
        print(f"✅ move_right() increased x from {initial_x} to {player.rect.x}") # Verify x position increased

    def test_can_shoot_returns_true_after_cooldown(self):
        #Test that can_shoot() returns True after cooldown period
        with patch('pygame.image.load', return_value=self.mock_surface):
            player = Player(pos=(400, 500))
        
        current_time = pygame.time.get_ticks() # Simulate time passing by setting last_shot to the past
        player.last_shot = current_time - 1000 # Set last_shot to 1 second ago
                
        can_shoot = player.can_shoot() # Check if can shoot (cooldown is 500ms, so should be True)
        self.assertTrue(can_shoot)
        print("✅ can_shoot() returned True after cooldown period") # Verify can_shoot returns True

if __name__ == '__main__':
    unittest.main()
