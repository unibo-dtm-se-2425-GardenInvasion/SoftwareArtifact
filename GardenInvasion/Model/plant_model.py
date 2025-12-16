import pygame
from ..Utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite): # sprite is used to represent game objects in the class
    def __init__(self, pos, scale_factor=0.15):
        super().__init__() # super() calls the constructor of the parent class (pygame.sprite.Sprite)
        original_image = pygame.image.load(r"GardenInvasion/Assets/images/BasePlant01.png").convert_alpha() # load image with transparency
        original_size = original_image.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self.image = pygame.transform.smoothscale(original_image, new_size)
        self.rect = self.image.get_rect(midbottom=pos)
        # get original image of the plant and change its size keeping the aspect ratio
        self.speed = 5 # movement speed

        self.shoot_SecondTime = 500  # 0.5 seconds
        self.last_shot = pygame.time.get_ticks()# track time of last shot

    def move_left(self): # move left
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0 # prevent moving out of screen on the left side

    def move_right(self): # move right
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH # prevent moving out of screen on the right side

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_SecondTime:
            self.last_shot = current_time
            return True
        return False