# Standard Library Imports


# Third-Party Imports
import pygame

# Local Imports
from settings import *


class TitleScreen:

    def __init__(self, game):
        self.game = game

        self.primary_font = pygame.font.Font(PRIMARY_FONT, 80)
        self.secondary_font = pygame.font.Font(SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.primary_font.render(CAPTION, True, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.bottom = SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.secondary_font.render("Press 'SPACE' to start.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.top = SCREEN_HEIGHT // 2 + 8
        surface.blit(text, rect)


class GameOverScreen:

    def __init__(self, game):
        self.game = game

        self.primary_font = pygame.font.Font(PRIMARY_FONT, 80)
        self.secondary_font = pygame.font.Font(SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.primary_font.render("Game over", True, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.bottom = SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.secondary_font.render("Press 'r' to play again.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.top = SCREEN_HEIGHT // 2 + 8
        surface.blit(text, rect)
