import pygame1, sys, time
from settings import *
from sprites import BG,Ground,Plane, Obstacles


class Game:
    def __init__(self):   # set up starting values (like position, score, health

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock() #creates a clock object

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        #scale factor
        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT/bg_height

        #sprite setup
        BG(self.all_sprites,self.scale_factor)    #like an obj creation
        Ground([self.all_sprites,self.collision_sprites],self.scale_factor)
        self.plane = Plane(self.all_sprites,self.scale_factor/1.6)

        #timer
        self.obstacle_timer= pygame.USEREVENT +1  #own custom event/want to do something automatically
        pygame.time.set_timer(self.obstacle_timer ,1000)

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites,False, pygame.sprite.collide_mask) \
        or self.plane.rect.top <=0:
            pygame.quit()
            sys.exit()


    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.plane.jump()
                if event.type == self.obstacle_timer:
                    Obstacles([self.all_sprites,self.collision_sprites], self.scale_factor*0.87)  #can be adjusted by *1.2 or more in scale



            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt) #calls each sprite's update() method
            self.all_sprites.draw(self.display_surface)
            self.collisions()
            pygame.display.update()
            self.clock.tick(FRAME_RATE)

if __name__ == '__main__':
    game = Game()
    game.run()