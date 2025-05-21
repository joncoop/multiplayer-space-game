import pygame


# Window settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CAPTION = "My Awesome Game"
FPS = 60

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (150, 150, 150)
RED = (200, 0, 0)

# Fonts
PRIMARY_FONT = 'assets/fonts/recharge bd.ttf'
SECONDARY_FONT = None

# World
WORLD_WIDTH = 20000
WOLRD_HEIGHT = 20000
WORLD_WRAP = False  # Camera lag is kinda weird if True

# Ship
SHIP_IMG = 'assets/images/player_ships/playerShip1_blue.png'
SHIP_MAX_SPEED = 10
SHIP_TURN_SPEED = 2
SHIP_STARTING_SHIELD = 3
ESCAPE_TIME = 1.75 * FPS  # From black holes and pulsars

ACCELERATION = 0.50
DRAG = 0.01  # 0=No drag, 1=Instant stop
MIN_VELOCITY_SQUARED = 0.25

# Lasers
PLAYER_LASER = 'assets/images/lasers/laserBlue05.png'
LASER_SPEED = 24
MAX_LASER_DISTANCE = 3000
DOUBLE_SHOT_TIME = 6 * FPS

# Items
POWERUP_IMG = 'assets/images/items/powerupYellow_bolt.png'
ITEM_MIN_SPEED = 5
ITEM_MAX_SPEED = 10
MIN_ITEM_DISTANCE = 500
MAX_ITEM_DISTANCE = 4000

ITEMS_PER_SECOND = 0.1

# Stars
NUM_STARS = 4000

# Asteroids
NUM_ASTEROIDS = 100
ASTEROID_IMGS = ['assets/images/space_objects/meteorGrey_big1.png',
                 'assets/images/space_objects/meteorGrey_big2.png',
                 'assets/images/space_objects/meteorGrey_big3.png',
                 'assets/images/space_objects/meteorGrey_big4.png',
                 'assets/images/space_objects/meteorGrey_med1.png',
                 'assets/images/space_objects/meteorGrey_med2.png',
                 'assets/images/space_objects/meteorGrey_small1.png',
                 'assets/images/space_objects/meteorGrey_small2.png']

ASTEROID_MIN_SPEED = 2
ASTEROID_MAX_SPEED = 8
ASTEROID_MIN_ROTATION_SPEED = 1
ASTEROID_MAX_ROTATION_SPEED = 4

# Blackholes
BLACKHOLE_IMG = 'assets/images/space_objects/blackhole_384x384.png'
BLACKHOLE_MIN_ROTATION_SPEED = 3
BLACKHOLE_MAX_ROTATION_SPEED = 8
BLACKHOLE_FADE_RATE = 0.999
BLACKHOLE_CAPTURE_THRESHOLD = 1

# Pulsars
PULSAR_IMG = 'assets/images/space_objects/pulsar_256x151.png'
PULSAR_ROTATION_SPEED = 10

# Sounds
SHOOT_SND = 'assets/sounds/laser.ogg'
EXPLOSION_SND = 'assets/sounds/explosion.ogg'
ITEM_SND = 'assets/sounds/powerup.wav'

# Music
TITLE_MUSIC = 'assets/music/calm_happy.ogg'
MAIN_THEME = 'assets/music/cooking_mania.wav'

# Gameplay settings
CONTROLS = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'thrust': pygame.K_UP,
    'shoot': pygame.K_SPACE,
    'respawn': pygame.K_r,
}

# Math stuff
ROTATION_OFFSET = 90  # In degreees, use if original image isn't pointing right (0 on unit circle)
