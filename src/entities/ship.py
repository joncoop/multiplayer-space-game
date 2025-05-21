# Standard-library imports
import math

# Third-Party Imports
import pygame

# Local imports
import settings
from .entity import Entity


class Ship(Entity):

    def __init__(self, game, image, location, controls):
        super().__init__(game, image, location)

        self.controls = controls
        self.angle = 90
        self.previous_angle = self.angle
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 0
        self.max_speed = settings.SHIP_MAX_SPEED
        self.escape_time = 0
        self.controls_enabled = True
        self.shield = settings.SHIP_STARTING_SHIELD
        self.doubleshot_time = 0
        self.rotational_speed = 0

    def act(self, events, keys):
        if not self.controls_enabled:
            self.slow()
            return
        
        if keys[self.controls['left']]:
            self.rotate_left()
        elif keys[self.controls['right']]:
            self.rotate_right()

        if keys[self.controls['thrust']]:
            self.thrust()
        else:
            self.slow()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls['shoot']:
                    self.shoot()
                if event.key == self.controls['respawn']:
                    self.respawn()

    def rotate_left(self):
        self.previous_angle = self.angle
        self.angle += settings.SHIP_TURN_SPEED
        self.angle %= 360
        self.rotational_speed = 0

    def rotate_right(self):
        self.previous_angle = self.angle
        self.angle -= settings.SHIP_TURN_SPEED
        self.angle %= 360
        self.rotational_speed = 0

    def thrust(self):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), -1 * math.sin(radians))
        self.velocity += direction * settings.ACCELERATION

        if self.velocity.length_squared() > self.max_speed ** 2:
            self.velocity.scale_to_length(self.max_speed) 

    def slow(self):
        self.velocity *= 1 - settings.DRAG

        if self.velocity.length_squared() < settings.MIN_VELOCITY_SQUARED:
            self.velocity.update(0, 0)

        if self.rotational_speed > 0:
            self.rotational_speed = max(self.rotational_speed - settings.ROTATIONAL_DRAG, 0)
        if self.rotational_speed < 0:
            self.rotational_speed = min(self.rotational_speed + settings.ROTATIONAL_DRAG, 0)

    def shoot(self):
        if self.doubleshot_time > 0:
            radians = math.radians(self.angle - 90)
            perpendicular_direction = pygame.Vector2(math.cos(radians), -1 * math.sin(radians))
            laser_spawn_point1 = self.location - perpendicular_direction * self.original_image.get_width() / 2
            laser_spawn_point2 = self.location + perpendicular_direction * self.original_image.get_width() / 2
            laser1 = Laser(self.game, self.game.laser_img, laser_spawn_point1, self.angle)
            laser2 = Laser(self.game, self.game.laser_img, laser_spawn_point2, self.angle)
            self.game.lasers.add(laser1, laser2)
        else:
            radians = math.radians(self.angle)
            forward_direction = pygame.Vector2(math.cos(radians), -1 * math.sin(radians))
            laser_spawn_point = self.location + forward_direction * self.original_image.get_height() / 2
            laser = Laser(self.game, self.game.laser_img, laser_spawn_point, self.angle)
            self.game.lasers.add(laser)

    def respawn(self):
        self.location = self.original_location.copy()
        self.velocity *= 0
        self.escape_time = 0
        self.controls_enabled = True

    def check_asteroids(self):
        hits = pygame.sprite.spritecollide(self, self.game.asteroids, False, pygame.sprite.collide_mask)

        if hits:
            self.respawn()  # should probably blow up and lose lives or something

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, self.game.items, True, pygame.sprite.collide_mask)

        for item in hits:
            item.apply(self)

        self.doubleshot_time = max(self.doubleshot_time - 1, 0)

    def check_boundaries(self):
        if settings.WORLD_WRAP:
            if self.location.x < 0:
                self.location.x = self.game.world_width
            elif self.location.x > self.game.world_width:
                self.location.x = 0

            if self.location.y < 0:
                self.location.y = self.game.world_height
            elif self.location.y > self.game.world_height:
                self.location.y = 0
        else:
            half_width = self.rect.width / 2
            half_height = self.rect.height / 2

            self.location.x = max(self.location.x, half_width)
            self.location.x = min(self.location.x, self.game.world_width - half_width)
            self.location.y = max(self.location.y, half_height)
            self.location.y = min(self.location.y, self.game.world_height - half_height)
    
    def check_blackholes(self):
        hits = pygame.sprite.spritecollide(self, self.game.blackholes, False, pygame.sprite.collide_mask)

        for blackhole in hits:
            if self.escape_time == 0:
                blackhole.apply(self)

    def check_pulsars(self):
        hits = pygame.sprite.spritecollide(self, self.game.pulsars, False, pygame.sprite.collide_mask)

        for pulsar in hits:
            if self.escape_time == 0:
                pulsar.apply(self)

    def check_escape_time(self):
        self.escape_time = max(self.escape_time - 1, 0)

        if self.escape_time == 0:
            self.controls_enabled = True

    def update(self, *args, **kwargs):
        self.rotate_to(self.angle)
        self.move()
        self.check_boundaries()
        self.check_asteroids()
        self.check_blackholes()
        self.check_pulsars()
        self.check_items()
        self.check_escape_time()
        self.rotate_amount(self.rotational_speed)


class Laser(Entity):

    def __init__(self, game, image, location, angle):
        super().__init__(game, image, location)

        self.rotate_to(angle)
        radians = math.radians(angle)
        self.velocity = pygame.Vector2(math.cos(radians), -1 * math.sin(radians)) * settings.LASER_SPEED

    def update(self, *args, **kwargs):
        self.move()

        distance_traveled_squared = self.location.distance_squared_to(self.original_location)

        if distance_traveled_squared > settings.MAX_LASER_DISTANCE ** 2:
            self.kill()
