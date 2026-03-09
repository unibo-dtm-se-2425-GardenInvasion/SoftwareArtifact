import pygame
from .zombie_model import RedZombie, OrangeZombie
from ..Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class WaveManager:
    # wave manager with 3 second timer between waves
        
    def __init__(self):
        self.current_wave = 0
        self.total_waves = 5
        self.wave_complete = True
        self.zombie_group = pygame.sprite.Group()
        self.zombie_projectile_group = pygame.sprite.Group()
        self.wave_timers = []
        
        self.next_wave_timer = 0 # timer for next wave start
        self.waiting_for_next_wave = False
        
        # spawn points for zombies
        self.spawn_points = {
            'A': (SCREEN_WIDTH // 2, -50),
            'B': (SCREEN_WIDTH // 3, -50),
            'C': (SCREEN_WIDTH * 2 // 3, -50),
            'D': (SCREEN_WIDTH // 4, -50),
            'E': (SCREEN_WIDTH * 3 // 4, -50)
        }
        
    def start_first_wave(self):
        # start first wave with 3 second timer
        self.current_wave = 0
        self.wave_complete = True
        self.waiting_for_next_wave = True
        self.next_wave_timer = pygame.time.get_ticks() + 3000
        
    def update(self):
        # update wave manager, called every frame
        current_time = pygame.time.get_ticks()
        
        # check if we are waiting for next wave and timer has expired
        if self.waiting_for_next_wave and current_time >= self.next_wave_timer:
            self._execute_wave_start()
            
        self.zombie_group.update()
        self.zombie_projectile_group.update()
        self._handle_zombie_shooting()
        
        # update wave timers, execute actions if timer has expired
        current_timers = self.wave_timers.copy()
        for timer in current_timers:
            if current_time >= timer['time']:
                timer['action']()
                if timer in self.wave_timers:  
                    self.wave_timers.remove(timer)
            
        # check if current wave is complete (no zombies left and no pending timers)
        if (not self.wave_complete and 
            not self.waiting_for_next_wave and 
            len(self.zombie_group) == 0 and 
            len(self.wave_timers) == 0):
            
            self.wave_complete = True
            # check if we have more waves to start
            if self.current_wave < self.total_waves:
                self._prepare_next_wave()

    def _prepare_next_wave(self):
        # prepare next wave with 3 second timer
        self.waiting_for_next_wave = True
        self.next_wave_timer = pygame.time.get_ticks() + 3000
            
    def _execute_wave_start(self):
        # exectute wave start, spawn zombies based on current wave
        self.waiting_for_next_wave = False
        self.current_wave += 1
        self.wave_complete = False
        self.wave_timers = []
        
        print(f"Wave {self.current_wave} begins")
        
        # execute wave logic based on current wave number
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
        # handling zombie shooting, spawn projectiles if zombies can shoot
        for zombie in self.zombie_group:
            if hasattr(zombie, 'can_shoot_now') and zombie.can_shoot_now():
                self._spawn_zombie_projectile(zombie.rect.midbottom)
                
    def _spawn_zombie_projectile(self, pos):
        # zombie shoots a projectile, spawn it at given position
        from .zombie_projectile_model import ZombieProjectile
        projectile = ZombieProjectile(pos)
        self.zombie_projectile_group.add(projectile)
        
    def _spawn_red(self, spawn_point, movement_pattern, wave_delay=0):
        # spawna zombie base 1
        if spawn_point in self.spawn_points:
            zombie = RedZombie(self.spawn_points[spawn_point], movement_pattern, spawn_point, wave_delay)
            self.zombie_group.add(zombie)
            delay_msg = f" (delay: {wave_delay}ms)" if wave_delay > 0 else ""
            
    def _spawn_orange(self, spawn_point, movement_pattern='straight', wave_delay=0):
        # spawn zombie base 2
        if spawn_point in self.spawn_points:
            zombie = OrangeZombie(self.spawn_points[spawn_point], spawn_point, wave_delay, movement_pattern)
            self.zombie_group.add(zombie)
            delay_msg = f" (delay: {wave_delay}ms)" if wave_delay > 0 else ""
            
    # waves logic, each wave has different spawn patterns and timings
    def _wave_1(self):
        self._spawn_red('A', 'straight')
        
    def _wave_2(self):
        self._spawn_red('B', 'roam_left')   
        self._spawn_red('C', 'roam_right')  
        
    def _wave_3(self):
        self._spawn_orange('B', 'roam_left')   
        self._spawn_orange('C', 'roam_right')  
        
    def _wave_4(self):
        self._spawn_red('B', 'roam_left')
        self._spawn_red('C', 'roam_right')
        
        self._spawn_orange('A', 'roam_full', 1000)
        
    def _wave_5(self):
        print("Ondata 5 - Fase 1: 3 Rossi")
        
        # phase 1 with 3 base 1 zombies
        self._spawn_red('D', 'straight')
        self._spawn_red('A', 'straight')
        self._spawn_red('E', 'straight')
    
        self.wave_timers.append({
            'time': pygame.time.get_ticks() + 1000, 
            'action': self._wave_5_phase2
        })
    
        self.wave_timers.append({
            'time': pygame.time.get_ticks() + 2000, 
            'action': self._wave_5_phase3
        })

    def _wave_5_phase2(self):
        self._spawn_red('B', 'roam_left')   
        self._spawn_red('C', 'roam_right')  
    
    def _wave_5_phase3(self):
        # base zombie 2 with delayed spawn to create more pressure on player
        self._spawn_orange('B', 'roam_left')   
        self._spawn_orange('C', 'roam_right')  
        
    def all_waves_completed(self):
        # check if all waves are completed
        return self.current_wave >= self.total_waves and self.wave_complete
    
    def get_wave_info(self):
        # return string with current wave info for UI display
        if self.waiting_for_next_wave:
            time_left = max(0, (self.next_wave_timer - pygame.time.get_ticks()) // 1000)
            return f"Ondata {self.current_wave + 1} tra {time_left}s"
        elif self.wave_complete and self.current_wave >= self.total_waves:
            return "VITTORIA!"
        elif self.wave_complete:
            return f"Ondata {self.current_wave} completata"
        else:
            return f"Ondata {self.current_wave} - Zombie: {len(self.zombie_group)}"
    
    def is_victory(self) -> bool: # check if player won by completing all waves and defeating all zombies
        all_waves_completed = self.current_wave >= self.total_waves
        no_zombies_remaining = len(self.zombie_group) == 0
        no_pending_spawns = len(self.wave_timers) == 0
        
        return all_waves_completed and no_zombies_remaining and no_pending_spawns
