import datetime as dt
import json
import pygame
import sys
import string
import math
import neat

from entities.tarnished import Tarnished
from entities.margit import Margit
from entities.base import Entity
from entities.actions import Actions
from entities.exceptions import *

from config.settings import *

# from utilities import draw_text


pygame.font.init()

######## DELETE GAME STATES ############
from pathlib import Path

[f.unlink() for f in Path("game_states").glob("*") if f.is_file()] 

##################


# Initialize Pygame
pygame.init()

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flatten Ring")

BG = pygame.image.load("assets/stage.png")

tarnished = None
margit = None

tarnished_neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            TARNISH_NEAT_PATH)

margit_neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            MARGIT_NEAT_PATH)

# Create the population
population_tarnished = neat.Population(tarnished_neat_config)
population_margit = neat.Population(margit_neat_config)

curr_pop = 0
curr_gen = 0

# Define the fitness function
def eval_genomes(genomes_tarnished, genomes_margit, config_tarnished, config_margit):
    global curr_gen
    global curr_pop
    curr_pop = 0
    curr_gen += 1

    print(type(genomes_tarnished))
    print(type(genomes_margit))
    if type(genomes_tarnished) == dict:
        genomes_tarnished = list(genomes_tarnished.items())
    if type(genomes_margit) == dict:
        genomes_margit = list(genomes_margit.items())

    # Initializing everything to 0 and not None
    for _, genome in genomes_tarnished:
        genome.fitness = 0
    for _, genome in genomes_margit:
        genome.fitness = 0

    for (genome_id_player, genome_tarnished), (genome_id_enemy, genome_margit) in zip(genomes_tarnished, genomes_margit):
        

        # Create separate neural networks for player and enemy
        player_net = neat.nn.FeedForwardNetwork.create(genome_tarnished, config_tarnished)
        enemy_net = neat.nn.FeedForwardNetwork.create(genome_margit, config_margit)
        
        # Run the simulation
        player_fitness, enemy_fitness = main(player_net, enemy_net)
        
        # Assign fitness to each genome
        genome_tarnished.fitness = player_fitness
        genome_margit.fitness = enemy_fitness

        assert genome_tarnished.fitness is not None
        assert genome_margit.fitness is not None

