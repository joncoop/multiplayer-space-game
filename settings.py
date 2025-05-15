import pygame


# Window settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CAPTION = "My Awesome Game"
FPS = 60

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)

# Fonts
PRIMARY_FONT = 'assets/fonts/recharge bd.ttf'
SECONDARY_FONT = None

# World
WORLD_WIDTH = 10000
WOLRD_HEIGHT = 10000
WORLD_WRAP = False

# Ship
SHIP_IMG = 'assets/images/player_ships/playerShip1_blue.png'
SHIP_MAX_SPEED = 16
SHIP_TURN_SPEED = 2
ACCELERATION = 0.50
DRAG = 0.01  # 0=No drag, 1=Instant stop
MIN_VELOCITY_SQUARED = 0.25

# Lasers
PLAYER_LASER = 'assets/images/lasers/laserBlue05.png'
LASER_SPEED = 24
MAX_LASER_DISTANCE = 3000

# Effects
FIRE = 'assets/images/effects/fire13.png'

# Items
POWERUP_IMG = 'assets/images/powerups/powerupYellow_bolt.png'

# Asteroids
NUM_ASTEROIDS = 50
ASTEROID_IMGS = ['assets/images/meteors/meteorGrey_big1.png',
                 'assets/images/meteors/meteorGrey_big2.png',
                 'assets/images/meteors/meteorGrey_big3.png',
                 'assets/images/meteors/meteorGrey_big4.png',
                 'assets/images/meteors/meteorGrey_med1.png',
                 'assets/images/meteors/meteorGrey_med2.png',
                 'assets/images/meteors/meteorGrey_small1.png',
                 'assets/images/meteors/meteorGrey_small2.png']

ASTEROID_MIN_SPEED = 2
ASTEROID_MAX_SPEED = 8
ASTEROID_MIN_ROTATION_SPEED = 1
ASTEROID_MAX_ROTATION_SPEED = 4

# Blackholes
BLACKHOLE_IMG = 'assets/images/blackholes/blackhole_small.png'

# Sounds
SHOOT_SND = 'assets/sounds/laser.ogg'
EXPLOSION_SND = 'assets/sounds/explosion.ogg'
POWERUP_SND = 'assets/sounds/powerup.wav'

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
ROTATION_OFFSET = 90  # # In degreees, use if original image isn't pointing right (0 on unit circle)
