import pygame

WIDTH, HEIGHT = 2000, 1200
TPS = 60 # Ticks per second

HEALTH_BAR_WIDTHS = 100
HEALTH_BAR_HEIGHTS = 20
DEFAULT_HEALTH_BAR_PADDING = 25

GAME_VERSION = "V0.1"
FITNESS_VERSION = "V0.0"

# Load entity images
TARNISHED_IMAGE = pygame.image.load("assets/tarnished.png")
MARGIT_IMAGE = pygame.image.load("assets/margit.png")