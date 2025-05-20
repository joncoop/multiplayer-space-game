import math
import random

import pygame

from settings import *

# Base Entity Class
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
            self.image = pygame.transform.rotate(self.original_image, angle - ROTATION_OFFSET)
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


# Player Ship
class Ship(Entity):

    def __init__(self, game, image, location, controls):
        super().__init__(game, image, location)

        self.controls = controls
        self.angle = 90
        self.previous_angle = self.angle
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 0
        self.blackhole_escape_time = 0
        self.controls_disabled = False
        self.shield = SHIP_STARTING_SHIELD
        self.doubleshot_time = 0

    def act(self, events, keys):
        if self.controls_disabled:
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
        self.angle += SHIP_TURN_SPEED
        self.angle %= 360

    def rotate_right(self):
        self.previous_angle = self.angle
        self.angle -= SHIP_TURN_SPEED
        self.angle %= 360

    def thrust(self):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), -1 * math.sin(radians))
        self.velocity += direction * ACCELERATION

        if self.velocity.length_squared() > SHIP_MAX_SPEED ** 2:
            self.velocity.scale_to_length(SHIP_MAX_SPEED) 

    def slow(self):
        self.velocity *= 1 - DRAG

        if self.velocity.length_squared() < MIN_VELOCITY_SQUARED:
            self.velocity.update(0, 0)

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
        self.blackhole_escape_time = 0
        self.controls_disabled = False

    def check_asteroids(self):
        hits = pygame.sprite.spritecollide(self, self.game.asteroids, False, pygame.sprite.collide_mask)

        if hits:
            self.respawn()  # should probably blow up and lose lives or something

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, self.game.items, True, pygame.sprite.collide_mask)

        for item in hits:
            item.apply(self)

        if self.doubleshot_time > 0:
            self.doubleshot_time -= 1

    def check_boundaries(self):
        if WORLD_WRAP:
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
            if self.blackhole_escape_time == 0:
                blackhole.apply(self)
            else:
                self.blackhole_escape_time -= 1

    def update(self, *args, **kwargs):
        self.rotate_to(self.angle)
        self.move()
        self.check_boundaries()
        self.check_blackholes()
        self.check_asteroids()
        self.check_items()


class Laser(Entity):

    def __init__(self, game, image, location, angle):
        super().__init__(game, image, location)

        self.rotate_to(angle)
        radians = math.radians(angle)
        self.velocity = pygame.Vector2(math.cos(radians), -1 * math.sin(radians)) * LASER_SPEED

    def update(self, *args, **kwargs):
        self.move()

        distance_traveled_squared = self.location.distance_squared_to(self.original_location)

        if distance_traveled_squared > MAX_LASER_DISTANCE ** 2:
            self.kill()


class Asteroid(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

        speed = random.randrange(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        angle = random.randrange(0, 360)
        radians = math.radians(angle)

        self.velocity = pygame.Vector2(math.cos(radians), -1 * math.sin(radians)) * speed
        self.rotational_speed = random.randrange(ASTEROID_MIN_ROTATION_SPEED, ASTEROID_MAX_ROTATION_SPEED)
        self.rotational_speed *= random.choice([-1, 1])

    def check_lasers(self):
        hits = pygame.sprite.spritecollide(self, self.game.lasers, False, pygame.sprite.collide_mask)

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

        self.rotational_speed = random.randrange(BLACKHOLE_MIN_ROTATION_SPEED, BLACKHOLE_MAX_ROTATION_SPEED)
        self.rotational_speed *= random.choice([-1, 1])
        self.destination = destination

    def apply(self, ship):
        if ship.blackhole_escape_time == 0:
            ship.controls_disabled = True
            ship.velocity.update(0, 0)

        if ship.controls_disabled:
            ship.location.move_towards_ip(self.location, 1)
            ship.rotate_amount(self.rotational_speed)
            ship.image.set_alpha(ship.image.get_alpha() * BLACKHOLE_FADE_RATE)
        
        if ship.location.distance_squared_to(self.location) < 1 and ship.image.get_alpha() < BLACKHOLE_CAPTURE_THRESHOLD:
            ship.move_to(self.destination)
            ship.blackhole_escape_time = BLACKHOLE_ESCAPE_TIME
            ship.controls_disabled = False
            ship.image.set_alpha(255)

    def update(self, *args, **kwargs):
        self.angle += self.rotational_speed
        self.rotate_to(self.angle)


class Item(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

        speed = random.randrange(ITEM_MIN_SPEED, ITEM_MAX_SPEED)
        self.distance_to_travel = random.randrange(MIN_ITEM_DISTANCE, MAX_ITEM_DISTANCE)
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


class ShieldBoost(Item):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

    def apply(self, ship):
        ship.shield += 1


class DoubleShot(Item):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

    def apply(self, ship):
        ship.doubleshot_time = DOUBLE_SHOT_TIME


class Pulsar(Entity):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

    def spawn_item(self):
        r = random.randrange(0, FPS)

        if r < ITEMS_PER_SECOND:
            powerup_type = random.choice([ShieldBoost, DoubleShot])
            item = powerup_type(self.game, self.game.powerup_img, self.location)
            self.game.items.add(item)

    def update(self):
        self.rotate_amount(PULSAR_ROTATION_SPEED)
        self.spawn_item()