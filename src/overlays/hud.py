# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
from settings import *


class HUD:

    def __init__(self, game):
        self.game = game

        self.primary_font = pygame.font.Font(PRIMARY_FONT, 80)
        self.secondary_font = pygame.font.Font(SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.secondary_font.render(f"Shield: {self.game.ship.shield}", True, WHITE)
        rect = text.get_rect()
        rect.bottomleft = 32, SCREEN_HEIGHT - 32
        surface.blit(text, rect)


class Minimap:
    
    def __init__(self, game):
        self.game = game
        
    def update(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, [16, 16, 128, 128], 2)

        for player in self.game.players:
            minimap_x = (player.location.x / self.game.world_width) * 128 + 16
            minimap_y = (player.location.y / self.game.world_height) * 128 + 16
            pygame.draw.rect(surface, RED, [minimap_x - 2, minimap_y - 2, 4, 4])
