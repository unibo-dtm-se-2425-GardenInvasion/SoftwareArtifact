import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__() # call the parent class constructor
        self.image = pygame.image.load(r'GardenInvasion/Assets/images/Projectile.png').convert_alpha()
        # load the projectile image with transparency
        self.rect = self.image.get_rect(midbottom=pos) # set the position of the projectile
        self.speed = -10 # the speed at which the projectile moves upwards, if positive if moves backwards

    def update(self): # update the position of the projectile
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill() # remove the projectile if it goes off-screen
