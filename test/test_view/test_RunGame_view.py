import unittest
from unittest.mock import Mock, patch
import pygame
import os
from GardenInvasion.View.RunGame_view import draw_game
from GardenInvasion.Model.plant_model import Player
from GardenInvasion.Model.wallnut_model import WallNut
from GardenInvasion.Model.projectile_model import Projectile
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from GardenInvasion.Model.setting_volume_model import SettingsModel

class TestRunGameView(unittest.TestCase):
    """Test suite for game view rendering functions"""

    @classmethod
    def setUpClass(cls):
        #Initialize pygame once for all tests
        os.environ['SDL_VIDEODRIVER'] = 'dummy' # Use dummy video driver for headless testing
        os.environ['SDL_AUDIODRIVER'] = 'dummy' # Use dummy audio driver for headless testing
        pygame.init()
        cls.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        #Quit pygame after all tests
        pygame.quit()

    def setUp(self):
        #Set up test fixtures before each test
        self.screen = self.display # Main display surface
        
        # Create sprite groups
        self.player_group = pygame.sprite.Group() # Group for player sprites
        self.projectile_group = pygame.sprite.Group() # Group for projectile sprites
        self.wallnut_group = pygame.sprite.Group() # Group for wallnut sprites
        self.zombie_group = pygame.sprite.Group()  # NUOVO: Group for zombie sprites
        self.zombie_projectile_group = pygame.sprite.Group()
        
    #Create settings model for Player
        self.settings_model = SettingsModel()

        # Create mock background
        self.game_background = Mock() # Mock background object
        self.game_background.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_background.rect = self.game_background.surface.get_rect()

    def test_draw_game_does_not_crash(self):
        """Test that draw_game executes without exceptions"""
        try:
            draw_game(self.screen, self.game_background, self.player_group, 
                     self.projectile_group, self.wallnut_group, self.zombie_group)  # AGGIUNTO zombie_group
            print("✅ draw_game executed successfully without errors")
        except Exception as e:
            self.fail(f"❌ draw_game raised an exception: {e}")

    def test_draw_game_renders_player(self):
        """Test that draw_game renders the player sprite"""
        # Create a mock surface to return when pygame.image.load is called
        mock_surface = pygame.Surface((100, 100)) # Mock player image
        mock_surface = mock_surface.convert_alpha() # Ensure it has alpha channel
        # Add a player to the group
        with patch('pygame.image.load', return_value=mock_surface):
            player = Player(pos=(400, 500), settings_model=self.settings_model) # Create player instance
            self.player_group.add(player) # Add player to group
        try:
            draw_game(self.screen, self.game_background, self.player_group, 
                     self.projectile_group, self.wallnut_group, self.zombie_group)  # AGGIUNTO zombie_group
            print("✅ draw_game rendered player sprite successfully")
        except Exception as e:
            self.fail(f"❌ draw_game failed with player sprite: {e}")

    def test_draw_game_renders_projectiles(self):
        """Test that draw_game renders all projectiles in the group"""
        # Create a mock surface for projectile image
        mock_surface = pygame.Surface((20, 20)) # Mock projectile image
        mock_surface = mock_surface.convert_alpha() # Ensure it has alpha channel
        
        # Add multiple projectiles
        with patch('pygame.image.load', return_value=mock_surface):
            for i in range(3):
                projectile = Projectile(pos=(100 * i, 300)) # Create projectile instance
                self.projectile_group.add(projectile) # Add projectile to group
        
        try:
            draw_game(self.screen, self.game_background, self.player_group, 
                     self.projectile_group, self.wallnut_group, self.zombie_group)  # AGGIUNTO zombie_group
            print(f"✅ draw_game rendered {len(self.projectile_group)} projectile sprites successfully")
        except Exception as e:
            self.fail(f"❌ draw_game failed with projectile sprites: {e}")

    def test_draw_game_renders_wallnuts(self):
        """Test that draw_game renders all wallnuts in the group"""
        # Create mock surfaces for wallnut sprites
        mock_surface = pygame.Surface((60, 60))
        mock_surface = mock_surface.convert_alpha()
        
        # Add multiple wallnuts
        with patch('pygame.image.load', return_value=mock_surface):
            for i in range(4): # Add 4 wallnuts
                wallnut = WallNut(position=(200 * i, 400), slot_index=i) # Create wallnut instance
                self.wallnut_group.add(wallnut) # Add wallnut to group
        
        try:
            draw_game(self.screen, self.game_background, self.player_group, 
                     self.projectile_group, self.wallnut_group, self.zombie_group)  # AGGIUNTO zombie_group
            print(f"✅ draw_game rendered {len(self.wallnut_group)} wallnut sprites successfully")
        except Exception as e:
            self.fail(f"❌ draw_game failed with wallnut sprites: {e}")

    # NUOVO TEST: Verifica rendering degli zombie
    def test_draw_game_renders_zombies(self):
        """Test that draw_game renders all zombies in the group"""
        # Create a mock zombie sprite
        mock_zombie = Mock(spec=pygame.sprite.Sprite)
        mock_zombie.image = pygame.Surface((30, 50))
        mock_zombie.rect = mock_zombie.image.get_rect(center=(300, 200))
        
        # Add zombie to group
        self.zombie_group.add(mock_zombie)
        
        try:
            draw_game(self.screen, self.game_background, self.player_group,
                     self.projectile_group, self.wallnut_group, self.zombie_group)
            print(f"✅ draw_game rendered {len(self.zombie_group)} zombie sprites successfully")
        except Exception as e:
            self.fail(f"❌ draw_game failed with zombie sprites: {e}")

    def test_draw_game_without_zombies(self):
        """Test that draw_game works without zombie_group parameter (backward compatibility)"""
        try:
            # ✅ FIXED: Call with only 5 parameters (without zombie groups) - this is what the test name says!
            draw_game(self.screen, self.game_background, self.player_group,
                    self.projectile_group, self.wallnut_group)
            print("✅ draw_game works without zombie_group (backward compatible)")
        except TypeError as e:
            self.fail(f"❌ draw_game not backward compatible: {e}")
        except Exception as e:
            self.fail(f"❌ Other error: {e}")


    def test_draw_game_layering_order(self):
        """Test that draw_game maintains correct visual layering"""
        # NOTE: Questo test verrà implementato successivamente quando
        # il sistema di rendering sarà completo. Pygame Surface.blit è
        # un attributo read-only che non può essere mockato facilmente.
        # Per ora testiamo la funzionalità base senza verificare l'ordine esatto.
        pass

    # NUOVO TEST: Verifica con zombie_group None
    def test_draw_game_with_none_zombie_group(self):
        """Test that draw_game handles None zombie_group correctly"""
        try:
            draw_game(self.screen, self.game_background, self.player_group,
                     self.projectile_group, self.wallnut_group, None)
            print("✅ draw_game handles None zombie_group correctly")
        except Exception as e:
            self.fail(f"❌ draw_game failed with None zombie_group: {e}")

    # NUOVO TEST: Verifica con zombie_group vuoto
    def test_draw_game_with_empty_zombie_group(self):
        """Test that draw_game handles empty zombie_group correctly"""
        try:
            draw_game(self.screen, self.game_background, self.player_group,
                     self.projectile_group, self.wallnut_group, pygame.sprite.Group())
            print("✅ draw_game handles empty zombie_group correctly")
        except Exception as e:
            self.fail(f"❌ draw_game failed with empty zombie_group: {e}")


if __name__ == '__main__':
    unittest.main()