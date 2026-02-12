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

    # ---------- PUNTO 5: Zombie → Plant (TEST ESSENZIALI) ----------
    def test_zombie_hits_plant_damage(self):
        """Test base: zombie distrutto, pianta danneggiata"""
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
            print("✅ Zombie → Plant: damage & removal OK")

    def test_zombie_destroys_plant(self):
        """Test distruzione pianta"""
        zombie_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = True
        
        mock_zombie = MagicMock()
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = [mock_zombie]
            plant_destroyed = _handle_zombie_plant_collisions(zombie_group, mock_player)
            
            self.assertTrue(plant_destroyed)
            print("✅ Zombie → Plant: destroys plant")

    def test_multiple_zombies_hit_plant(self):
        """Test multipli zombie sulla pianta"""
        zombie_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.side_effect = [False, True]
        
        mock_zombies = [MagicMock() for _ in range(2)]
        for z in mock_zombies:
            zombie_group.add(z)
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = mock_zombies
            plant_destroyed = _handle_zombie_plant_collisions(zombie_group, mock_player)
            
            self.assertTrue(plant_destroyed)
            self.assertEqual(mock_player.take_damage.call_count, 2)
            print("✅ Zombie → Plant: multiple hits OK")

    def test_no_zombie_plant_collision(self):
        """Test nessuna collisione"""
        zombie_group = pygame.sprite.Group()
        mock_player = MagicMock()
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = []
            plant_destroyed = _handle_zombie_plant_collisions(zombie_group, mock_player)
            
            self.assertFalse(plant_destroyed)
            mock_player.take_damage.assert_not_called()
            print("✅ Zombie → Plant: no collision OK")

    # ---------- PUNTO 4: Zombie → Wallnut (TEST ESSENZIALI) ----------
    def test_zombie_hits_wallnut_damage(self):
        """Test base: zombie distrutto, wallnut danneggiato"""
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
            print("✅ Zombie → Wallnut: damage & removal OK")

    def test_zombie_destroys_wallnut(self):
        """Test distruzione wallnut"""
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
            print("✅ Zombie → Wallnut: destroys wallnut")

    def test_multiple_zombies_hit_wallnut(self):
        """Test multipli zombie su stesso wallnut"""
        zombie_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = False
        mock_wallnut_group.add(mock_wallnut)
        
        mock_zombies = [MagicMock() for _ in range(3)]
        for z in mock_zombies:
            zombie_group.add(z)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {z: [mock_wallnut] for z in mock_zombies}
            collision = _handle_zombie_wallnut_collisions(zombie_group, mock_wallnut_manager)
            
            self.assertTrue(collision)
            self.assertEqual(mock_wallnut.take_damage.call_count, 3)
            print("✅ Zombie → Wallnut: multiple hits OK")

    def test_no_zombie_wallnut_collision(self):
        """Test nessuna collisione"""
        zombie_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {}
            collision = _handle_zombie_wallnut_collisions(zombie_group, mock_wallnut_manager)
            
            self.assertFalse(collision)
            print("✅ Zombie → Wallnut: no collision OK")

    # ---------- PUNTO 3: Zombie projectile → Wallnut (TEST ESSENZIALI) ----------
    def test_zombie_projectile_hits_wallnut_damage(self):
        """Test base: proiettile rimosso, wallnut danneggiato"""
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
            print("✅ Zombie projectile → Wallnut: damage OK")

    def test_zombie_projectile_destroys_wallnut(self):
        """Test distruzione wallnut"""
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
            print("✅ Zombie projectile → Wallnut: destroys wallnut")

    def test_multiple_projectiles_hit_wallnut(self):
        """Test multipli proiettili su stesso wallnut"""
        proj_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = False
        mock_wallnut_group.add(mock_wallnut)
        
        mock_projs = [MagicMock() for _ in range(3)]
        for p in mock_projs:
            proj_group.add(p)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {p: [mock_wallnut] for p in mock_projs}
            collision = _handle_zombie_projectile_wallnut_collisions(proj_group, mock_wallnut_manager)
            
            self.assertTrue(collision)
            self.assertEqual(mock_wallnut.take_damage.call_count, 3)
            print("✅ Zombie projectile → Wallnut: multiple hits OK")

    def test_no_projectile_wallnut_collision(self):
        """Test nessuna collisione"""
        proj_group = pygame.sprite.Group()
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {}
            collision = _handle_zombie_projectile_wallnut_collisions(proj_group, mock_wallnut_manager)
            
            self.assertFalse(collision)
            print("✅ Zombie projectile → Wallnut: no collision OK")

    # ---------- PUNTO 2: Zombie projectile → Plant (TEST ESSENZIALI) ----------
    def test_zombie_projectile_hits_plant_damage(self):
        """Test base: proiettile rimosso, pianta danneggiata"""
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
            print("✅ Zombie projectile → Plant: damage OK")

    def test_zombie_projectile_destroys_plant(self):
        """Test distruzione pianta"""
        proj_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = True
        
        mock_proj = MagicMock()
        proj_group.add(mock_proj)
        
        with patch('pygame.sprite.spritecollide') as mock_collide:
            mock_collide.return_value = [mock_proj]
            destroyed = _handle_zombie_projectile_plant_collisions(proj_group, mock_player)
            
            self.assertTrue(destroyed)
            print("✅ Zombie projectile → Plant: destroys plant")

    def test_multiple_projectiles_hit_plant(self):
        """Test multipli proiettili sulla pianta"""
        proj_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = False
        
        mock_projs = [MagicMock() for _ in range(3)]
        for p in mock_projs:
            proj_group.add(p)
        
        with patch('pygame.sprite.spritecollide') as mock_collide:
            mock_collide.return_value = mock_projs
            destroyed = _handle_zombie_projectile_plant_collisions(proj_group, mock_player)
            
            self.assertFalse(destroyed)
            self.assertEqual(mock_player.take_damage.call_count, 3)
            print("✅ Zombie projectile → Plant: multiple hits OK")

    # ---------- PUNTO 1: Projectile → Zombie (TEST ESSENZIALI) ----------
    def test_projectile_hits_zombie_damage(self):
        """Test base: proiettile rimosso, zombie danneggiato"""
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
            print("✅ Projectile → Zombie: damage OK")

    def test_projectile_destroys_zombie(self):
        """Test distruzione zombie"""
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
            print("✅ Projectile → Zombie: destroys zombie")

    def test_multiple_zombies_hit_by_projectile(self):
        """Test proiettile colpisce multipli zombie (edge case utile)"""
        proj_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        mock_proj = MagicMock()
        mock_zombie1 = MagicMock()
        mock_zombie2 = MagicMock()
        mock_zombie1.take_damage.return_value = False
        mock_zombie2.take_damage.return_value = False
        
        proj_group.add(mock_proj)
        zombie_group.add(mock_zombie1, mock_zombie2)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {mock_proj: [mock_zombie1, mock_zombie2]}
            result = _handle_projectile_zombie_collisions(proj_group, zombie_group)
            
            self.assertTrue(result)
            self.assertEqual(mock_zombie1.take_damage.call_count, 1)
            self.assertEqual(mock_zombie2.take_damage.call_count, 1)
            print("✅ Projectile → Zombie: hits multiple OK")

    def test_no_projectile_zombie_collision(self):
        """Test nessuna collisione"""
        proj_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {}
            result = _handle_projectile_zombie_collisions(proj_group, zombie_group)
            
            self.assertFalse(result)
            print("✅ Projectile → Zombie: no collision OK")

    # ---------- PAUSE MENU (TEST ESSENZIALI - 5 TEST) ----------
    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_escape_opens_menu(self, mock_flip, mock_draw):
        """Test che ESC apra il menu e ESC stesso faccia resume"""
        events = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})],  # Apre menu
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})],  # ESC = resume
            []
        ]
        with patch('pygame.event.get', side_effect=events):
            result = show_pause_menu(self.screen, self.menu_model)
        self.assertEqual(result, 'resume')
        print("✅ Pause menu: ESC opens menu and ESC resumes")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_quit_selection(self, mock_flip, mock_draw):
        """Test selezione Quit con tastiera (RIGHT → RETURN)"""
        events = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],  # Da Resume a Quit
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})], # Seleziona Quit
            []
        ]
        with patch('pygame.event.get', side_effect=events):
            result = show_pause_menu(self.screen, self.menu_model)
        self.assertEqual(result, 'quit')
        print("✅ Pause menu: quit selection OK")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_main_menu_selection(self, mock_flip, mock_draw):
        """Test selezione Main Menu con tastiera (LEFT → RETURN)"""
        events = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],   # Da Resume a Main Menu
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})], # Seleziona Main Menu
            []
        ]
        with patch('pygame.event.get', side_effect=events):
            result = show_pause_menu(self.screen, self.menu_model)
        self.assertEqual(result, 'menu')
        print("✅ Pause menu: main menu selection OK")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_resume_selection(self, mock_flip, mock_draw):
        """Test selezione Resume con tastiera (RETURN diretto)"""
        events = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})], # Seleziona Resume (default)
            []
        ]
        with patch('pygame.event.get', side_effect=events):
            result = show_pause_menu(self.screen, self.menu_model)
        self.assertEqual(result, 'resume')
        print("✅ Pause menu: resume selection OK")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('GardenInvasion.Controller.NewGame_controller.get_pause_menu_button_rects')
    @patch('pygame.display.flip')
    def test_pause_menu_mouse_click_resume(self, mock_flip, mock_rects, mock_draw):
        """Test click del mouse su Resume"""
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
        print("✅ Pause menu: mouse click on Resume OK")

    @unittest.skip("Test integrazione - richiede mock complessi")
    def test_wave_manager_integration(self):
        pass

if __name__ == '__main__':
    unittest.main()