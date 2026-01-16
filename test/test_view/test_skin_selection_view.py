import unittest
import pygame
from unittest.mock import patch, MagicMock
import os
import sys

# Try to initialize pygame with proper video/audio drivers
# this is due to past errors in this test file when run in headless environments
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    pygame.quit()  # Clean slate
    pygame.init()
except:
    pass
# Force quit and restart without dummy driver if font init fails
if not pygame.font.get_init():
    try:
        pygame.quit()
        if 'SDL_VIDEODRIVER' in os.environ:
            del os.environ['SDL_VIDEODRIVER']
        if 'SDL_AUDIODRIVER' in os.environ:
            del os.environ['SDL_AUDIODRIVER']
        pygame.init()
    except:
        pass

from GardenInvasion.View.skin_selection_view import draw_skin_selection_menu
from GardenInvasion.Model.skin_selection_model import SkinSelectionModel
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class TestSkinSelectionView(unittest.TestCase):
    # Test suite for skin selection view rendering
    
    @classmethod
    def setUpClass(cls):
        # Set up class-level fixtures once before all tests
        # Ensure pygame and font are initialized
        if not pygame.get_init():
            pygame.init()
        
        if not pygame.font.get_init():
            pygame.font.init()
        
        # Create display
        try:
            pygame.display.set_mode((800, 600), pygame.HIDDEN)
        except:
            try:
                pygame.display.set_mode((1, 1))
            except:
                pass
    
    def setUp(self):
        # Set up test fixtures before each test
        # Create test screen
        self.screen = pygame.Surface((800, 600))
        
        # Mock pygame.image.load
        self.mock_surface = pygame.Surface((100, 100))
        self.patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.patcher.start()
        
        # Create test model
        self.model = SkinSelectionModel()
        
        # Create test fonts
        try:
            self.title_font = pygame.font.Font(None, 32)
            self.item_font = pygame.font.Font(None, 20)
            self.inst_font = pygame.font.Font(None, 14)
        except pygame.error:
            # If Font still fails, skip font-dependent tests
            self.skipTest("Font initialization failed - cannot test rendering")
        
        self.fonts = (self.title_font, self.item_font, self.inst_font)
        
        # Create test background
        self.background_surf = pygame.Surface((800, 600))
        self.background_surf.fill((50, 50, 100))
        self.background_rect = self.background_surf.get_rect()
    
    def tearDown(self):
        self.patcher.stop()

    def test_draw_skin_selection_menu_with_background(self):
        # Test drawing with custom background
        try:
            back_rect = draw_skin_selection_menu(
                self.screen,
                self.model,
                self.background_surf,
                self.background_rect,
                self.fonts
            )
            self.assertIsNotNone(back_rect)
            self.assertIsInstance(back_rect, pygame.Rect)
            print("✅ Skin selection menu renders with custom background")
        except Exception as e:
            self.fail(f"❌ Error: {e}")
    
    def test_draw_skin_selection_menu_without_background(self):
        # Test drawing without background (solid color fallback)
        try:
            back_rect = draw_skin_selection_menu(
                self.screen,
                self.model,
                None,  # No background
                None,
                self.fonts
            )
            self.assertIsNotNone(back_rect)
            self.assertIsInstance(back_rect, pygame.Rect)
            print("✅ Skin selection menu renders with solid color fallback")
        except Exception as e:
            self.fail(f"❌ Error: {e}")
    
    def test_draw_skin_selection_menu_with_skin_selected(self):
        # Test drawing with a skin selected
        self.model.selected_index = 1
        self.model.back_button_selected = False
        
        try:
            back_rect = draw_skin_selection_menu(
                self.screen,
                self.model,
                self.background_surf,
                self.background_rect,
                self.fonts
            )
            self.assertIsNotNone(back_rect)
            print("✅ Skin selection menu renders with skin selected")
        except Exception as e:
            self.fail(f"❌ Error: {e}")


if __name__ == '__main__':
    unittest.main()
