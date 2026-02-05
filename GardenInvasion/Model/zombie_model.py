import pygame
from pathlib import Path
from GardenInvasion.Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, color, health, speed_y, movement_pattern, spawn_point, wave_delay=0):
        super().__init__()
        
        self.color = color
        self._load_sprite()
        
        self.rect = self.image.get_rect(midtop=pos)
        self.health = health
        self.max_health = health
        self.speed_y = speed_y
        self.movement_pattern = movement_pattern
        self.spawn_point = spawn_point
        self.wave_delay = wave_delay
        self.active = wave_delay == 0
        
        # Variabili per movimento - velocità di base 2.5
        self.horizontal_speed = 2.5  # Velocità base per tutti i zombie
        self.movement_counter = 0
        self.x_accumulator = self.rect.x
        
        # Per movimento simmetrico
        if movement_pattern == 'roam_left':
            self.horizontal_direction = 1
        elif movement_pattern == 'roam_right':
            self.horizontal_direction = -1
        else:
            self.horizontal_direction = 1
            
        # Sistema di sparo
        self.can_shoot = False
        self.shoot_cooldown = 1000  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.spawn_time = pygame.time.get_ticks()

    def _load_sprite(self):
        # Load zombie sprite based on color type
        pkg_root = Path(__file__).resolve().parent.parent
        sprites_path = pkg_root / "Assets" / "images"
        
        # Determine which sprite to load based on color
        if self.color == (255, 0, 0):  # Red zombie
            sprite_file = sprites_path / "BaseZombie01.png"
        elif self.color == (255, 165, 0):  # Orange zombie
            sprite_file = sprites_path / "BaseZombie02.png"
        else:  # Default fallback
            sprite_file = sprites_path / "BaseZombie01.png"
        
        try:
            # Load and scale sprite
            self.image = pygame.image.load(str(sprite_file)).convert_alpha()
             # Load the original image
            original_image = pygame.image.load(str(sprite_file)).convert_alpha()
            # Get original dimensions to preserve aspect ratio
            original_width, original_height = original_image.get_size()
            # Calculate target size maintaining aspect ratio
            target_height = 70  # Your desired height
            aspect_ratio = original_width / original_height
            target_width = int(target_height * aspect_ratio)
            
            # Use smoothscale with larger intermediate size for better quality
            intermediate_size = (target_width * 2, target_height * 2) # Scale up first
            temp_image = pygame.transform.smoothscale(original_image, intermediate_size) # Scale up
            
            # Then scale down to final size (produces smoother result)
            self.image = pygame.transform.smoothscale(temp_image, (target_width, target_height))
            print(f"Loaded sprite: {sprite_file.name}")

        except (pygame.error, FileNotFoundError):
            # Fallback to colored surface
            print(f"Warning: Could not load sprite {sprite_file}, using colored surface")
            self.image = pygame.Surface((40,70))
            self.image.fill(self.color)

    def update(self):
        # Gestione delay
        current_time = pygame.time.get_ticks()
        if not self.active and current_time - self.spawn_time >= self.wave_delay:
            self.active = True
        
        if not self.active:
            return
            
        self.rect.y += self.speed_y
        
        # Gestione diversi pattern di movimento
        if self.movement_pattern == 'zigzag':
            self._move_zigzag()
        elif self.movement_pattern == 'straight':
            pass
        elif self.movement_pattern == 'roam_left':
            self._move_roam_half_screen('left')
        elif self.movement_pattern == 'roam_right':
            self._move_roam_half_screen('right')
        elif self.movement_pattern == 'roam_full':
            self._move_roam_full_screen()
        
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
    
    def _move_zigzag(self):
        # existing zigzag movement with improved fluidity and better boundary handling
        self.movement_counter += 1
        
        if self.movement_counter >= 32:
            self.horizontal_direction *= -1
            self.movement_counter = 0
            
        if self.color == (255, 165, 0):
            zigzag_amplitude = 5
        else:
            zigzag_amplitude = 2.5
        
        # Usa accumulatore per movimento fluido
        self.x_accumulator += self.horizontal_direction * zigzag_amplitude
        
        if self.color == (255, 165, 0):
            min_x = 15
            max_x = SCREEN_WIDTH - 45
        else:
            if self.spawn_point in ['B', 'D']:
                min_x = 15
                max_x = SCREEN_WIDTH // 2 - 15
            else:
                min_x = SCREEN_WIDTH // 2 + 15
                max_x = SCREEN_WIDTH - 45
        
        if self.x_accumulator < min_x:
            self.x_accumulator = min_x
            self.horizontal_direction = 1
        elif self.x_accumulator > max_x:
            self.x_accumulator = max_x
            self.horizontal_direction = -1
            
        self.rect.x = int(self.x_accumulator)
    
    def _move_roam_half_screen(self, side):
        # movement pattern that roams across half the screen with smooth bouncing at edges, meeting at center without overlap
        effective_speed = self.horizontal_speed
        if (self.color == (255, 165, 0) and 
            self.movement_pattern == 'roam_full' and 
            self.spawn_point == 'A'):
            effective_speed = 3.0  # 1.5x speed per orange zombie in wave 4
        
        # Aggiorna accumulatore
        self.x_accumulator += self.horizontal_direction * effective_speed
        
        # Calcola i limiti esatti per meeting al centro senza overlap
        center_x = SCREEN_WIDTH // 2
        zombie_width = 30
        
        if side == 'left':
            min_x = 15
            max_x = center_x - zombie_width
        else:  # right
            min_x = center_x
            max_x = SCREEN_WIDTH - 45
        
        # Controlla bordi e cambia direzione
        if self.x_accumulator <= min_x:
            self.x_accumulator = min_x
            self.horizontal_direction = 1
        elif self.x_accumulator >= max_x:
            self.x_accumulator = max_x
            self.horizontal_direction = -1
            
        # Aggiorna posizione reale
        self.rect.x = int(self.x_accumulator)
    
    def _move_roam_full_screen(self):
        # movement pattern that roams across the entire screen with smooth bouncing at edges
        effective_speed = self.horizontal_speed
        if (self.color == (255, 165, 0) and 
            self.movement_pattern == 'roam_full' and 
            self.spawn_point == 'A'):
            effective_speed = 3.0  # 1.5x speed per orange zombie in wave 4
        
        self.x_accumulator += self.horizontal_direction * effective_speed
        
        min_x = 15
        max_x = SCREEN_WIDTH - 45
        
        if self.x_accumulator <= min_x:
            self.x_accumulator = min_x
            self.horizontal_direction = 1
        elif self.x_accumulator >= max_x:
            self.x_accumulator = max_x
            self.horizontal_direction = -1
            
        self.rect.x = int(self.x_accumulator)
            
    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False
            
    def can_shoot_now(self):
        if not self.can_shoot or not self.active:
            return False
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown:
            self.last_shot = current_time
            return True
        return False

class RedZombie(Zombie): # base zombie class 1
    def __init__(self, pos, movement_pattern='straight', spawn_point='A', wave_delay=0):
        super().__init__(
            pos=pos,
            color=(255, 0, 0),
            health=1,
            speed_y=2,
            movement_pattern=movement_pattern,
            spawn_point=spawn_point,
            wave_delay=wave_delay
        )
        self.can_shoot = False

class OrangeZombie(Zombie): # base zombie class 2, can shoot and has zigzag movement by default
    def __init__(self, pos, spawn_point='A', wave_delay=0, movement_pattern='zigzag'):
        super().__init__(
            pos=pos,
            color=(255, 165, 0),
            health=2,
            speed_y=1.5,
            movement_pattern=movement_pattern,
            spawn_point=spawn_point,
            wave_delay=wave_delay
        )
        self.can_shoot = True
