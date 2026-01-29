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
    _handle_zombie_projectile_wallnut_collisions
)
from GardenInvasion.Model.menu_model import MenuModel
from GardenInvasion.Model.setting_volume_model import SettingsModel

class TestNewGameController(unittest.TestCase):
    # Test suite for NewGame controller

    def setUp(self):
        # Set up test fixtures
        self.mock_surface = pygame.Surface((100, 100))
        self.image_patcher = patch('pygame.image.load', return_value=self.mock_surface)
        self.image_patcher.start()

        self.screen = pygame.Surface((600, 600))
        self.menu_model = MenuModel()
        self.settings_model = SettingsModel()

    def tearDown(self):
        self.image_patcher.stop()
        pygame.event.clear()

    # TESTS FOR POINT 3: Zombie projectile → Wallnut collision
    def test_zombie_projectile_hits_wallnut(self):
        """Test che i proiettili zombie danneggiano i wallnut"""
        # Crea mock per gruppo proiettili zombie e wallnut manager
        zombie_projectile_group = pygame.sprite.Group()
        
        # Mock wallnut manager e wallnut group
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        # Crea mock wallnut
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = False  # Wallnut non distrutto
        mock_wallnut.slot_index = 0
        mock_wallnut_group.add(mock_wallnut)
        
        # Crea mock proiettile zombie
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        # Mock pygame.sprite.groupcollide per restituire collisione
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_wallnut]
            }
            
            # Esegui la funzione di collisione
            collision_occurred = _handle_zombie_projectile_wallnut_collisions(
                zombie_projectile_group, 
                mock_wallnut_manager
            )
            
            # Verifica
            self.assertTrue(collision_occurred)  # Collisione avvenuta
            mock_wallnut.take_damage.assert_called_once()  # Dovrebbe infliggere danno
            mock_collide.assert_called_once_with(
                zombie_projectile_group,
                mock_wallnut_group,
                True,   # rimuovi proiettile
                False   # non rimuovere wallnut (prendi danno invece)
            )
            print("✅ Zombie projectile damages wallnut")

    def test_zombie_projectile_destroys_wallnut(self):
        """Test quando un proiettile zombie distrugge il wallnut"""
        zombie_projectile_group = pygame.sprite.Group()
        
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = True  # Wallnut distrutto!
        mock_wallnut.slot_index = 1
        mock_wallnut_group.add(mock_wallnut)
        
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_wallnut]
            }
            
            collision_occurred = _handle_zombie_projectile_wallnut_collisions(
                zombie_projectile_group, 
                mock_wallnut_manager
            )
            
            self.assertTrue(collision_occurred)
            mock_wallnut.take_damage.assert_called_once()
            print("✅ Zombie projectile destroys wallnut")

    def test_multiple_zombie_projectiles_hit_wallnut(self):
        """Test collisione con multiple proiettili zombie su wallnut"""
        zombie_projectile_group = pygame.sprite.Group()
        
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = False
        mock_wallnut.slot_index = 2
        mock_wallnut_group.add(mock_wallnut)
        
        # Crea 3 proiettili mock
        mock_projectiles = [MagicMock() for _ in range(3)]
        for projectile in mock_projectiles:
            zombie_projectile_group.add(projectile)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            # Tutti i proiettili colpiscono lo stesso wallnut
            mock_collide.return_value = {
                mock_projectiles[0]: [mock_wallnut],
                mock_projectiles[1]: [mock_wallnut],
                mock_projectiles[2]: [mock_wallnut]
            }
            
            collision_occurred = _handle_zombie_projectile_wallnut_collisions(
                zombie_projectile_group, 
                mock_wallnut_manager
            )
            
            self.assertTrue(collision_occurred)
            # take_damage dovrebbe essere chiamato 3 volte
            self.assertEqual(mock_wallnut.take_damage.call_count, 3)
            print("✅ Multiple zombie projectiles damage wallnut")

    def test_no_zombie_projectile_wallnut_collision_returns_false(self):
        """Test che restituisce False quando non ci sono collisioni con wallnut"""
        zombie_projectile_group = pygame.sprite.Group()
        
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {}  # Nessuna collisione
            
            collision_occurred = _handle_zombie_projectile_wallnut_collisions(
                zombie_projectile_group, 
                mock_wallnut_manager
            )
            
            self.assertFalse(collision_occurred)
            mock_collide.assert_called_once()
            print("✅ No zombie projectile-wallnut collision returns False")

    def test_zombie_projectile_hits_multiple_wallnuts(self):
        """Test collisione proiettile zombie con multiple wallnuts (edge case)"""
        zombie_projectile_group = pygame.sprite.Group()
        
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        # Crea 3 wallnut mock
        mock_wallnut1 = MagicMock()
        mock_wallnut1.take_damage.return_value = False
        mock_wallnut1.slot_index = 0
        
        mock_wallnut2 = MagicMock()
        mock_wallnut2.take_damage.return_value = True  # Distrutto
        mock_wallnut2.slot_index = 1
        
        mock_wallnut3 = MagicMock()
        mock_wallnut3.take_damage.return_value = False
        mock_wallnut3.slot_index = 2
        
        mock_wallnut_group.add(mock_wallnut1, mock_wallnut2, mock_wallnut3)
        
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_wallnut1, mock_wallnut2, mock_wallnut3]
            }
            
            collision_occurred = _handle_zombie_projectile_wallnut_collisions(
                zombie_projectile_group, 
                mock_wallnut_manager
            )
            
            self.assertTrue(collision_occurred)
            # Ogni wallnut dovrebbe prendere danno
            mock_wallnut1.take_damage.assert_called_once()
            mock_wallnut2.take_damage.assert_called_once()
            mock_wallnut3.take_damage.assert_called_once()
            print("✅ Zombie projectile hits multiple wallnuts")

    def test_zombie_projectile_wallnut_collision_with_sound_manager(self):
        """Test collisione con sound manager (il suono è gestito in wallnut.take_damage())"""
        zombie_projectile_group = pygame.sprite.Group()
        
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = False
        mock_wallnut.slot_index = 3
        mock_wallnut_group.add(mock_wallnut)
        
        mock_sound_manager = MagicMock()
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_wallnut]
            }
            
            collision_occurred = _handle_zombie_projectile_wallnut_collisions(
                zombie_projectile_group, 
                mock_wallnut_manager,
                mock_sound_manager
            )
            
            self.assertTrue(collision_occurred)
            mock_wallnut.take_damage.assert_called_once()
            print("✅ Zombie projectile-wallnut collision with sound manager parameter")

    def test_zombie_projectile_removed_on_wallnut_hit(self):
        """Test che i proiettili zombie vengono rimossi dopo collisione con wallnut"""
        zombie_projectile_group = pygame.sprite.Group()
        
        mock_wallnut_manager = MagicMock()
        mock_wallnut_group = pygame.sprite.Group()
        mock_wallnut_manager.get_wallnuts.return_value = mock_wallnut_group
        
        mock_wallnut = MagicMock()
        mock_wallnut.take_damage.return_value = False
        mock_wallnut_group.add(mock_wallnut)
        
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_wallnut]
            }
            
            _handle_zombie_projectile_wallnut_collisions(
                zombie_projectile_group, 
                mock_wallnut_manager
            )
            
            # Verifica che groupcollide sia chiamato con True per rimuovere proiettile
            mock_collide.assert_called_once_with(
                zombie_projectile_group,
                mock_wallnut_group,
                True,   # rimuovi proiettile
                False   # non rimuovere wallnut
            )
            print("✅ Zombie projectile removed on wallnut hit")

    # NUOVO TEST: Collisione proiettile zombie → pianta
    def test_zombie_projectile_hits_plant(self):
        """Test che i proiettili zombie danneggiano la pianta"""
        # Crea mock per gruppo proiettili zombie e player
        zombie_projectile_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = False  # Pianta non distrutta
        
        # Crea mock proiettile zombie
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        # Mock pygame.sprite.spritecollide per restituire collisione
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = [mock_projectile]
            
            # Esegui la funzione di collisione
            plant_destroyed = _handle_zombie_projectile_plant_collisions(
                zombie_projectile_group, 
                mock_player
            )
            
            # Verifica
            self.assertFalse(plant_destroyed)  # Pianta non distrutta
            mock_player.take_damage.assert_called_once()  # Dovrebbe infliggere danno
            mock_spritecollide.assert_called_once_with(
                mock_player,
                zombie_projectile_group,
                True,  # rimuovi proiettile
                pygame.sprite.collide_rect
            )
            print("✅ Zombie projectile damages plant")

    def test_zombie_projectile_destroys_plant(self):
        """Test quando un proiettile zombie distrugge la pianta"""
        zombie_projectile_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = True  # Pianta distrutta!
        
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = [mock_projectile]
            
            plant_destroyed = _handle_zombie_projectile_plant_collisions(
                zombie_projectile_group, 
                mock_player
            )
            
            self.assertTrue(plant_destroyed)  # Pianta distrutta
            mock_player.take_damage.assert_called_once()
            print("✅ Zombie projectile destroys plant")

    def test_multiple_zombie_projectiles_hit_plant(self):
        """Test collisione con multiple proiettili zombie"""
        zombie_projectile_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = False
        
        # Crea 3 proiettili mock
        mock_projectiles = [MagicMock() for _ in range(3)]
        for projectile in mock_projectiles:
            zombie_projectile_group.add(projectile)
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = mock_projectiles
            
            plant_destroyed = _handle_zombie_projectile_plant_collisions(
                zombie_projectile_group, 
                mock_player
            )
            
            self.assertFalse(plant_destroyed)
            # take_damage dovrebbe essere chiamato 3 volte (uno per proiettile)
            self.assertEqual(mock_player.take_damage.call_count, 3)
            print("✅ Multiple zombie projectiles damage plant")

    def test_no_zombie_projectile_collision_returns_false(self):
        """Test che restituisce False quando non ci sono collisioni"""
        zombie_projectile_group = pygame.sprite.Group()
        mock_player = MagicMock()
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = []  # Nessuna collisione
            
            plant_destroyed = _handle_zombie_projectile_plant_collisions(
                zombie_projectile_group, 
                mock_player
            )
            
            self.assertFalse(plant_destroyed)
            mock_player.take_damage.assert_not_called()  # Nessun danno
            print("✅ No zombie projectile collision returns False")

    def test_zombie_projectile_removed_on_hit(self):
        """Test che i proiettili zombie vengono rimossi dopo collisione"""
        zombie_projectile_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = False
        
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = [mock_projectile]
            
            _handle_zombie_projectile_plant_collisions(zombie_projectile_group, mock_player)
            
            # Verifica che spritecollide sia chiamato con True per rimuovere proiettile
            mock_spritecollide.assert_called_once_with(
                mock_player,
                zombie_projectile_group,
                True,  # rimuovi proiettile
                pygame.sprite.collide_rect
            )
            print("✅ Zombie projectile removed on plant hit")

    # Test per sound manager (opzionale)
    def test_zombie_projectile_collision_with_sound_manager(self):
        """Test collisione con sound manager (se implementato in futuro)"""
        zombie_projectile_group = pygame.sprite.Group()
        mock_player = MagicMock()
        mock_player.take_damage.return_value = False
        
        mock_sound_manager = MagicMock()
        mock_projectile = MagicMock()
        zombie_projectile_group.add(mock_projectile)
        
        with patch('pygame.sprite.spritecollide') as mock_spritecollide:
            mock_spritecollide.return_value = [mock_projectile]
            
            plant_destroyed = _handle_zombie_projectile_plant_collisions(
                zombie_projectile_group, 
                mock_player,
                mock_sound_manager
            )
            
            self.assertFalse(plant_destroyed)
            mock_player.take_damage.assert_called_once()
            # Nota: al momento non viene chiamato play_sound, ma potrebbe in futuro
            print("✅ Zombie projectile collision with sound manager parameter")

    def test_projectile_zombie_collision_damages_zombie(self):
        """Test che le collisioni proiettile-zombie infliggono danno"""
        # Crea gruppi mock
        projectile_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        # Crea mock per proiettile e zombie
        mock_projectile = MagicMock()
        mock_zombie = MagicMock()
        mock_zombie.take_damage.return_value = False  # Zombie non distrutto
        
        # Aggiungi agli sprite group
        projectile_group.add(mock_projectile)
        zombie_group.add(mock_zombie)
        
        # Mock pygame.sprite.groupcollide per restituire collisione
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_zombie]
            }
            
            # Esegui la funzione di collisione
            result = _handle_projectile_zombie_collisions(projectile_group, zombie_group)
            
            # Verifica
            self.assertTrue(result)  # Dovrebbe restituire True (collisione avvenuta)
            mock_zombie.take_damage.assert_called_once_with(1)  # Dovrebbe infliggere 1 danno
            print("✅ Projectile-zombie collision damages zombie")

    def test_projectile_zombie_collision_removes_projectile(self):
        """Test che i proiettili vengono rimossi dopo collisione"""
        # Crea gruppi mock
        projectile_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        # Crea mock
        mock_projectile = MagicMock()
        mock_zombie = MagicMock()
        mock_zombie.take_damage.return_value = False
        
        projectile_group.add(mock_projectile)
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_zombie]
            }
            
            _handle_projectile_zombie_collisions(projectile_group, zombie_group)
            
            # Verifica che groupcollide sia chiamato con True per rimuovere proiettile
            mock_collide.assert_called_once_with(
                projectile_group,
                zombie_group,
                True,   # rimuovi proiettile
                False   # non rimuovere zombie (prendi danno invece)
            )
            print("✅ Projectile removed on zombie collision")

    def test_projectile_zombie_collision_zombie_destroyed(self):
        """Test quando zombie viene distrutto dalla collisione"""
        projectile_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        mock_projectile = MagicMock()
        mock_zombie = MagicMock()
        mock_zombie.take_damage.return_value = True  # Zombie distrutto!
        
        projectile_group.add(mock_projectile)
        zombie_group.add(mock_zombie)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_zombie]
            }
            
            result = _handle_projectile_zombie_collisions(projectile_group, zombie_group)
            
            self.assertTrue(result)
            mock_zombie.take_damage.assert_called_once_with(1)
            print("✅ Zombie destroyed by projectile collision")

    def test_no_collision_returns_false(self):
        """Test che restituisce False quando non ci sono collisioni"""
        projectile_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {}  # Nessuna collisione
            
            result = _handle_projectile_zombie_collisions(projectile_group, zombie_group)
            
            self.assertFalse(result)
            print("✅ No collision returns False")

    def test_multiple_zombies_hit_by_same_projectile(self):
        """Test collisione con multiple zombie (edge case)"""
        projectile_group = pygame.sprite.Group()
        zombie_group = pygame.sprite.Group()
        
        mock_projectile = MagicMock()
        mock_zombie1 = MagicMock()
        mock_zombie2 = MagicMock()
        mock_zombie1.take_damage.return_value = False
        mock_zombie2.take_damage.return_value = True
        
        projectile_group.add(mock_projectile)
        zombie_group.add(mock_zombie1, mock_zombie2)
        
        with patch('pygame.sprite.groupcollide') as mock_collide:
            mock_collide.return_value = {
                mock_projectile: [mock_zombie1, mock_zombie2]
            }
            
            result = _handle_projectile_zombie_collisions(projectile_group, zombie_group)
            
            self.assertTrue(result)
            mock_zombie1.take_damage.assert_called_once_with(1)
            mock_zombie2.take_damage.assert_called_once_with(1)
            print("✅ Multiple zombies hit by same projectile")

    @unittest.skip("Test complesso di integrazione WaveManager - richiede mock estensivi del game loop. "
                   "Da implementare quando il sistema di collisioni sarà completo e stabile.")
    def test_wave_manager_integrated_in_game_loop(self):
        """Test che WaveManager sia integrato nel game loop"""
        # NOTE: Questo test verrà implementato successivamente quando
        # tutte le collisioni saranno sviluppate e il sistema sarà stabile.
        # Attualmente richiederebbe mock troppo complessi del game loop completo.
        pass

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_escape_opens_pause_menu(self, mock_flip, mock_draw):
        # Test that ESC shows pause modal

        # Simulate ESC key, then Resume
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],  # Resume
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'resume')
        print("✅ ESC opens pause menu")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_resume_continues_game(self, mock_flip, mock_draw):
        # Test that Resume returns to gameplay

        # Select Resume (default selection is 1)
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'resume')
        print("✅ Resume continues gameplay")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_main_menu_exits(self, mock_flip, mock_draw):
        # Test that Main Menu exits game loop

        # Navigate left to Main Menu (index 0) and select
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'menu')
        print("✅ Main Menu exits game loop")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_pause_menu_quit_exits_application(self, mock_flip, mock_draw):
        # Test that Quit closes game

        # Navigate right to Quit (index 2) and select
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'quit')
        print("✅ Quit exits application")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('pygame.display.flip')
    def test_left_right_navigation_in_pause(self, mock_flip, mock_draw):
        # Test navigating pause menu buttons with LEFT/RIGHT

        # Navigate left, then right, then select
        events_sequence = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],   # To Main Menu
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],  # To Resume
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})],  # To Quit
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})],   # Back to Resume
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})], # Select Resume
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'resume')
        print("✅ LEFT/RIGHT navigation works in pause menu")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('GardenInvasion.Controller.NewGame_controller.get_pause_menu_button_rects')
    @patch('pygame.display.flip')
    def test_mouse_click_resume(self, mock_flip, mock_rects, mock_draw):
        # Test clicking Resume button

        # Mock button rects
        resume_rect = pygame.Rect(230, 300, 140, 50)
        mock_rects.return_value = (pygame.Rect(0, 0, 140, 50), resume_rect, pygame.Rect(0, 0, 140, 50))

        # Simulate mouse motion over Resume, then click
        events_sequence = [
            [pygame.event.Event(pygame.MOUSEMOTION, {'pos': (300, 325)})],
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (300, 325)})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'resume')
        print("✅ Mouse click on Resume works")

    @patch('GardenInvasion.Controller.NewGame_controller.draw_pause_modal')
    @patch('GardenInvasion.Controller.NewGame_controller.get_pause_menu_button_rects')
    @patch('pygame.display.flip')
    def test_mouse_click_quit(self, mock_flip, mock_rects, mock_draw):
        # Test clicking Quit button
        
        # Mock button rects
        quit_rect = pygame.Rect(390, 300, 140, 50)
        mock_rects.return_value = (pygame.Rect(0, 0, 140, 50), pygame.Rect(0, 0, 140, 50), quit_rect)

        # Simulate mouse motion over Quit, then click
        events_sequence = [
            [pygame.event.Event(pygame.MOUSEMOTION, {'pos': (460, 325)})],
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (460, 325)})],
            []
        ]

        with patch('pygame.event.get', side_effect=events_sequence):
            result = show_pause_menu(self.screen, self.menu_model)

        self.assertEqual(result, 'quit')
        print("✅ Mouse click on Quit works")

if __name__ == '__main__':
    unittest.main()