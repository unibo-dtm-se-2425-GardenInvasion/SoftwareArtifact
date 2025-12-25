import unittest
import pygame
from unittest.mock import patch, MagicMock

# Initialize pygame
pygame.init()
pygame.display.set_mode((1, 1))

from GardenInvasion.Controller.wallnut_controller import handle_wallnut_placement, handle_wallnut_collisions
from GardenInvasion.Model.wallnut_model import WallNutManager
from GardenInvasion.Model.projectile_model import Projectile

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

if __name__ == '__main__':
    unittest.main()