def draw_text(surface, text, x, y, font_size=20, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw():
    global curr_gen
    global curr_pop
    WIN.blit(BG, (0,0))

    tarnished.draw(WIN)
    margit.draw(WIN)

    # Draw the name below the health bar
    draw_text(WIN, "Generation: " + str(curr_gen), 200, 500, font_size=50, color=(255, 0, 0))
    draw_text(WIN, "Population: " + str(curr_pop), 200, 600, font_size=50, color=(255, 0, 0))

    pygame.display.update()

def main(tarnished_net, margit_net) -> tuple[int]:
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
    global tarnished
    global margit
    global curr_pop
    curr_pop += 1

    # Reset the npcs
    tarnished = Tarnished()
    margit = Margit()

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
    updates = 0
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

            # Get actions from current state
            tarnish_actions = get_tarnished_actions(tarnished_net, curr_state)
            curr_state["tarnished"]["actions"] = tarnish_actions
            margit_actions = get_margit_actions(margit_net, curr_state)
            curr_state["margit"]["actions"] = margit_actions
            
            # Do tarnished action first
            tarnished.do_actions(tarnish_actions)
            margit.do_actions(margit_actions)

            # Game logic here
            tarnished.update()
            margit.update()

            draw()
            
            game_result["game_states"].append(curr_state)
            updates += 1
            # print(updates)
            if updates > MAX_UPDATES_PER_GAME:
                game_result["notes"] = "Game stalemated"
                running = False
    except TarnishedDied:
        # Update winner
        game_result["winner"] = "margit"
        # Update the state of the last game tick for tarnished status
        game_result["game_states"][-1]["tarnished"]["state"] = tarnished.get_state()
    except MargitDied as e:
        # Update winner
        game_result["winner"] = "tarnished"
        # Update the state of the last game tick for margit status
        game_result["game_states"][-1]["margit"]["state"] = margit.get_state()
        game_result["notes"] = "Margit died to: " + str(e)
    finally:
        # Record our game state
        last_state = game_result["game_states"][-1]
        game_result["tarnished_fitness"] = int(get_tarnished_fitness(game_result))
        game_result["margit_fitness"] = int(get_margit_fitness(game_result))

        file_name = f"{dt.datetime.now().time()}"
        file_name += f"-{game_result['tarnished_fitness']}"
        file_name += f"-{game_result['margit_fitness']}"
        file_name += f"-{game_result['fitness_version']}"
        file_name += f"-{game_result['game_version']}"
        file_name += ".json"
        file_name = file_name.replace(":", "_")
        with open(f"game_states/{file_name}", 'w') as f:
            json.dump(game_result, f, indent=4)
    
    return game_result["tarnished_fitness"], game_result["margit_fitness"]

### Actions ###


TARNISHED_OUTPUT_MAP = [ # ABSOLUTELY CRITICAL THIS IS NOT TOUCHED OR THE NETWORK WILL NEED TO BE RETRAINED
    Actions.PLEFT,
    Actions.PRIGHT,
    Actions.PFORWARD,
    Actions.PBACK,
    Actions.PTURNL,
    Actions.PTURNR,
    Actions.PDODGE,
    Actions.PATTACK,
]

def get_tarnished_actions(net, gamestate) -> list[Actions]:
    """_summary_

    Args:
        tarnished_net (_type_): _description_
        gamestate (_type_): _description_

    TARNISHED_INPUT_MAP = [
        X Position
        Y Position
        Current Angle
        Margit X
        Margit Y
        Margit's angle
        Margit's current action
        Time remaining in Margit action
    ]
    """
    tarnished_state = gamestate["tarnished"]["state"]
    margit_state = gamestate["margit"]["state"]
    inputs = (
        tarnished_state["x"],
        tarnished_state["y"],
        tarnished_state["angle"],
        margit_state["x"],
        margit_state["y"],
        margit_state["angle"],
        margit_state["current_action"] or -1,
        margit_state["time_in_action"],
    )
    # Now get the recommended outputs
    outputs = net.activate(inputs)

    # Now map to actions
    # Go through every element in the output, and if it exists, then place the corresponding
    # action into the list.
    actions = [TARNISHED_OUTPUT_MAP[i] for i in range(len(outputs)) if outputs[i]]
    # print(actions)
    
    return prune_actions(actions)

MARGIT_OUTPUT_MAP = [ # ABSOLUTELY CRITICAL THIS IS NOT TOUCHED OR THE NETWORK WILL NEED TO BE RETRAINED
    Actions.MLEFT,
    Actions.MRIGHT,
    Actions.MFORWARD,
    Actions.MBACK,
    Actions.MTURNL,     # NOTE!!!!!!!!!!!!!!! I moved L and R here, because the order was wrong, despite the warning. I think it should be fine.
    Actions.MTURNR,
    Actions.MRETREAT,
    Actions.MSLASH,
    Actions.MREVSLASH,
    Actions.MDAGGERS,
]

def get_margit_actions(net, gamestate) -> list[Actions]:
    """_summary_

    Args:
        net (_type_): _description_
        gamestate (_type_): _description_
    
    MARGIT_INPUT_MAP = [
        X Position
        Y Position
        Current Angle
        Tarnished X
        Tarnished Y
        Tarnished's angle
        Tarnished's current action
        Time remaining in Tarnished action
    ]
    """
    tarnished_state = gamestate["tarnished"]["state"]
    margit_state = gamestate["margit"]["state"]
    inputs = (
        margit_state["x"],
        margit_state["y"],
        margit_state["angle"],
        tarnished_state["x"],
        tarnished_state["y"],
        tarnished_state["angle"],
        tarnished_state["current_action"] or -1,
        tarnished_state["time_in_action"],
    )

    # Now get the recommended outputs
    outputs = net.activate(inputs)
    
    # Now map to actions
    # Go through every element in the output, and if it exists, then place the corresponding
    # action into the list.
    actions = [MARGIT_OUTPUT_MAP[i] for i in range(len(outputs)) if outputs[i]]

    print(actions)
    return prune_actions(actions)

def prune_actions(actions: list[Actions]):
    """Take a list of actions and prune out the actions that would cancel each other out, meaning they wont be used.

    Mainly prunes out the rights and lefts in the inputs.

    Args:
        actions (_type_): _description_
    """
    # Left/right
    a = Actions
    if a.PLEFT in actions and a.PRIGHT in actions:
        actions.remove(a.PLEFT)
        actions.remove(a.PRIGHT)
    if a.MLEFT in actions and a.MRIGHT in actions:
        actions.remove(a.MLEFT)
        actions.remove(a.MRIGHT)
    
    # Forward/Back
    if a.PFORWARD in actions and a.PBACK in actions:
        actions.remove(a.PFORWARD)
        actions.remove(a.PBACK)
    if a.MFORWARD in actions and a.MBACK in actions:
        actions.remove(a.MFORWARD)
        actions.remove(a.MBACK)

    # Turning
    if a.PTURNL in actions and a.PTURNR in actions:
        actions.remove(a.PTURNL)
        actions.remove(a.PTURNR)
    if a.MTURNL in actions and a.MTURNR in actions:
        actions.remove(a.MTURNL)
        actions.remove(a.MTURNR)

    return actions


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


def determine_primary_action(outputs: list[Actions]) -> Actions:
    """Determine what the primary action that was taken the previous turn.

    e.g. MOVE, TURN, ATTACK

    Attack is the primary action, because the others would not be executed due to action priority.

    Args:
        outputs (list[Actions]): _description_

    Returns:
        Actions: _description_

    Details:
        Will be used when giving fitness points for not spamming the same move twice in a row.
    """
    pass

####### Fitness ############

def get_tarnished_fitness(result):
    last_state = result["game_states"][-1]
    settings = FitnessSettings.Tarnished
    fitness = 0

    # Reward for damaging % more the enemy than you got damaged
    # tarnished_percent = last_state["tarnished"]["state"]["health"] / last_state["tarnished"]["state"]["max_health"]
    # margit_percent = last_state["margit"]["state"]["health"] / last_state["margit"]["state"]["max_health"]
    # diff = tarnished_percent - margit_percent
    # if diff > 0:
    #     fitness += diff * 10
    margit_missing_health = last_state["margit"]["state"]["max_health"] - last_state["margit"]["state"]["health"]
    fitness += margit_missing_health * settings.DAMAGE_MULTIPLER

    last_distance = None
    last_dist_traveled = None
    last_actions = None
    for frame in result["game_states"]:
        ### Reward Tarnished for proximity to Margit
        # Calculate proximity
        tx, ty = (frame["tarnished"]["state"]["x"], frame["tarnished"]["state"]["y"])
        mx, my = (frame["margit"]["state"]["x"], frame["margit"]["state"]["y"])

        dist = math.hypot(mx - tx, my - ty)
        # Reward for each frame
        if dist < settings.MIN_DISTANCE_FOR_MAX_POINTS:
            fitness += settings.MAX_PROXIMITY_POINTS_PER_UPDATE
        else:
            # We are outside of the minimum distance, so scale points given based on how far away from this min distance
            fitness += (settings.MAX_PROXIMITY_POINTS_PER_UPDATE * settings.MIN_DISTANCE_FOR_MAX_POINTS) / dist

        ### Reward for moving around
        curr_moved = last_state["tarnished"]["state"]["moved"]
        if last_distance and last_distance > dist:
            # Last update we closed some distance to the enemy, good deadpool
            if last_dist_traveled and (diff := curr_moved - last_dist_traveled):
                fitness += diff * settings.DIST_TRAVELED_MULT

        ### Reward for choosing different actions than the last frame
        curr_actions = frame["tarnished"]["actions"]
        if last_actions:
            if last_actions != curr_actions:
                fitness += settings.NEW_ACTION_BONUS

        last_actions = curr_actions
        last_distance = dist
        last_dist_traveled = curr_moved
    
    if result["winner"] == "tarnished":
        # Major fitness points, this is very hard
        fitness += settings.WIN
    elif result["winner"] == "draw":
        # only slight fitness loss, but I want to encourage them to fight
        fitness += settings.DRAW
    else:
        # You lost, but % health will already take a big beating, so slight punishment
        # This avoids stacking loss too much that they are scared to fight at all
        fitness += settings.DRAW
    
    fitness += len(result["game_states"]) * 0.1

    if "fall" in result["notes"]:
        # Don't fall into pits
        fitness -= 150
    
    return fitness


def get_margit_fitness(result):
    last_state = result["game_states"][-1]
    settings = FitnessSettings.Margit
    fitness = 0

    last_distance = None
    last_actions = None
    last_dist_traveled = None
    for frame in result["game_states"]:
        # Reward for moving around
        curr_moved = last_state["margit"]["state"]["moved"]
        if last_dist_traveled and (diff := curr_moved - last_dist_traveled):
            fitness += diff * settings.DIST_TRAVELED_MULT

        # Reward Margit for proximity to Tarnished
        # Calculate proximity
        tx, ty = (frame["tarnished"]["state"]["x"], frame["tarnished"]["state"]["y"])
        mx, my = (frame["margit"]["state"]["x"], frame["margit"]["state"]["y"])

        dist = math.hypot(mx - tx, my - ty)
        # Reward for each frame
        if dist < settings.MIN_DISTANCE_FOR_MAX_POINTS:
            fitness += settings.MAX_PROXIMITY_POINTS_PER_UPDATE
        else:
            fitness += (settings.MAX_PROXIMITY_POINTS_PER_UPDATE * settings.MIN_DISTANCE_FOR_MAX_POINTS) / dist

        ### Reward for moving around
        curr_moved = last_state["margit"]["state"]["moved"]
        if last_distance and last_distance > dist:
            # Last update we closed some distance to the enemy, good deadpool
            if last_dist_traveled and (diff := curr_moved - last_dist_traveled):
                fitness += diff * settings.DIST_TRAVELED_MULT

        ### Reward for choosing different actions than the last frame
        curr_actions = frame["margit"]["actions"]
        if last_actions:
            if last_actions != curr_actions:
                fitness += settings.NEW_ACTION_BONUS
        
        last_distance = dist
        last_actions = curr_actions
        last_dist_traveled = curr_moved
    
    # Reward for damaging % more the enemy than you got damaged
    tarnished_percent = last_state["tarnished"]["state"]["health"] / last_state["tarnished"]["state"]["max_health"]
    margit_percent = last_state["margit"]["state"]["health"] / last_state["margit"]["state"]["max_health"]
    diff = (margit_percent - tarnished_percent)
    # Now check which direction it is in, and weight it accordingly
    if diff < 0:
        # NOTE: += because diff is already negative
        fitness += diff * 2 # Heavier losses if we lose more than if we gain more
    else:
        fitness += diff

    if result["winner"] == "tarnished":
        # Major fitness points, Margit should not lose
        fitness += settings.LOSS
    elif result["winner"] == "draw":
        # Biggest draw loss on Margit, he should be pressuring Tarnished
        fitness += settings.DRAW
    else:
        # Margit's expected victory
        fitness += settings.WIN
    
    return fitness


if __name__ == "__main__":
    # Run NEAT for player and enemy separately
    
    # print(type(genomes))
    print(type(population_margit.population))
    try:
        winner_player = population_tarnished.run(lambda genomes, config: eval_genomes(genomes, population_margit.population, config, margit_neat_config), n=GENERATIONS)
        winner_enemy = population_margit.run(lambda genomes, config: eval_genomes(population_tarnished.population, genomes, tarnished_neat_config, config), n=GENERATIONS)
    except Exception as e:
        with open("debug.txt", "w") as f:
            f.write(str(e))
    

pygame.quit()
