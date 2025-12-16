import pygame
from Utilities.constants import SCREEN_HEIGHT

class ZombieProjectile(pygame.sprite.Sprite):
    """Proiettile sparato dagli zombie arancioni"""
    
    def __init__(self, pos):
        super().__init__()
        
        # Creazione proiettile (rettangolo giallo)
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(midbottom=pos)
        
        self.speed = 5
        
    def update(self):
        """Aggiorna posizione del proiettile"""
        self.rect.y += self.speed
        
        # Rimuovi se esce dallo schermo in basso
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            