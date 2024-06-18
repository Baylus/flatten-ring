import pygame
import sys

from entities.tarnished import Tarnished
from entities.margit import Margit
from entities.base import Entity
from entities.actions import Actions

WIDTH, HEIGHT = 2000, 1200
# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flatten Ring")

BG = pygame.image.load("assets/stage.png")
TPS = 60 # Ticks per second, not sure if this matters


tarnished = Tarnished()
margit = Margit()

entities = [tarnished, margit]

def draw(drawables: list[Entity]):
    WIN.blit(BG, (0,0))

    # TODO: This cannot possibly be the way to do this...
    for i in range(len(drawables)):
        pygame.draw.rect(WIN, entities[i].default_rect_color, drawables[i])

    pygame.display.update()

def main():
    # Initialize Pygame
    pygame.init()

    player = pygame.Rect(tarnished.x, tarnished.y, tarnished.width, tarnished.height)
    enemy = pygame.Rect(margit.x, margit.y, margit.width, margit.height)
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        clock.tick(TPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        actions = get_actions(keys)
        apply_actions(actions)

        # Game logic here

        # Garbage drawing of rectangles
        draw([player, enemy])

    pygame.quit()
    sys.exit()

def get_actions(inputs) -> list[int]:
    """Create list of actions that should be taken based on the inputs

    Args:
        inputs (_type_): keys being pressed
    """
    actions = []

    # Standard movement
    # Forward/Back
    if inputs[pygame.K_w]: # W
        actions.append(Actions.PFORWARD)
    if inputs[pygame.K_s]: # S
        if Actions.PFORWARD in actions:
            # Cancel both out, since both are pressed
            actions.remove(Actions.PFORWARD)
        else:
            actions.append(Actions.PBACK)
    # Left/right
    if inputs[pygame.K_a]: # A
        actions.append(Actions.PLEFT)
    if inputs[pygame.K_d]: # D
        if Actions.PLEFT in actions:
            # Cancel both out, since both are pressed
            actions.remove(Actions.PLEFT)
        else:
            actions.append(Actions.PRIGHT)
    # Turning
    if inputs[pygame.K_q]: # Q
        actions.append(Actions.PTURNL)
    if inputs[pygame.K_e]: # E
        if Actions.PTURNL in actions:
            # Cancel both out, since both are pressed
            actions.remove(Actions.PTURNL)
        else:
            actions.append(Actions.PTURNR)

    if inputs[pygame.K_LSHIFT]: # Dodge
        actions.append(Actions.PDODGE)
    if inputs[pygame.K_SPACE]: # Attack
        actions.append(Actions.PATTACK)
    
    ############# MARGIT ###############
    # Forward/Back
    if inputs[pygame.K_8]: # 8
        actions.append(Actions.MFORWARD)
    if inputs[pygame.K_5]: # 5
        if Actions.MFORWARD in actions:
            # Cancel both out, since both are pressed
            actions.remove(Actions.MFORWARD)
        else:
            actions.append(Actions.MBACK)
    # Left/right
    if inputs[pygame.K_4]: # 4
        actions.append(Actions.MLEFT)
    if inputs[pygame.K_6]: # 6
        if Actions.MLEFT in actions:
            # Cancel both out, since both are pressed
            actions.remove(Actions.MLEFT)
        else:
            actions.append(Actions.MRIGHT)
    # Turning
    if inputs[pygame.K_7]: # 7
        actions.append(Actions.MTURNL)
    if inputs[pygame.K_9]: # 9
        if Actions.MTURNL in actions:
            # Cancel both out, since both are pressed
            actions.remove(Actions.MTURNL)
        else:
            actions.append(Actions.MTURNR)

    if inputs[pygame.K_0]: # Dodge
        actions.append(Actions.MRETREAT)
    if inputs[pygame.K_1]: # Attack
        actions.append(Actions.MSLASH)
    if inputs[pygame.K_2]: #
        actions.append(Actions.MREVSLASH)
    if inputs[pygame.K_PLUS]:
        actions.append(Actions.MDAGGERS)

    return actions


def apply_actions(actions):
    """Apply output actions to the game state.

    Args:
        actions (_type_): List of actions to take
    """
    # Do tarnished action first
    tarnished.do_actions(actions)
    
    # Do Margit Actions
    margit.do_actions(actions)

if __name__ == "__main__":
    main()