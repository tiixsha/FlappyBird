import pygame, sys, time
from settings import *
from sprites import BG,Ground,Bird, Obstacles

class Game:
    def __init__(self):   # set up starting values (like position, score, health

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock() # creates a clock object
        self.font = pygame.font.SysFont(None, 30)  # Added for score display
        self.gameover_bg = pygame.image.load("graphics/environment/gameover_bg.png").convert_alpha()
        self.game_over_bg = pygame.transform.scale(self.gameover_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # game state
        self.game_active = True  # Added to track game over
        self.score = 0  # Added to track score

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        #scale factor
        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT/bg_height

        #sprite setup
        BG(self.all_sprites,self.scale_factor)    #like an obj creation
        Ground([self.all_sprites,self.collision_sprites],self.scale_factor)
        self.plane = Bird(self.all_sprites,self.scale_factor/1.6)


        #timer
        self.obstacle_timer= pygame.USEREVENT +1  # own custom event/want to do something automatically
        pygame.time.set_timer(self.obstacle_timer ,900)



    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites,False, pygame.sprite.collide_mask) \
        or self.plane.rect.top <=0:
            self.game_active = False

    def check_score(self):
        for obstacle in self.collision_sprites:
            if getattr(obstacle, 'is_scorer', False) and obstacle.rect.right < self.plane.rect.left:
                self.score += 1
                obstacle.kill()  # Remove to prevent duplicate scoring

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.display_surface.blit(score_surf, (20, 20))

    def display_game_over(self):
        self.display_surface.blit(self.game_over_bg, (0, 0))
        score_surf = self.font.render(f'Score: {self.score}', True, (42, 42, 42))
        self.display_surface.blit(score_surf, (WINDOW_WIDTH//2 - 45, WINDOW_HEIGHT//2 + 20))

    def reset_game(self):
        self.game_active = True
        self.score = 0
        self.all_sprites.empty()
        self.collision_sprites.empty()
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Bird(self.all_sprites, self.scale_factor / 1.6)

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
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_SPACE and self.game_active:
                        self.plane.jump()
                if event.type == self.obstacle_timer and self.game_active:
                    Obstacles.spawn_pipe_pair([self.all_sprites, self.collision_sprites], self.scale_factor * 0.87)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.game_active:
                    self.reset_game()

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt) #calls each sprite's update() method
            self.all_sprites.draw(self.display_surface)

            if self.game_active:
                self.collisions()
                self.check_score()
                self.display_score()
            else:
                self.display_game_over()

            pygame.display.update()
            self.clock.tick(FRAME_RATE)

if __name__ == '__main__':
    game = Game()
    game.run()