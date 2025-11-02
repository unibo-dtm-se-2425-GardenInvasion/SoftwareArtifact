import pygame
from .zombie_model import RedZombie, OrangeZombie
from Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class WaveManager:
    """Gestisce le ondate di zombie con timer di 3 secondi tra le ondate"""
    
    def __init__(self):
        self.current_wave = 0
        self.total_waves = 5
        self.wave_complete = True
        self.zombie_group = pygame.sprite.Group()
        self.zombie_projectile_group = pygame.sprite.Group()
        self.wave_timers = []
        
        # Timer per prossima ondata (3 secondi)
        self.next_wave_timer = 0
        self.waiting_for_next_wave = False
        
        # Punti di spawn (sopra lo schermo)
        self.spawn_points = {
            'A': (SCREEN_WIDTH // 2, -50),
            'B': (SCREEN_WIDTH // 3, -50),
            'C': (SCREEN_WIDTH * 2 // 3, -50),
            'D': (SCREEN_WIDTH // 4, -50),
            'E': (SCREEN_WIDTH * 3 // 4, -50)
        }
        
    def start_first_wave(self):
        """Avvia la prima ondata dopo 3 secondi"""
        self.current_wave = 0
        self.wave_complete = True
        self.waiting_for_next_wave = True
        self.next_wave_timer = pygame.time.get_ticks() + 3000  # 3 secondi
        print("🕒 Prima ondata tra 3 secondi...")
        
    def update(self):
        """Aggiorna lo stato delle ondate e timer"""
        current_time = pygame.time.get_ticks()
        
        # Controlla se è tempo di avviare una nuova ondata
        if self.waiting_for_next_wave and current_time >= self.next_wave_timer:
            self._execute_wave_start()
            
        # Aggiorna zombie e proiettili
        self.zombie_group.update()
        self.zombie_projectile_group.update()
        self._handle_zombie_shooting()
        
        # Aggiorna timer interni delle ondate
        current_timers = self.wave_timers.copy()  # Copia per evitare modifiche durante l'iterazione
        for timer in current_timers:
            if current_time >= timer['time']:
                timer['action']()
                if timer in self.wave_timers:  # Controlla se ancora nella lista
                    self.wave_timers.remove(timer)
        
        # DEBUG: Mostra stato corrente (ogni 2 secondi)
        if current_time % 2000 < 16:  # Ogni 2 secondi circa
            print(f"DEBUG: Wave {self.current_wave}, Complete: {self.wave_complete}, Waiting: {self.waiting_for_next_wave}, Zombies: {len(self.zombie_group)}, Timers: {len(self.wave_timers)}")
        
        # Controlla se ondata corrente è completata
        if (not self.wave_complete and 
            not self.waiting_for_next_wave and 
            len(self.zombie_group) == 0 and 
            len(self.wave_timers) == 0):
            
            self.wave_complete = True
            print(f"✅ Ondata {self.current_wave} completata!")
            
            # Prepara automaticamente la prossima ondata
            if self.current_wave < self.total_waves:
                self._prepare_next_wave()
            else:
                print("🎉 TUTTE LE ONDATE COMPLETATE! VITTORIA!")
                
    def _prepare_next_wave(self):
        """Prepara la prossima ondata da avviare dopo 3 secondi"""
        self.waiting_for_next_wave = True
        self.next_wave_timer = pygame.time.get_ticks() + 3000  # 3 secondi
        print(f"🕒 Ondata {self.current_wave + 1} tra 3 secondi...")
            
    def _execute_wave_start(self):
        """Esegue l'effettivo avvio dell'ondata"""
        self.waiting_for_next_wave = False
        self.current_wave += 1
        self.wave_complete = False
        self.wave_timers = []
        
        print(f"🧟 ONDATA {self.current_wave} INIZIATA!")
        
        # Esegue l'ondata corrispondente
        if self.current_wave == 1:
            self._wave_1()
        elif self.current_wave == 2:
            self._wave_2()
        elif self.current_wave == 3:
            self._wave_3()
        elif self.current_wave == 4:
            self._wave_4()
        elif self.current_wave == 5:
            self._wave_5()
            
    def _handle_zombie_shooting(self):
        """Gestisce lo sparo degli zombie arancioni"""
        for zombie in self.zombie_group:
            if hasattr(zombie, 'can_shoot_now') and zombie.can_shoot_now():
                self._spawn_zombie_projectile(zombie.rect.midbottom)
                
    def _spawn_zombie_projectile(self, pos):
        """Crea un nuovo proiettile zombie"""
        from .zombie_projectile_model import ZombieProjectile
        projectile = ZombieProjectile(pos)
        self.zombie_projectile_group.add(projectile)
        
    def _spawn_red(self, spawn_point, movement_pattern, wave_delay=0):
        """Spawna zombie rosso"""
        if spawn_point in self.spawn_points:
            zombie = RedZombie(self.spawn_points[spawn_point], movement_pattern, spawn_point, wave_delay)
            self.zombie_group.add(zombie)
            delay_msg = f" (delay: {wave_delay}ms)" if wave_delay > 0 else ""
            print(f"  🟥 Zombie rosso spawnato in {spawn_point} ({movement_pattern}){delay_msg}")
        
    def _spawn_orange(self, spawn_point, movement_pattern='straight', wave_delay=0):
        """Spawna zombie arancione"""
        if spawn_point in self.spawn_points:
            zombie = OrangeZombie(self.spawn_points[spawn_point], spawn_point, wave_delay, movement_pattern)
            self.zombie_group.add(zombie)
            delay_msg = f" (delay: {wave_delay}ms)" if wave_delay > 0 else ""
            print(f"  🟧 Zombie arancione spawnato in {spawn_point} ({movement_pattern}){delay_msg}")
    
    # --- DEFINIZIONE ONDATE ---
    def _wave_1(self):
        """Ondata 1: 1 zombie rosso in linea retta"""
        self._spawn_red('A', 'straight')
        
    def _wave_2(self):
        """Ondata 2: 2 zombie rossi con movimento simmetrico opposto"""
        self._spawn_red('B', 'roam_left')   # Si muove da sinistra verso destra (metà sinistra)
        self._spawn_red('C', 'roam_right')  # Si muove da destra verso sinistra (metà destra)
        
    def _wave_3(self):
        """Ondata 3: 2 zombie arancioni con movimento simmetrico opposto"""
        self._spawn_orange('B', 'roam_left')   # Si muove da sinistra verso destra (metà sinistra)
        self._spawn_orange('C', 'roam_right')  # Si muove da destra verso sinistra (metà destra)
        
    def _wave_4(self):
        """Ondata 4: 2 rossi simmetrici + 1 arancione full screen con delay"""
        # Due rossi con movimento simmetrico opposto
        self._spawn_red('B', 'roam_left')
        self._spawn_red('C', 'roam_right')
        
        # Arancione con delay di 0.4 secondi che si muove su tutto lo schermo
        self._spawn_orange('A', 'roam_full', 1000)
        
    def _wave_5(self):
        """Ondata 5: Sequenza ordinata con spawn separati e intervalli dimezzati"""
        print("  🌊 Ondata 5 - Fase 1: 3 Rossi")
        # Fase 1 - 3 rossi insieme
        self._spawn_red('D', 'straight')
        self._spawn_red('A', 'straight')
        self._spawn_red('E', 'straight')
    
        # Fase 2 - Dopo 1 secondo (dimezzato): 2 rossi con comportamento come wave 2
        self.wave_timers.append({
            'time': pygame.time.get_ticks() + 1000,  # 1 secondo (dimezzato da 2)
            'action': self._wave_5_phase2
        })
    
        # Fase 3 - Dopo 2 secondi (dimezzato): 2 arancioni simmetrici
        self.wave_timers.append({
            'time': pygame.time.get_ticks() + 2000,  # 2 secondi (dimezzato da 4)
            'action': self._wave_5_phase3
        })

    def _wave_5_phase2(self):
        """Seconda fase ondata 5: 2 rossi con comportamento come wave 2"""
        print("  🌊 Ondata 5 - Fase 2: 2 Rossi Simmetrici")
        self._spawn_red('B', 'roam_left')   # Stesso comportamento di wave 2
        self._spawn_red('C', 'roam_right')  # Stesso comportamento di wave 2
    
    def _wave_5_phase3(self):
        """Terza fase ondata 5: 2 arancioni simmetrici"""
        print("  🌊 Ondata 5 - Fase 3: 2 Arancioni Simmetrici")
        # Arancioni con movimento speculare perfetto
        self._spawn_orange('B', 'roam_left')   # Si muove da sinistra verso destra
        self._spawn_orange('C', 'roam_right')  # Si muove da destra verso sinistra
        
    def all_waves_completed(self):
        """Controlla se tutte le ondate sono state completate"""
        return self.current_wave >= self.total_waves and self.wave_complete
    
    def get_wave_info(self):
        """Restituisce informazioni sull'ondata corrente"""
        if self.waiting_for_next_wave:
            time_left = max(0, (self.next_wave_timer - pygame.time.get_ticks()) // 1000)
            return f"Ondata {self.current_wave + 1} tra {time_left}s"
        elif self.wave_complete and self.current_wave >= self.total_waves:
            return "VITTORIA!"
        elif self.wave_complete:
            return f"Ondata {self.current_wave} completata"
        else:
            return f"Ondata {self.current_wave} - Zombie: {len(self.zombie_group)}"