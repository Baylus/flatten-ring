import pygame
from enum import Enum

WIDTH, HEIGHT = 2000, 1200
TPS = 1000 # Ticks per second

HEALTH_BAR_WIDTHS = 100
HEALTH_BAR_HEIGHTS = 20
DEFAULT_HEALTH_BAR_PADDING = 25

MAX_UPDATES_PER_GAME = 1000

GAME_VERSION = "V0.1"
FITNESS_VERSION = "V0.7"

# Load entity images
TARNISHED_IMAGE = pygame.image.load("assets/tarnished.png")
MARGIT_IMAGE = pygame.image.load("assets/margit.png")

# NEAT STUFF

TARNISH_NEAT_PATH = "config/neat_config_tarnished.txt"
MARGIT_NEAT_PATH = "config/neat_config_margit.txt"

GENERATIONS = 50

class FitnessSettings:
    class Tarnished:
        MIN_DISTANCE_FOR_MAX_POINTS = 100
        MAX_PROXIMITY_POINTS_PER_UPDATE = 2
        DAMAGE_MULTIPLER = 15
        DIST_TRAVELED_MULT = 0.2 # Raw distance traveled
        NEW_ACTION_BONUS = 3

        # Major fitness points, this is very hard
        WIN = 300
        # only slight fitness loss, but I want to encourage them to fight
        DRAW = -25
        # You lost, but % health will already take a big beating, so slight punishment
        # This avoids stacking loss too much that they are scared to fight at all
        LOSS = -15


    class Margit:
        MIN_DISTANCE_FOR_MAX_POINTS = 100
        MAX_PROXIMITY_POINTS_PER_UPDATE = 2
        DAMAGE_MULTIPLIER = 15
        DIST_TRAVELED_MULT = 0.2 # Raw distance traveled
        NEW_ACTION_BONUS = 3

        # Margit's expected victory
        WIN = 100
        # Big draw loss on Margit, he should be pressuring Tarnished
        DRAW = -50
        # Major fitness points, Margit should not lose
        LOSS = -300


# FITNESS_SETTINGS = {
#     TARNISHED: {
#         MIN_DISTANCE_FOR_MAX_POINTS: 
#     }
# }