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

#### REPLAYS
REPLAY_TPS = 15 # Ticks for replays
# Used when running replay functionality to make sure we dont accidentally clean our data
SAVE_GAMESTATES = False
DEFAULT_NUM_BEST_GENS = 5 # Default for number of best generations that 


##### NEAT STUFF

# NEAT Paths
TARNISH_NEAT_PATH = "config/neat_config_tarnished.txt"
MARGIT_NEAT_PATH = "config/neat_config_margit.txt"

CHECKPOINTS_PATH = "checkpoints/"
GAMESTATES_PATH = "game_states/"


GENERATIONS = 500 # We are really going to max out the learning now that we are continuing checkpoints
# Number of iterations that one model will train before training the other one.
TRAINING_INTERVAL = 5
CACHE_CHECKPOINTS = True
CHECKPOINT_INTERVAL = 10
RESTORE_CHECKPOINTS = True

TARNISHED_CHECKPOINT_PREFIX = "neat-checkpoint-tarnished-"
MARGIT_CHECKPOINT_PREFIX = "neat-checkpoint-margit-"

SILENT = True
PARALLEL_OVERRIDE = False