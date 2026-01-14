import unittest
import pygame
from unittest.mock import patch, MagicMock

# Initialize pygame
pygame.init()
pygame.display.set_mode((1, 1))

from GardenInvasion.Controller.plant_controller import handle_player_input
from GardenInvasion.Model.plant_model import Player
from GardenInvasion.Model.setting_volume_model import SettingsModel
from GardenInvasion.Model.sound_manager_model import SoundManager

class TestPlantController(unittest.TestCase):
    # Test suite for plant controller
    
    def setUp(self):
        # Set up test fixtures
        self.mock_surface = pygame.Surface((100, 100))
        
        # Create a mock that returns a surface with convert_alpha
        self.mock_image = MagicMock()
        self.mock_image.convert_alpha.return_value = self.mock_surface
        
        # Patch both pygame.image.load for Player and Projectile
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_image)
        self.image_patcher.start()
        
        self.settings = SettingsModel()
        self.player = Player((300, 570), self.settings)
        self.projectile_group = pygame.sprite.Group()

        self.mock_sound_manager=MagicMock(spec=SoundManager) # Mock SoundManager
    
    def tearDown(self):
        self.image_patcher.stop()
        pygame.event.clear()
    
    def test_left_arrow_moves_player_left(self):
        # Test that left arrow moves player left
        initial_x = self.player.rect.x
        
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: True, pygame.K_RIGHT: False, 
                                                           pygame.K_a: False, pygame.K_d: False}):
            handle_player_input(self.player, self.projectile_group)
        
        self.assertLess(self.player.rect.x, initial_x)
        print("✅ Left arrow moves player left")
    
    def test_right_arrow_moves_player_right(self):
        # Test that right arrow moves player right

        initial_x = self.player.rect.x
        
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: True,
                                                           pygame.K_a: False, pygame.K_d: False}):
            handle_player_input(self.player, self.projectile_group)
        
        self.assertGreater(self.player.rect.x, initial_x)
        print("✅ Right arrow moves player right")
    
    @patch('pygame.time.get_ticks')
    def test_player_auto_shooting_with_cooldown(self, mock_ticks):
        # Test that projectile creation respects 500ms cooldown

        # First shot at time 0
        mock_ticks.return_value = 0
        self.player.last_shot = 0
        
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: False,
                                                           pygame.K_a: False, pygame.K_d: False}):
            handle_player_input(self.player, self.projectile_group)
        
        first_count = len(self.projectile_group)
        
        # Second attempt at 200ms - should not shoot (cooldown not elapsed)
        mock_ticks.return_value = 200
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: False,
                                                           pygame.K_a: False, pygame.K_d: False}):
            handle_player_input(self.player, self.projectile_group)
        self.assertEqual(len(self.projectile_group), first_count)
        
        # Third attempt at 600ms - should shoot (cooldown elapsed)
        mock_ticks.return_value = 600
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: False,
                                                           pygame.K_a: False, pygame.K_d: False}):
            handle_player_input(self.player, self.projectile_group)
        self.assertGreater(len(self.projectile_group), first_count)
        
        print("✅ Projectile creation respects 500ms cooldown")
    
    def test_player_stops_at_left_boundary(self):
        # Test that player cannot move beyond left screen boundary
        self.player.rect.x = 5
        
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: True, pygame.K_RIGHT: False,
                                                           pygame.K_a: False, pygame.K_d: False}):
            for _ in range(10):  # Try to move left many times
                handle_player_input(self.player, self.projectile_group)
        
        self.assertGreaterEqual(self.player.rect.left, 0)
        print("✅ Player stops at left boundary")
    
    def test_player_stops_at_right_boundary(self):
        # Test that player cannot move beyond right screen boundary
        
        self.player.rect.x = 590  # Near right edge
        
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: True,
                                                           pygame.K_a: False, pygame.K_d: False}):
            for _ in range(10):  # Try to move right many times
                handle_player_input(self.player, self.projectile_group)
        
        self.assertLessEqual(self.player.rect.right, 600)
        print("✅ Player stops at right boundary")

    @patch('pygame.time.get_ticks') # Mock time to control shooting timing
    def test_shoot_sound_plays_when_projectile_created(self, mock_ticks):
        # Test that plant_shoot sound plays when player shoots

        mock_ticks.return_value = 1000 # Simulate time
        self.player.last_shot = 0 # Ensure shooting is allowed
        
        # Reset mock to clear any previous calls
        self.mock_sound_manager.reset_mock()
        
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: False,
                                                           pygame.K_a: False, pygame.K_d: False}):
            handle_player_input(self.player, self.projectile_group, self.mock_sound_manager)
        
        # Verify sound was played
        self.mock_sound_manager.play_sound.assert_called_once_with('plant_shoot')
        print("✅ plant_shoot sound plays when projectile created")
    
    @patch('pygame.time.get_ticks')
    def test_no_sound_during_cooldown(self, mock_ticks):
        # Test that no sound plays when cooldown prevents shooting

        mock_ticks.return_value = 1000
        self.player.last_shot = 0
        
        # First shot
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: False,
                                                           pygame.K_a: False, pygame.K_d: False}):
            handle_player_input(self.player, self.projectile_group, self.mock_sound_manager)
        
        # Reset mock
        self.mock_sound_manager.reset_mock()
        
        # Try to shoot during cooldown (200ms)
        mock_ticks.return_value = 200
        with patch('pygame.key.get_pressed', return_value={pygame.K_LEFT: False, pygame.K_RIGHT: False,
                                                           pygame.K_a: False, pygame.K_d: False}):
            handle_player_input(self.player, self.projectile_group, self.mock_sound_manager)
        
        # Sound should NOT have been called
        self.mock_sound_manager.play_sound.assert_not_called()
        print("✅ No sound plays during shooting cooldown")
    
if __name__ == '__main__':
    unittest.main()
