import pygame
from settings import*

class BG(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups) #calls parent init
        bg_image =  pygame.image.load('../FlappyBird/environment/background.png').convert()

        full_height = bg_image.get_height() * scale_factor
        full_width =  bg_image.get_width() * scale_factor

        full_sized_image= pygame.transform.scale(bg_image,(full_width,full_height))

        self.image = pygame.Surface((full_width*2,full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image,(full_width,0))
        self.rect = self.image.get_rect(topleft = (0,0))
        #rect required for pygame's rendering and collision system
        self.pos = pygame.math.Vector2(self.rect.topleft)
        #creates a 2d vector that stores the sprite's position
        # vector2 allows floating point precision unlike rect which uses integers

    def update(self,dt):
        self.pos.x -= 300*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)

        #image
        ground_surf = pygame.image.load('../FlappyBird/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size())* scale_factor)

        #position
        self.rect = self.image.get_rect(bottomleft =(0,WINDOW_HEIGHT) )
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self,dt):
        self.pos.x -= 360*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
