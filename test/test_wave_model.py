import unittest
import pygame
import sys
import os

# Setup dei path corretti
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
my_project_path = os.path.join(project_root, 'my_project')
sys.path.insert(0, my_project_path)

from Model.wave_model import WaveManager
from Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class TestWaveModel(unittest.TestCase):
    """Test per la classe WaveManager con ondata 5 migliorata"""
    
    def setUp(self):
        """Setup prima di ogni test"""
        pygame.init()
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        pygame.quit()
    
    def test_wave_manager_creation(self):
        """Test creazione WaveManager"""
        wave_manager = WaveManager()
        
        self.assertEqual(wave_manager.current_wave, 0)
        self.assertEqual(wave_manager.total_waves, 5)
        self.assertTrue(wave_manager.wave_complete)
        self.assertEqual(len(wave_manager.zombie_group), 0)
        self.assertEqual(len(wave_manager.zombie_projectile_group), 0)
    
    def test_spawn_points(self):
        """Test che i punti di spawn siano corretti"""
        wave_manager = WaveManager()
        
        # Verifica che tutti i punti di spawn esistano
        expected_points = ['A', 'B', 'C', 'D', 'E']
        for point in expected_points:
            self.assertIn(point, wave_manager.spawn_points)
        
        # Verifica posizioni approssimative
        self.assertEqual(wave_manager.spawn_points['A'][0], SCREEN_WIDTH // 2)
        self.assertEqual(wave_manager.spawn_points['B'][0], SCREEN_WIDTH // 3)
        self.assertEqual(wave_manager.spawn_points['C'][0], SCREEN_WIDTH * 2 // 3)
        self.assertEqual(wave_manager.spawn_points['D'][0], SCREEN_WIDTH // 4)
        self.assertEqual(wave_manager.spawn_points['E'][0], SCREEN_WIDTH * 3 // 4)
        
        # Tutti dovrebbero spawnare sopra lo schermo
        for point in wave_manager.spawn_points.values():
            self.assertEqual(point[1], -50)
    
    def test_first_wave_start(self):
        """Test avvio prima ondata"""
        wave_manager = WaveManager()
        
        # Avvia prima ondata
        wave_manager.start_first_wave()
        
        self.assertTrue(wave_manager.waiting_for_next_wave)
        self.assertGreater(wave_manager.next_wave_timer, 0)
    
    def test_wave_1_spawn(self):
        """Test spawn ondata 1"""
        wave_manager = WaveManager()
        wave_manager.current_wave = 1
        wave_manager._wave_1()
        
        # Ondata 1 dovrebbe avere 1 zombie rosso
        self.assertEqual(len(wave_manager.zombie_group), 1)
    
    def test_wave_2_spawn(self):
        """Test spawn ondata 2"""
        wave_manager = WaveManager()
        wave_manager.current_wave = 2
        wave_manager._wave_2()
        
        # Ondata 2 dovrebbe avere 2 zombie rossi
        self.assertEqual(len(wave_manager.zombie_group), 2)
    
    def test_wave_3_spawn(self):
        """Test spawn ondata 3"""
        wave_manager = WaveManager()
        wave_manager.current_wave = 3
        wave_manager._wave_3()
        
        # Ondata 3 dovrebbe avere 2 zombie arancioni
        self.assertEqual(len(wave_manager.zombie_group), 2)
        
        # Verifica che siano arancioni
        for zombie in wave_manager.zombie_group:
            self.assertEqual(zombie.health, 2)  # Zombie arancioni hanno 2 vita
    
    def test_wave_4_spawn(self):
        """Test spawn ondata 4"""
        wave_manager = WaveManager()
        wave_manager.current_wave = 4
        wave_manager._wave_4()
        
        # Ondata 4 dovrebbe avere 3 zombie (1 arancione + 2 rossi)
        self.assertEqual(len(wave_manager.zombie_group), 3)
    
    def test_wave_5_spawn(self):
        """Test spawn ondata 5 con fasi separate"""
        wave_manager = WaveManager()
        wave_manager.current_wave = 5
        wave_manager._wave_5()
        
        # Fase 1: 3 rossi
        self.assertEqual(len(wave_manager.zombie_group), 3)
        self.assertEqual(len(wave_manager.wave_timers), 2)  # 2 timer per fasi successive
    
    def test_wave_5_phase2(self):
        """Test seconda fase ondata 5"""
        wave_manager = WaveManager()
        wave_manager._wave_5_phase2()
        
        # Fase 2: 2 rossi zigzag
        self.assertEqual(len(wave_manager.zombie_group), 2)
    
    def test_wave_5_phase3(self):
        """Test terza fase ondata 5"""
        wave_manager = WaveManager()
        wave_manager._wave_5_phase3()
        
        # Fase 3: 2 arancioni
        self.assertEqual(len(wave_manager.zombie_group), 2)
        
        # Verifica che siano arancioni
        for zombie in wave_manager.zombie_group:
            self.assertEqual(zombie.health, 2)
    
    def test_wave_completion_detection(self):
        """Test rilevamento completamento ondata"""
        wave_manager = WaveManager()
        wave_manager.current_wave = 1
        wave_manager.wave_complete = False
        wave_manager.waiting_for_next_wave = False
        
        # Aggiungi uno zombie
        wave_manager._spawn_red('A', 'straight')
        self.assertEqual(len(wave_manager.zombie_group), 1)
        
        # Simula che lo zombie muoia
        for zombie in wave_manager.zombie_group:
            zombie.kill()
        
        # Aggiorna e verifica che rilevi il completamento
        wave_manager.update()
        self.assertTrue(wave_manager.wave_complete)
    
    def test_all_waves_completed(self):
        """Test rilevamento vittoria"""
        wave_manager = WaveManager()
        
        # Simula che tutte le ondate siano completate
        wave_manager.current_wave = 5
        wave_manager.wave_complete = True
        
        self.assertTrue(wave_manager.all_waves_completed())
        
        # Test caso non completato
        wave_manager.current_wave = 3
        self.assertFalse(wave_manager.all_waves_completed())
    
    def test_wave_delay_spawn(self):
        """Test spawn con delay"""
        wave_manager = WaveManager()
        
        # Spawn con delay
        wave_manager._spawn_red('A', 'straight', wave_delay=1000)
        wave_manager._spawn_orange('B', wave_delay=500)
        
        # Dovrebbero essere presenti ma non attivi inizialmente
        self.assertEqual(len(wave_manager.zombie_group), 2)

class TestWaveIntegration(unittest.TestCase):
    """Test di integrazione per il sistema di ondate"""
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()
    
    def test_multiple_waves_sequence(self):
        """Test sequenza di multiple ondate"""
        wave_manager = WaveManager()
        
        # Simula il passare del tempo per testare le ondate
        wave_manager.start_first_wave()
        
        # Simula che il timer scada
        wave_manager.next_wave_timer = pygame.time.get_ticks() - 1000
        wave_manager.update()
        
        # Dovrebbe aver avviato ondata 1
        self.assertEqual(wave_manager.current_wave, 1)
        self.assertFalse(wave_manager.wave_complete)
    
    def test_zombie_movement_in_wave(self):
        """Test che gli zombie nelle ondate si muovano correttamente"""
        wave_manager = WaveManager()
        wave_manager.current_wave = 2  # Ondata con zigzag
        wave_manager._wave_2()
        
        initial_positions = []
        for zombie in wave_manager.zombie_group:
            initial_positions.append((zombie.rect.x, zombie.rect.y))
        
        # Simula update
        wave_manager.update()
        
        # Verifica che gli zombie si siano mossi
        for i, zombie in enumerate(wave_manager.zombie_group):
            self.assertGreater(zombie.rect.y, initial_positions[i][1])  # Si muovono verso il basso
            self.assertNotEqual(zombie.rect.x, initial_positions[i][0])  # Si muovono orizzontalmente (zigzag)

if __name__ == '__main__':
    unittest.main(verbosity=2)