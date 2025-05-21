# Standard Library Imports
import random

# Third-Party Imports
import pygame

# Local Imports
import src.camera as camera
import src.entities as entities
import src.overlays as overlays
import settings


# Main game class 
class Game:

    START = 0
    PLAYING = 1
    END = 2

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()

        self.screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_assets()
        self.make_overlays()
        self.new_game()

    def load_assets(self):
        self.ship_img = pygame.image.load(settings.SHIP_IMG).convert_alpha()
        self.laser_img = pygame.image.load(settings.PLAYER_LASER).convert_alpha()
        self.blackhole_img = pygame.image.load(settings.BLACKHOLE_IMG).convert_alpha()
        self.pulsar_img = pygame.image.load(settings.PULSAR_IMG).convert_alpha()
        self.powerup_img = pygame.image.load(settings.POWERUP_IMG).convert_alpha()
        self.asteroid_imgs = [pygame.image.load(img).convert_alpha() for img in settings.ASTEROID_IMGS]

    def make_overlays(self):
        self.title_screen = overlays.TitleScreen(self)
        self.game_over_screen = overlays.GameOverScreen(self)
        self.hud = overlays.HUD(self)
        self.minimap = overlays.Minimap(self)
        
    def new_game(self):
        self.world_width = settings.WORLD_WIDTH
        self.world_height = settings.WOLRD_HEIGHT

        self.players = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.blackholes = pygame.sprite.Group()
        self.pulsars = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        
        self.start_location = [9800, 10200]
        self.ship = entities.Ship(self, self.ship_img, self.start_location, settings.CONTROLS)
        self.players.add(self.ship)

        self.camera = camera.ScrollingCamera(self.screen, [self.world_width, self.world_height], self.ship, 0.8)

        self.scene = Game.START

        for _ in range(settings.NUM_ASTEROIDS):
            x = random.randrange(0, self.world_width)
            y = random.randrange(0, self.world_width)
            img = random.choice(self.asteroid_imgs)
            asteroid = entities.Asteroid(self, img, [x, y])
            self.asteroids.add(asteroid)            
        
        # make black hole teleporters
        loc1 = [7500, 7500]
        loc2 = [12500, 12500]
        blackhole1 = entities.BlackHole(self, self.blackhole_img, loc1, loc2)
        blackhole2 = entities.BlackHole(self, self.blackhole_img, loc2, loc1)
        self.blackholes.add(blackhole1, blackhole2)

        # make powerup-spewing pulsar
        loc = [self.world_width // 2, self.world_height // 2]
        pulsar = entities.Pulsar(self, self.pulsar_img, loc)
        self.pulsars.add(pulsar)

        # maybe make stars sprites later, or perhaps make a StarField class
        self.star_locs = [] 
        for _ in range(settings.NUM_STARS):
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
        if self.scene == Game.PLAYING:
            self.pulsars.update()
            self.lasers.update()
            self.blackholes.update()
            self.asteroids.update()
            self.items.update()
            self.players.update()

        self.camera.update()

    def render(self):
        group_drawing_order = [self.blackholes, self.lasers, self.asteroids, self.items, self.pulsars, self.players]
        offset_x, offset_y = self.camera.get_offsets()

        self.screen.fill(settings.BLACK)

        for loc in self.star_locs:
            x = loc[0] - offset_x
            y = loc[1] - offset_y
            r = random.randint(0, 25) # Magic number alert!
            color = settings.WHITE if r == 0 else settings.LIGHT_GRAY
            pygame.draw.circle(self.screen, color, [x, y], 3)

        for group in group_drawing_order:
            for sprite in group:
                x = sprite.rect.x - offset_x
                y = sprite.rect.y - offset_y
                self.screen.blit(sprite.image, [x, y])
        
        # World boundary
        pygame.draw.rect(self.screen, settings.RED, [-offset_x, -offset_y, self.world_width, self.world_height], 2)

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

            # For debugging & navigation help
            extra_caption_info = f"Angle={self.ship.angle} Speed={self.ship.velocity.length(): .2f} location={self.ship.location} FPS={self.clock.get_fps(): .2f}"
            pygame.display.set_caption(f"{settings.CAPTION} {extra_caption_info}")

            pygame.display.update()
            self.clock.tick(settings.FPS)

        pygame.quit()