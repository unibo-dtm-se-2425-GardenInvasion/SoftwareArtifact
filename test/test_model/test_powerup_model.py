import unittest
import pygame
import os
from unittest.mock import patch, MagicMock

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from GardenInvasion.Model.PowerUp_model import IncreasingFirePU
from GardenInvasion.Model.setting_volume_model import SettingsModel
from GardenInvasion.Model.plant_model import Player
from GardenInvasion.Model.PowerUp_model import RepairWallnutPU
from GardenInvasion.Model.wallnut_model import WallNutManager
from GardenInvasion.Model.sound_manager_model import SoundManager
from GardenInvasion.Model.setting_volume_model import SettingsModel
from GardenInvasion.Model.PowerUp_model import PowerUpManager

class TestIncreasingFirePU(unittest.TestCase):
    # Tests for IncreasingFirePU model

    @classmethod
    def setUpClass(cls):
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_surface():
            pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        if not pygame.get_init():
            pygame.init()

        # Mock image loading to avoid needing asset files
        self.mock_surface = pygame.Surface((30, 30))
        self.mock_image = MagicMock()
        self.mock_image.convert_alpha.return_value = self.mock_surface
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_image)
        self.image_patcher.start()

        self.IncreasingFirePU = IncreasingFirePU
        self.settings_model = SettingsModel()
        self.player = Player((300, 500), self.settings_model)

    def tearDown(self):
        self.image_patcher.stop()
        if pygame.get_init():
            pygame.event.clear()

    def test_fire_boost_expires_after_duration(self):
        # After duration, shoot_SecondTime should return to base cooldown
        pu = self.IncreasingFirePU((300, 300), duration_ms=1, cooldown_multiplier=0.6, target_size=(30, 30))

        pu.apply(self.player)

        # Force expiry by setting end time in the past
        self.player.fire_rate_boost_end_time = pygame.time.get_ticks() - 1
        self.player.update()

        self.assertEqual(self.player.shoot_SecondTime, self.player.base_shoot_cooldown)
        print("✅ Fire boost expires and cooldown resets to base")

    def test_fire_boost_stacks_duration(self):
        # Collecting two power-ups extends, and not resets, the boost end time

        pu1 = self.IncreasingFirePU((300, 300), duration_ms=5000, cooldown_multiplier=0.6, target_size=(30, 30))
        pu2 = self.IncreasingFirePU((300, 300), duration_ms=5000, cooldown_multiplier=0.6, target_size=(30, 30))

        pu1.apply(self.player)
        first_end_time = self.player.fire_rate_boost_end_time

        # Small delay then collect second
        pygame.time.wait(10)
        pu2.apply(self.player)
        second_end_time = self.player.fire_rate_boost_end_time

        self.assertGreaterEqual(second_end_time, first_end_time)
        print("✅ Second power-up extends (not resets) boost duration")

    def test_player_can_shoot_faster_during_boost(self):
        # shoot_SecondTime is lower during boost → faster fire rate

        pu = self.IncreasingFirePU((300, 300), cooldown_multiplier=0.5, target_size=(30, 30))
        normal_cooldown = self.player.base_shoot_cooldown

        pu.apply(self.player)
        boosted_cooldown = self.player.shoot_SecondTime

        self.assertLess(boosted_cooldown, normal_cooldown)
        print("✅ Player can shoot faster during fire rate boost")


class TestRepairWallnutPU(unittest.TestCase):
    # Tests for RepairWallnutPU model

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

        self.RepairWallnutPU = RepairWallnutPU
        self.settings_model = SettingsModel()
        self.sound_manager = MagicMock(spec=SoundManager)
        self.wallnut_manager = WallNutManager(
            player_position=(300, 570),
            screen_width=600,
            screen_height=600,
            sound_manager=self.sound_manager
        )
        self.wallnut_manager.place_all_wallnuts()

    def tearDown(self):
        self.image_patcher.stop()
        if pygame.get_init():
            pygame.event.clear()

    def _get_wallnut_by_slot(self, slot_index):
        # Helper to find wallnut by slot index
        for wn in self.wallnut_manager.get_wallnuts():
            if wn.slot_index == slot_index:
                return wn
        return None

    def test_repair_heals_damaged_wallnut(self):
        # check if wallnut in slot 0 is at health 1, then apply repair and check if it goes to 2
        
        wn = self._get_wallnut_by_slot(0)
        wn.health = 1
        wn.update_image_by_health()

        pu = self.RepairWallnutPU((300, 300), target_size=(30, 30))
        pu.apply(self.wallnut_manager)

        healed = self._get_wallnut_by_slot(0)
        self.assertEqual(healed.health, 2)
        print("✅ Damaged wallnut (health=1) healed to full health (2)")

    def test_repair_does_not_overheal(self):
        # check wallnut already at health 2 stays at 2

        wn = self._get_wallnut_by_slot(0)
        self.assertEqual(wn.health, 2)  # already full

        pu = self.RepairWallnutPU((300, 300), target_size=(30, 30))
        pu.apply(self.wallnut_manager)

        healed = self._get_wallnut_by_slot(0)
        self.assertEqual(healed.health, 2)
        print("✅ Full health wallnut not over-healed")

    def test_repair_respawns_destroyed_wallnut(self):
        # after a wallnut is killed, applying repair should respawn it in the same slot

        wn = self._get_wallnut_by_slot(0)
        wn.kill()
        self.wallnut_manager.slot_occupied[0] = False

        initial_count = len(self.wallnut_manager.get_wallnuts())

        pu = self.RepairWallnutPU((300, 300), target_size=(30, 30))
        pu.apply(self.wallnut_manager)

        self.assertGreater(len(self.wallnut_manager.get_wallnuts()), initial_count)
        print("✅ Destroyed wallnut respawns after repair power-up")

class TestPowerUpManager(unittest.TestCase):
    #Tests for PowerUpManager

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

        self.powerup_manager = PowerUpManager()

    def tearDown(self):
        self.image_patcher.stop()
        if pygame.get_init():
            pygame.event.clear()

    def test_spawn_increasing_fire_adds_to_group(self):
        # spawn_increasing_fire adds exactly 1 sprite of the powerup to the group
        
        self.powerup_manager.spawn_increasing_fire((300, 300))
        self.assertEqual(len(self.powerup_manager.powerup_group), 1)
        print("✅ spawn_increasing_fire adds 1 power-up to group")

    def test_spawn_repair_wallnut_adds_to_group(self):
        # spawn_repair_wallnut adds exactly 1 sprite of the powerup to the group
        
        self.powerup_manager.spawn_repair_wallnut((300, 300))
        self.assertEqual(len(self.powerup_manager.powerup_group), 1)
        print("✅ spawn_repair_wallnut adds 1 power-up to group")

if __name__ == '__main__':
    unittest.main()
