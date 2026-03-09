import unittest
import pygame
import os
from unittest.mock import patch, MagicMock

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from GardenInvasion.Model.PowerUp_model import PowerUpManager, IncreasingFirePU, RepairWallnutPU
from GardenInvasion.Model.plant_model import Player
from GardenInvasion.Model.wallnut_model import WallNutManager
from GardenInvasion.Model.setting_volume_model import SettingsModel
from GardenInvasion.Model.sound_manager_model import SoundManager


class TestPowerUpController(unittest.TestCase):
    # Tests for power-up collection and drop logic in the controller

    @classmethod
    def setUpClass(cls):
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_surface():
            pygame.display.set_mode((1, 1))

    def setUp(self):
        if not pygame.get_init():
            pygame.init()

        self.mock_surface = pygame.Surface((30, 30))
        self.mock_image = MagicMock()
        self.mock_image.convert_alpha.return_value = self.mock_surface
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_image)
        self.image_patcher.start()

        self.IncreasingFirePU = IncreasingFirePU
        self.RepairWallnutPU = RepairWallnutPU

        self.settings_model = SettingsModel()
        self.sound_manager = MagicMock(spec=SoundManager)
        self.player = Player((300, 500), self.settings_model)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.wallnut_manager = WallNutManager(
            player_position=(300, 570),
            screen_width=600,
            screen_height=600,
            sound_manager=self.sound_manager
        )
        self.wallnut_manager.place_all_wallnuts()
        self.powerup_manager = PowerUpManager()

    def tearDown(self):
        self.image_patcher.stop()
        if pygame.get_init():
            pygame.event.clear()

    def test_powerup_collected_on_player_overlap(self):
        # the player collects a power-up when they overlap, and the power-up is removed from the group
        
        # Spawn power-up exactly at player position
        self.powerup_manager.spawn_increasing_fire(self.player.rect.center)
        self.assertEqual(len(self.powerup_manager.powerup_group), 1)

        # Simulate collision (same as in run_game)
        collected = pygame.sprite.spritecollide(
            self.player, self.powerup_manager.powerup_group, dokill=True
        )

        self.assertEqual(len(collected), 1)
        self.assertEqual(len(self.powerup_manager.powerup_group), 0)
        print("Power-up removed from group when player overlaps it")

    def test_powerup_removed_after_collection(self):
        # after player collects power-up, it should be removed from the group (dokill=True)
        
        self.powerup_manager.spawn_repair_wallnut(self.player.rect.center)

        pygame.sprite.spritecollide(
            self.player, self.powerup_manager.powerup_group, dokill=True
        )

        self.assertEqual(len(self.powerup_manager.powerup_group), 0)
        print("Power-up removed from group after collection (dokill=True)")

if __name__ == '__main__':
    unittest.main()
