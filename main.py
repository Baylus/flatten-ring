import datetime as dt
import json
import pygame
import sys
import string

from entities.tarnished import Tarnished
from entities.margit import Margit
from entities.base import Entity
from entities.actions import Actions
from entities.exceptions import *

from settings import WIDTH, HEIGHT, TPS, GAME_VERSION, FITNESS_VERSION

# Initialize Pygame
pygame.init()

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flatten Ring")

BG = pygame.image.load("assets/stage.png")

tarnished = Tarnished()
margit = Margit()

entities = [tarnished, margit]

def draw():
    WIN.blit(BG, (0,0))

    # draw_entity(tarnished, TARNISHED_IMAGE)
    tarnished.draw(WIN)
    # draw_entity(margit, MARGIT_IMAGE)
    margit.draw(WIN)

    pygame.display.update()

def draw_entity(entity: Entity, image):
    # Rotate the image
    rotated_image = pygame.transform.rotate(image, -entity.angle)
    # Get the new rect with the center in the correct position
    new_rect = rotated_image.get_rect(center=(entity.x, entity.y))
    # Draw the rotated image on the screen
    WIN.blit(rotated_image, new_rect.topleft)

def main():
    # Initial housekeeping
    """Game states:
    Game states will be comprised of several things:
        - Current states of all objects
        - Outputs from the network
    Each of these will be for every tick we process, from which we will log them
    all utilizing this metric.

    Once the game has finished, the total game status will be stored with all the
    game states, the current game version, the fitness version,
    the winner of the match, and the total fitness for each side.
    """
    game_result = { # For recording all other elements and storing final output of logging function
        "winner": "draw", # Default incase something fails
        "tarnished_fitness": 0,
        "margit_fitness": 0,
        "game_version": GAME_VERSION,
        "fitness_version": FITNESS_VERSION,
        "notes": "",
        "game_states": []
    }

    tarnished.give_target(margit)
    margit.give_target(tarnished)

    clock = pygame.time.Clock()
    try:
        # Main game loop
        running = True
        while running:
            clock.tick(TPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            curr_state = {
                "tick": pygame.time.get_ticks(),
                "tarnished": {
                    "state": tarnished.get_state()
                },
                "margit": {
                    "state": margit.get_state()
                }
            }

            keys = pygame.key.get_pressed()
            actions = get_actions(keys)
            
            # Add actions chosen to our game state.
            curr_state["tarnished"]["actions"] = [x for x in actions if int(x) < int(Actions.MLEFT)]
            curr_state["margit"]["actions"] = [x for x in actions if  int(x) >= int(Actions.MLEFT)]
            
            apply_actions(actions)

            # Game logic here
            tarnished.update()
            margit.update()

            draw()
            
            game_result["game_states"].append(curr_state)
    except TarnishedDied:
        # Update winner
        game_result["winner"] = "margit"
        # Update the state of the last game tick for tarnished status
        game_result["game_states"][-1]["tarnished"]["state"] = tarnished.get_state()
    except MargitDied:
        # Update winner
        game_result["winner"] = "tarnished"
        # Update the state of the last game tick for margit status
        game_result["game_states"][-1]["margit"]["state"] = margit.get_state()
    finally:
        # Record our game state
        last_state = game_result["game_states"][-1]
        game_result["tarnished_fitness"] = get_tarnished_fitness(last_state)
        game_result["margit_fitness"] = get_margit_fitness(last_state)

        file_name = f"{dt.datetime.now().time()}"
        file_name += f"-{game_result['tarnished_fitness']}"
        file_name += f"-{game_result['margit_fitness']}"
        file_name += f"-{game_result['fitness_version']}"
        file_name += f"-{game_result['game_version']}"
        file_name += ".json"
        file_name = file_name.replace(":", "_")
        with open(f"game_states/{file_name}", 'w') as f:
            json.dump(game_result, f, indent=4)
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
    if inputs[pygame.K_2]: # Reverse attack
        actions.append(Actions.MREVSLASH)
    if inputs[pygame.K_3]: # Daggers
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

####### Fitness ############

def get_tarnished_fitness(state):
    return 0

def get_margit_fitness(state):
    return 0


if __name__ == "__main__":
    main()