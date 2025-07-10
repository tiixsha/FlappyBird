import pygame
from settings import *


class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0

        # Load high score
        try:
            with open("data.txt") as data:
                self.high_score = int(data.read())
        except (FileNotFoundError, ValueError):
            self.high_score = 0
            with open("data.txt", mode="w") as data:
                data.write("0")

        # Font setup
        self.font = pygame.font.Font('./graphics/font/BD_Cartoon_Shout.ttf', 30)

        # Create sprite image and rect
        self.image = pygame.Surface((300, 50), pygame.SRCALPHA)  # Transparent surface
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, 50))

        # Score text surface
        self.score_text = None
        self.update_scoreboard()

    def update_scoreboard(self):
        """Update the score display"""
        self.score_text = self.font.render(str(self.score), True, 'black')
        # Center the text on our surface
        self.image.fill((0, 0, 0, 0))  # Clear with transparent
        text_rect = self.score_text.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        self.image.blit(self.score_text, text_rect)

    def reset(self):
        """Reset the current score and update high score if needed"""
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", mode="w") as data:
                data.write(f"{self.high_score}")
        self.score = 0
        self.update_scoreboard()

    def increase_score(self):
        """Increment the score and update the display"""
        self.score += 1
        self.update_scoreboard()

    def update(self, dt=None):
        """Sprite update method (required but not needed for scoreboard)"""
        pass