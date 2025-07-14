import pygame
from settings import*
from random import choice, randint


class BG(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):   #define a function or a method
        super().__init__(groups) #calls parent init, Adds this BG sprite to the group self.all_sprites
        bg_image =  pygame.image.load('./graphics/environment/background.png').convert()
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
        ground_surf = pygame.image.load('./graphics/environment/ground.png').convert_alpha()
        full_height = ground_surf.get_height() * scale_factor
        full_width = ground_surf.get_width() * scale_factor

        full_sized_image = pygame.transform.scale(ground_surf, (full_width, full_height))

        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))

        #position
        self.rect = self.image.get_rect(bottomleft =(0,WINDOW_HEIGHT) )
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #mask
        self.mask= pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= 360*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Bird(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)

        #image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #rect
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH/20,WINDOW_HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.gravity = 975
        self.direction = 0

    def import_frames(self,scale_factor):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(f'./graphics/bird/bird{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor*1.8)
            self.frames.append(scaled_surface)

    def apply_gravity(self,dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = -400

    def animate(self,dt):
        self.frame_index += 10*dt #to control speed of animation 10 frames per sec
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image,-self.direction*0.06,1) #adds rotate fn to the animation
        self.image = rotated_plane
        # mask
        self.mask = pygame.mask.from_surface(self.image)
    def update(self,dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor, orientation, x_pos, y_pos, is_scorer=False):  # Add is_scorer
        super().__init__(groups)
        self.is_scorer = is_scorer  # Marks if this is a scoring trigger

        if not self.is_scorer:  # Normal pipe logic
            surf = pygame.image.load('./graphics/obstacles/1.png').convert_alpha()
            self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor*1.2)

            if orientation == 'down':
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect = self.image.get_rect(midtop=(x_pos, y_pos))
            else:
                self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))

            self.mask = pygame.mask.from_surface(self.image)
        else:  # Invisible scoring trigger
            self.image = pygame.Surface((10, 1), pygame.SRCALPHA)  # Tiny invisible surface
            self.rect = self.image.get_rect(center=(x_pos, y_pos))

        self.pos = pygame.math.Vector2(self.rect.topleft)

    def spawn_pipe_pair(groups, scale_factor):
        gap_height = 100
        x_pos = WINDOW_WIDTH + randint(40, 100)
        y_pos_bottom = WINDOW_HEIGHT+randint(20,110)

        # Bottom pipe
        Obstacles(groups, scale_factor, 'up', x_pos, y_pos_bottom)

        # Top pipe
        y_pos_top = y_pos_bottom - WINDOW_HEIGHT- gap_height
        Obstacles(groups, scale_factor, 'down', x_pos, y_pos_top)
        # Invisible scoring trigger (placed between pipes)
        Obstacles(groups, scale_factor, None, x_pos + 50, (y_pos_bottom + y_pos_top) // 2, is_scorer=True)

    def update(self,dt):
        self.pos.x-= 500*dt
        self.rect.x= round(self.pos.x)
        if self.rect.right <=-50:
            self.kill()
