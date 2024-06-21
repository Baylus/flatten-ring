import pygame
from enum import Enum

WIDTH, HEIGHT = 2000, 1200
TPS = 1000 # Ticks per second

HEALTH_BAR_WIDTHS = 100
HEALTH_BAR_HEIGHTS = 20
DEFAULT_HEALTH_BAR_PADDING = 25

MAX_UPDATES_PER_GAME = 1000

GAME_VERSION = "V0.1"
FITNESS_VERSION = "V0.9"

# Load entity images
TARNISHED_IMAGE = pygame.image.load("assets/tarnished.png")
MARGIT_IMAGE = pygame.image.load("assets/margit.png")

##### NEAT STUFF

# NEAT Paths
TARNISH_NEAT_PATH = "config/neat_config_tarnished.txt"
MARGIT_NEAT_PATH = "config/neat_config_margit.txt"

CHECKPOINTS_PATH = "checkpoints/"
GAMESTATES_PATH = "game_states/"


GENERATIONS = 150
# Number of iterations that one model will train before training the other one.
TRAINING_INTERVAL = 5
CACHE_CHECKPOINTS = True
CHECKPOINT_INTERVAL = 10

