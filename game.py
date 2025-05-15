# Imports
import random
import pygame

from entities import *
from overlays import *
from settings import *
from camera import *


# Main game class 
class Game:

    START = 0
    PLAYING = 1
    END = 2

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()

        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        print(self.screen.get_rect())
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_assets()
        self.new_game()
        self.make_overlays()

    def load_assets(self):
        self.ship_img = pygame.image.load(SHIP_IMG).convert_alpha()
        self.laser_img = pygame.image.load(PLAYER_LASER).convert_alpha()
        self.blackhole_img = pygame.image.load(BLACKHOLE_IMG).convert_alpha()
        self.asteroid_imgs = [pygame.image.load(img).convert_alpha()
                              for img in ASTEROID_IMGS]

    def make_overlays(self):
        self.title_screen = TitleScreen(self)
        self.game_over_screen = GameOverScreen(self)
        self.hud = HUD(self)
        self.minimap = Minimap(self, self.players)
        
    def new_game(self):
        self.world_width = WORLD_WIDTH
        self.world_height = WOLRD_HEIGHT

        self.players = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.blackholes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        
        self.start_location = WORLD_WIDTH // 2, WOLRD_HEIGHT // 2
        self.ship = Ship(self, self.ship_img, self.start_location, CONTROLS)
        self.players.add(self.ship)


        self.all_sprites.add(self.players)

        self.camera = ScrollingCamera(self.screen, [self.world_width, self.world_height], self.ship, 0.8)

        self.scene = Game.START

        for _ in range(NUM_ASTEROIDS):
            x = random.randrange(0, self.world_width)
            y = random.randrange(0, self.world_width)
            img = random.choice(self.asteroid_imgs)
            asteroid = Asteroid(self, img, [x, y])
            self.asteroids.add(asteroid)            
        
        # make blackhole teleporters
        loc1 = [2500, 2500]
        loc2 = [7500, 7500]
        blackhole1 = BlackHole(self, self.blackhole_img, loc1, loc2)
        blackhole2 = BlackHole(self, self.blackhole_img, loc2, loc1)
        self.blackholes.add(blackhole1, blackhole2)

        # maybe make stars sprites later, or perhaps make a StarField class
        self.star_locs = [] 
        for _ in range(3000):
            x = random.randrange(0, self.world_width)
            y = random.randrange(0, self.world_width)
            self.star_locs.append([x, y])

    def start_playing(self):
        self.scene = Game.PLAYING

    def process_input(self):
        filtered_events = []
        pressed_keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # start/restart
                if self.scene == Game.START and event.key == pygame.K_SPACE:
                    self.start_playing()
                elif event.key == pygame.K_n:
                    self.new_game()

                # camera
                elif event.key == pygame.K_c:
                    self.camera.toggle()

                # actual gameplay
                else:
                    filtered_events.append(event)

        if self.scene == Game.PLAYING:
            self.ship.act(filtered_events, pressed_keys)
     
    def update(self):
        self.all_sprites.add(self.lasers, self.asteroids, self.blackholes)

        if self.scene == Game.PLAYING:
            self.all_sprites.update()

        self.camera.update()

    def render(self):
        offset_x, offset_y = self.camera.get_offsets()

        self.screen.fill(BLACK)

        for loc in self.star_locs:
            x = loc[0] - offset_x
            y = loc[1] - offset_y
            pygame.draw.circle(self.screen, WHITE, [x, y], 3)

        for sprite in self.all_sprites:
            x = sprite.rect.x - offset_x
            y = sprite.rect.y - offset_y
            self.screen.blit(sprite.image, [x, y])
        
        # World boundary
        pygame.draw.rect(self.screen, RED, [-offset_x, -offset_y, self.world_width, self.world_height], 2)

        self.hud.draw(self.screen)
        self.minimap.draw(self.screen)
        self.camera.draw(self.screen)

        if self.scene == Game.START:
            self.title_screen.draw(self.screen)
        elif self.scene == Game.END:
            self.game_over_screen.draw(self.screen)
        
    def play(self):
        while self.running:
            self.process_input()     
            self.update()     
            self.render()
            pygame.display.set_caption(f"{CAPTION} Angle={self.ship.angle} Speed={self.ship.velocity.length(): .2f} FPS={self.clock.get_fps(): .2f},location={self.ship.location}")
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
