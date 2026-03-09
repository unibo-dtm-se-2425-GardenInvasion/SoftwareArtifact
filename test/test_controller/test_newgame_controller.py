import unittest
import pygame
from unittest.mock import patch, MagicMock, call
import sys

pygame.init()
pygame.display.set_mode((1, 1))

from GardenInvasion.Controller.NewGame_controller import (
    show_pause_menu, 
    run_game, 
    _handle_projectile_zombie_collisions,
    _handle_zombie_projectile_plant_collisions,
    _handle_zombie_projectile_wallnut_collisions,
    _handle_zombie_wallnut_collisions,
    _handle_zombie_plant_collisions
)
from GardenInvasion.Model.menu_model import MenuModel
from GardenInvasion.Model.setting_volume_model import SettingsModel

class TestNewGameController(unittest.TestCase):
    # Test suite for NewGame controller

    def setUp(self):
        self.mock_surface = pygame.Surface((100, 100))
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.image_patcher.start()

        self.screen = pygame.Surface((600, 600))
        self.menu_model = MenuModel()
        self.settings_model = SettingsModel()

    def tearDown(self):
        self.image_patcher.stop()
        pygame.event.clear()

    def test_zombie_hits_plant_damage(self):
        # zombie damages plant but doesn't destroy it
        
        zombie_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.life_points = 2
        mock_player.take_damage.return_value = False
        
        mock_zombie = MagicMock()
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = [mock_zombie]
            plant_destroyed = _handle_zombie_plant_collisions(zombie_group, mock_player)
            
            self.assertFalse(plant_destroyed)
            mock_player.take_damage.assert_called_once()
            mock_spritecollide.assert_called_once_with(mock_player, zombie_group, True, pygame.sprite.collide_rect)
            print("Zombie → Plant: damage & removal OK")

    def test_zombie_destroys_plant(self):
        # zombie damages plant and destroys it

        zombie_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = True
        
        mock_zombie = MagicMock()
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = [mock_zombie]
            plant_destroyed = _handle_zombie_plant_collisions(zombie_group, mock_player)
            
            self.assertTrue(plant_destroyed)
            print("Zombie → Plant: destroys plant")

    def test_no_zombie_plant_collision(self):
        # no collision between zombie and plant
        zombie_group = pygame.sprite.Group()
        mock_player = MagicMock()
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = []
            plant_destroyed = _handle_zombie_plant_collisions(zombie_group, mock_player)
            
            self.assertFalse(plant_destroyed)
            mock_player.take_damage.assert_not_called()
            print("Zombie → Plant: no collision OK")

    def test_zombie_hits_wallnut_damage(self):
        # zombie hits wallnut, wallnut takes damage but isn't destroyed

        zombie_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = False
        mock_wallnut_group.add(mock_wallnut)
        mock_zombie = MagicMock()
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {mock_zombie: [mock_wallnut]}
            collision = _handle_zombie_wallnut_collisions(zombie_group, mock_wallnut_manager)
            
            self.assertTrue(collision)
            mock_wallnut.take_damage.assert_called_once()
            mock_collide.assert_called_once_with(zombie_group, mock_wallnut_group, True, False)
            print("Zombie → Wallnut: damage & removal OK")

    def test_zombie_destroys_wallnut(self):
        # zombie hits wallnut, wallnut takes damage and is destroyed
        zombie_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = True
        mock_wallnut_group.add(mock_wallnut)
        mock_zombie = MagicMock()
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {mock_zombie: [mock_wallnut]}
            collision = _handle_zombie_wallnut_collisions(zombie_group, mock_wallnut_manager)
            
            self.assertTrue(collision)
            print("Zombie → Wallnut: destroys wallnut")

    def test_no_zombie_wallnut_collision(self):
        # no collision between zombie and wallnut
        zombie_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {}
            collision = _handle_zombie_wallnut_collisions(zombie_group, mock_wallnut_manager)
            
            self.assertFalse(collision)
            print("Zombie → Wallnut: no collision OK")

    def test_zombie_projectile_hits_wallnut_damage(self):
        # zombie projectile hits wallnut, wallnut takes damage but isn't destroyed
        proj_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = False
        mock_wallnut_group.add(mock_wallnut)
        mock_proj = MagicMock()
        proj_group.add(mock_proj)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {mock_proj: [mock_wallnut]}
            collision = _handle_zombie_projectile_wallnut_collisions(proj_group, mock_wallnut_manager)
            
            self.assertTrue(collision)
            mock_wallnut.take_damage.assert_called_once()
            mock_collide.assert_called_once_with(proj_group, mock_wallnut_group, True, False)
            print("Zombie projectile → Wallnut: damage OK")

    def test_zombie_projectile_destroys_wallnut(self):
        # wallnut takes damage and is destroyed by zombie projectile
        proj_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = True
        mock_wallnut_group.add(mock_wallnut)
        mock_proj = MagicMock()
        proj_group.add(mock_proj)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {mock_proj: [mock_wallnut]}
            collision = _handle_zombie_projectile_wallnut_collisions(proj_group, mock_wallnut_manager)
            
            self.assertTrue(collision)
            print("Zombie projectile → Wallnut: destroys wallnut")

    def test_no_projectile_wallnut_collision(self):
        # no collision between zombie projectile and wallnut
        proj_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {}
            collision = _handle_zombie_projectile_wallnut_collisions(proj_group, mock_wallnut_manager)
            
            self.assertFalse(collision)
            print("Zombie projectile → Wallnut: no collision OK")

    def test_zombie_projectile_hits_plant_damage(self):
        # zombie projectile hits plant, plant takes damage but isn't destroyed
        proj_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = False
        
        mock_proj = MagicMock()
        proj_group.add(mock_proj)
        
        with patch('pygame.sprite.spritecollide') as mock_collide:
            mock_collide.return_value = [mock_proj]
            destroyed = _handle_zombie_projectile_plant_collisions(proj_group, mock_player)
            
            self.assertFalse(destroyed)
            mock_player.take_damage.assert_called_once()
            mock_collide.assert_called_once_with(mock_player, proj_group, True, pygame.sprite.collide_rect)
            print("Zombie projectile → Plant: damage OK")

    def test_zombie_projectile_destroys_plant(self):
        # zombie projectile hits plant, plant takes damage and is destroyed
        proj_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = True
        
        mock_proj = MagicMock()
        proj_group.add(mock_proj)
        
        with patch('pygame.sprite.spritecollide') as mock_collide:
            mock_collide.return_value = [mock_proj]
            destroyed = _handle_zombie_projectile_plant_collisions(proj_group, mock_player)
            
            self.assertTrue(destroyed)
            print("Zombie projectile → Plant: destroys plant")

    def test_projectile_hits_zombie_damage(self):
        # projectile hits zombie, zombie takes damage but isn't destroyed
        proj_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        mock_proj = MagicMock()
        mock_zombie = MagicMock()
        mock_zombie.take_damage.return_value = False
        
        proj_group.add(mock_proj)
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {mock_proj: [mock_zombie]}
            result = _handle_projectile_zombie_collisions(proj_group, zombie_group)
            
            self.assertTrue(result)
            mock_zombie.take_damage.assert_called_once_with(1)
            mock_collide.assert_called_once_with(proj_group, zombie_group, True, False)
            print("Projectile → Zombie: damage OK")

    def test_projectile_destroys_zombie(self):
        # projectile hits zombie, zombie takes damage and is destroyed
        proj_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        mock_proj = MagicMock()
        mock_zombie = MagicMock()
        mock_zombie.take_damage.return_value = True
        
        proj_group.add(mock_proj)
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {mock_proj: [mock_zombie]}
            result = _handle_projectile_zombie_collisions(proj_group, zombie_group)
            
            self.assertTrue(result)
            print("Projectile → Zombie: destroys zombie")

    def test_no_projectile_zombie_collision(self):
        # projectile does not hit zombie
        proj_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {}
            result = _handle_projectile_zombie_collisions(proj_group, zombie_group)
            
            self.assertFalse(result)
            print("Projectile → Zombie: no collision OK")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_escape_opens_menu(self, mock_flip, mock_draw):
        # press ESC to open pause menu, then press ESC again to resume
        
        events = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})],
            []
        ]
        with patch('pygame.event.get', side_effect=events):
            result = show_pause_menu(self.screen, self.menu_model)
        self.assertEqual(result, 'resume')
        print("Pause menu: ESC opens menu and ESC resumes")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_navigation(self, mock_flip, mock_draw):
        # test quitting the game from pause menu
        events_quit = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            []
        ]
        with patch('pygame.event.get', side_effect=events_quit):
            result = show_pause_menu(self.screen, self.menu_model)
        self.assertEqual(result, 'quit')
        
        events_menu = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            []
        ]
        with patch('pygame.event.get', side_effect=events_menu):
            result = show_pause_menu(self.screen, self.menu_model)
        self.assertEqual(result, 'menu')
        
        print("Pause menu: navigation OK")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('GardenInvasion.Controller.NewGame_controller.get_pause_menu_button_rects')
    @patch('pygame.display.flip')
    def test_pause_menu_mouse_click(self, mock_flip, mock_rects, mock_draw):
        # test clicking the "Resume" button in the pause menu 
        resume_rect = pygame.Rect(230, 300, 140, 50)
        mock_rects.return_value = (pygame.Rect(0,0,140,50), resume_rect, pygame.Rect(0,0,140,50))
        
        events = [
            [pygame.event.Event(pygame.MOUSEMOTION, {'pos': (300, 325)})],
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (300, 325)})],
            []
        ]
        with patch('pygame.event.get', side_effect=events):
            result = show_pause_menu(self.screen, self.menu_model)
        self.assertEqual(result, 'resume')
        print("Pause menu: mouse click OK")

if __name__ == '__main__':
    unittest.main()