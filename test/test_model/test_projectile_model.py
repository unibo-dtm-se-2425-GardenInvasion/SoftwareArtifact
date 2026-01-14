import unittest
from unittest.mock import Mock, patch
import pygame
import os
from GardenInvasion.Model.projectile_model import Projectile

class TestProjectile(unittest.TestCase):
    """Test suite for Projectile class"""

    @classmethod
    def setUpClass(cls):
        #Initialize pygame once for all tests
        os.environ['SDL_VIDEODRIVER'] = 'dummy' # Set SDL to use dummy video driver
        pygame.init()
        cls.display = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        #Quit pygame after all tests
        pygame.quit()

    def setUp(self):
        #Set up test fixtures before each test
        mock_surface = pygame.Surface((20, 20)) # Create a mock surface for projectile image
        self.mock_surface = mock_surface.convert_alpha() 

    def test_projectile_initializes_at_position(self):
        #Test that Projectile initializes at the specified position
        test_position = (200, 300) # Define test position
        
        with patch('pygame.image.load', return_value=self.mock_surface):
            projectile = Projectile(pos=test_position)# Create Projectile with mocked image loading
        
        
        self.assertEqual(projectile.rect.midbottom, test_position)
        print(f"✅ Projectile initialized at position: {test_position}") # Verify projectile's midbottom matches the position

    def test_projectile_image_loaded(self):
        #Test that Projectile image is loaded successfully
        with patch('pygame.image.load', return_value=self.mock_surface):
            projectile = Projectile(pos=(200, 300))
        
        self.assertTrue(hasattr(projectile, 'image'))
        self.assertIsNotNone(projectile.image)
        self.assertIsInstance(projectile.image, pygame.Surface)
        print("✅ Projectile image loaded successfully") # Verify image attribute exists and it is a pygame.Surface

    def test_update_moves_projectile_upward(self):
        #Test that update() moves projectile upward (negative y direction)
        with patch('pygame.image.load', return_value=self.mock_surface):
            projectile = Projectile(pos=(200, 300))
        
        initial_y = projectile.rect.y # Store initial y position
        projectile.update()
        
        self.assertLess(projectile.rect.y, initial_y)
        print(f"✅ update() moved projectile upward from y={initial_y} to y={projectile.rect.y}") # Verify y position decreased (moved upward)S

    def test_update_removes_projectile_offscreen(self):
        #Test that update() removes projectile when it goes off-screen
        sprite_group = pygame.sprite.Group()
        with patch('pygame.image.load', return_value=self.mock_surface):
            projectile = Projectile(pos=(200, 10))  # Start near top
            sprite_group.add(projectile)
        
        for _ in range(20): # Move projectile off-screen by calling update multiple times
            projectile.update()
        
        self.assertNotIn(projectile, sprite_group)
        print("✅ update() removed projectile when it went off-screen") # Verify projectile was removed from the group

if __name__ == '__main__':
    unittest.main()
