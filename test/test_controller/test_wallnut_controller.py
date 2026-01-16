import unittest
import pygame
from unittest.mock import patch, MagicMock

# Initialize pygame
pygame.init()
pygame.display.set_mode((1, 1))

from GardenInvasion.Controller.wallnut_controller import handle_wallnut_placement, handle_wallnut_collisions
from GardenInvasion.Model.wallnut_model import WallNut, WallNutManager
from GardenInvasion.Model.projectile_model import Projectile
from GardenInvasion.Model.sound_manager_model import SoundManager

class TestWallnutController(unittest.TestCase):
    # Test suite for wallnut controller
    
    def setUp(self):
        # Set up test fixtures

        # Create a mock surface for images
        self.mock_surface = pygame.Surface((60, 60))
        
        # Create a mock image with convert_alpha method
        self.mock_image = MagicMock()
        self.mock_image.convert_alpha.return_value = self.mock_surface
        
        # Patch pygame.image.load to return our mock for both wallnuts and projectiles
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_image)
        self.image_patcher.start()

        self.mock_sound_manager = MagicMock(spec=SoundManager) # Mock SoundManager
        
        # Create wallnut manager
        self.wallnut_manager = WallNutManager(
            player_position=(300, 570),
            screen_width=600,
            screen_height=600
        )
        self.projectile_group = pygame.sprite.Group()
    
    def tearDown(self):
        self.image_patcher.stop()
        pygame.event.clear()
    
    def test_projectile_collision_blocks_projectile(self):
        # Test that projectiles are blocked by wallnuts

        # Place a wallnut
        self.wallnut_manager.place_wallnut(0)
        
        # Create a projectile
        projectile = Projectile((100, 300))
        self.projectile_group.add(projectile)
        
        initial_projectile_count = len(self.projectile_group)
        self.assertEqual(initial_projectile_count, 1)
        
        # Manually position projectile to collide with wallnut
        wallnut = list(self.wallnut_manager.wallnuts)[0]
        projectile.rect.center = wallnut.rect.center
        
        # Handle collision
        collisions = handle_wallnut_collisions(self.wallnut_manager, self.projectile_group)
        
        # Projectile should be removed
        self.assertEqual(len(self.projectile_group), 0)
        print("✅ Projectiles are blocked by wallnuts")
    
    def test_wallnut_not_damaged_by_player_projectile(self):
        # Test that wallnuts are not damaged by player projectiles (friendly fire disabled)
        
        # Place a wallnut
        self.wallnut_manager.place_wallnut(0)
        wallnut = list(self.wallnut_manager.wallnuts)[0]
        initial_health = wallnut.health
        
        # Create a projectile at same position
        projectile = Projectile(wallnut.rect.center)
        self.projectile_group.add(projectile)
        
        # Handle collision
        handle_wallnut_collisions(self.wallnut_manager, self.projectile_group)
        
        # Wallnut health should be unchanged (no friendly fire)
        self.assertEqual(wallnut.health, initial_health)
        print("✅ Wallnuts not damaged by player projectiles (friendly fire disabled)")

    def test_wallnut_destroyed_sound_plays(self):
        # Test that wallnut_destroyed sound plays when wallnut health reaches 0

        # Create wallnut directly with mock sound manager
        wallnut = WallNut((300, 300), 0, self.mock_sound_manager)
        
        # Reset mock
        self.mock_sound_manager.reset_mock()
        
        # Damage wallnut 3 times to destroy it
        wallnut.take_damage()  # Health: 1
        result = wallnut.take_damage()  # Health: 0 (destroyed)
        
        # Verify destruction sound was played
        self.mock_sound_manager.play_sound.assert_called_once_with('wallnut_destroyed')
        self.assertTrue(result)  # Should return True when destroyed
        print("✅ wallnut_destroyed sound plays when health reaches 0")

    def test_no_sound_when_wallnut_damaged_but_alive(self):
        # Test that no sound plays when wallnut is damaged but not destroyed
        
        wallnut = WallNut((300, 300), 0, self.mock_sound_manager)
        
        # Reset mock
        self.mock_sound_manager.reset_mock()
        
        # Damage wallnut once (should survive)
        result = wallnut.take_damage()  # Health: 2
        
        # Sound should NOT have been called
        self.mock_sound_manager.play_sound.assert_not_called()
        self.assertFalse(result)  # Should return False (not destroyed)
        print("✅ No sound plays when wallnut damaged but still alive")
    
if __name__ == '__main__':
    unittest.main()
