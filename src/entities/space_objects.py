# Standard Library Imports
import math
import random

# Third-Party Imports
import pygame

# Local imports
import settings
from .entity import Entity
from .items import ShieldBoost, DoubleShot


class Asteroid(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

        speed = random.randrange(settings.ASTEROID_MIN_SPEED, settings.ASTEROID_MAX_SPEED)
        angle = random.randrange(0, 360)
        radians = math.radians(angle)

        self.velocity = pygame.Vector2(math.cos(radians), -1 * math.sin(radians)) * speed
        self.rotational_speed = random.randrange(settings.ASTEROID_MIN_ROTATION_SPEED, settings.ASTEROID_MAX_ROTATION_SPEED)
        self.rotational_speed *= random.choice([-1, 1])

    def check_lasers(self):
        hits = pygame.sprite.spritecollide(self, self.game.lasers, True, pygame.sprite.collide_mask)

        if hits:
            self.kill()  # later, they should break up

    def check_world_edges(self):
        if self.location.x < 0:
            self.location.x = self.game.world_width
        elif self.location.x > self.game.world_width:
            self.location.x = 0

        if self.location.y < 0:
            self.location.y = self.game.world_height
        elif self.location.y > self.game.world_height:
            self.location.y = 0

    def update(self, *args, **kwargs):
        self.move()
        self.angle += self.rotational_speed
        self.rotate_to(self.angle)
        self.check_lasers()
        self.check_world_edges()


class BlackHole(Entity):

    def __init__(self, game, image, location, destination):
        super().__init__(game, image, location)    

        self.rotational_speed = random.randrange(settings.BLACKHOLE_MIN_ROTATION_SPEED, settings.BLACKHOLE_MAX_ROTATION_SPEED)
        self.rotational_speed *= random.choice([-1, 1])
        self.destination = destination

    def apply(self, ship):
        if ship.escape_time == 0:
            ship.controls_disabled = True
            ship.velocity.update(0, 0)

        if ship.controls_disabled:
            ship.location.move_towards_ip(self.location, 1)
            ship.rotate_amount(self.rotational_speed)
            ship.image.set_alpha(ship.image.get_alpha() * settings.BLACKHOLE_FADE_RATE)
        
        if ship.location.distance_squared_to(self.location) < 1 and ship.image.get_alpha() < settings.BLACKHOLE_CAPTURE_THRESHOLD:
            ship.move_to(self.destination)
            ship.escape_time = settings.ESCAPE_TIME
            ship.controls_disabled = False
            ship.image.set_alpha(255)

    def update(self, *args, **kwargs):
        self.angle += self.rotational_speed
        self.rotate_to(self.angle)


class Pulsar(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

        self.rotational_speed = settings.PULSAR_ROTATION_SPEED

    def spawn_item(self):
        r = random.randrange(0, settings.FPS)

        if r < settings.ITEMS_PER_SECOND:
            powerup_type = random.choice([ShieldBoost, DoubleShot])
            item = powerup_type(self.game, self.game.powerup_img, self.location)
            self.game.items.add(item)

    def apply(self, ship):
        if ship.escape_time == 0:
            ship.controls_enabled = False
            ship.escape_time = settings.ESCAPE_TIME
            ship.velocity = (self.location - ship.location).normalize().rotate(90) * settings.PULSAR_FLING_SPEED
            ship.rotational_speed = self.rotational_speed

    def update(self):
        self.rotate_amount(self.rotational_speed)
        self.spawn_item()


class Starfield:

    def __init__(self, game, num_stars):
        self.game = game

        self.star_locs = [] 
        for _ in range(num_stars):
            x = random.randrange(0, self.game.world_width)
            y = random.randrange(0, self.game.world_width)
            self.star_locs.append([x, y])

    def draw(self, surface, offset_x, offset_y):
        for loc in self.star_locs:
            x = loc[0] - offset_x
            y = loc[1] - offset_y
            r = random.randint(0, 25) # Magic number alert!
            color = settings.WHITE if r == 0 else settings.LIGHT_GRAY
            pygame.draw.circle(surface, color, [x, y], 3)        