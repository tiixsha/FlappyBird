import pygame, sys, time
from settings import *
from sprites import BG


class Game:
    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock() #creates a clock object

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        #scale factor
        bg_height = pygame.image.load('../FlappyBird/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT/bg_height

        #sprite setup
        BG(self.all_sprites,self.scale_factor)

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

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
            self.clock.tick(FRAME_RATE)

if __name__ == '__main__':
    game = Game()
    game.run()