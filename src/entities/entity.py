# Standard Library Imports
import math
import random

# Third-Party Imports
import pygame

# Local Imports
import settings


# Base Entity class
class Entity(pygame.sprite.Sprite):

    def __init__(self, game, image, location):
        super().__init__()

        self.game = game
        self.original_image = image
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.location = pygame.Vector2(location)
        self.original_location = self.location.copy()
        self.rect.center = self.location
        self.angle = 0
        self.previous_angle = self.angle

    def rotate_to(self, angle):
        if angle != self.previous_angle:
            alpha = self.image.get_alpha()
            self.image = pygame.transform.rotate(self.original_image, angle - settings.ROTATION_OFFSET)
            self.rect = self.image.get_rect(center=self.location)
            self.mask = pygame.mask.from_surface(self.image)
            self.image.set_alpha(alpha)

    def rotate_amount(self, angle):
        self.angle = (self.angle + angle) % 360
        self.rotate_to(self.angle)

    def move(self):
        self.location += self.velocity
        self.rect.center = self.location

    def move_to(self, location):
        self.location.update(location)
        self.rect.center = self.location
        
    def update(self, *args, **kwargs):
        pass


# Base Item class
class Item(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

        speed = random.randrange(settings.ITEM_MIN_SPEED, settings.ITEM_MAX_SPEED)
        self.distance_to_travel = random.randrange(settings.MIN_ITEM_DISTANCE, settings.MAX_ITEM_DISTANCE)
        angle = random.randrange(0, 360)
        radians = math.radians(angle)
        self.velocity = pygame.Vector2(math.cos(radians), -1 * math.sin(radians)) * speed

    def apply(self, ship):
        raise NotImplementedError
        
    def update(self, *args, **kwargs):
        self.move()

        distance_traveled_squared = self.location.distance_squared_to(self.original_location)

        if distance_traveled_squared > self.distance_to_travel ** 2:
            self.kill()
