from argparse import ArgumentParser
import datetime as dt
import json
import math
import neat
import os
import pathlib
import pygame
import shutil
import string
import sys


from fitness import get_tarnished_fitness, get_margit_fitness

from entities.tarnished import Tarnished
from entities.margit import Margit
from entities.base import Entity
from entities.actions import Actions
from entities.exceptions import *

from config.settings import *

pygame.font.init()

########## STARTUP CLEANUP

# DELETE GAME STATES #

folder = GAMESTATES_PATH
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Delete debug file to ensure we arent looking at old exceptions
pathlib.Path.unlink("debug.txt", missing_ok=True)


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
curr_trainer = "Unknown"

# Define the fitness function
def eval_genomes(genomes_tarnished, genomes_margit, config_tarnished, config_margit):
    global curr_gen
    global curr_pop
    curr_pop = 0
    curr_gen += 1
    pathlib.Path(f"{GAMESTATES_PATH}/gen_{curr_gen}").mkdir(parents=True, exist_ok=True)

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
    global curr_trainer
    WIN.blit(BG, (0,0))

    tarnished.draw(WIN)
    margit.draw(WIN)

    # Draw the name below the health bar
    draw_text(WIN, "Trainer: " + str(curr_trainer), 200, 400, font_size=40, color=(255, 0, 0))
    draw_text(WIN, "Generation: " + str(curr_gen), 200, 500, font_size=40, color=(255, 0, 0))
    draw_text(WIN, "Population: " + str(curr_pop), 200, 600, font_size=40, color=(255, 0, 0))

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
    global curr_gen
    global curr_trainer
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

        # file_name = f"{dt.datetime.now().time()}"
        # file_name += f"-{game_result['tarnished_fitness']}"
        # file_name += f"-{game_result['margit_fitness']}"
        # file_name += f"-{game_result['fitness_version']}"
        # file_name += f"-{game_result['game_version']}"
        file_name = str(curr_pop) + f"_{curr_trainer}"
        file_name += ".json"
        file_name = file_name.replace(":", "_")
        with open(f"{GAMESTATES_PATH}/gen_{curr_gen}/{file_name}", 'w') as f:
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

    if not SILENT:
        print(f"Margit's actions we found: {actions}")
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


# To fix it from doing n-1 checkpoint numbers
class OneIndexedCheckpointer(neat.Checkpointer):
    def __init__(self, generation_interval=1, time_interval_seconds=None, filename_prefix="neat-checkpoint-"):
        super().__init__(generation_interval, time_interval_seconds, filename_prefix)

    def save_checkpoint(self, config, population, species_set, generation):
        # Increment the generation number by 1 to make it 1-indexed
        super().save_checkpoint(config, population, species_set, generation + 1)

def get_newest_checkpoint_file(files: list[str], prefix: str) -> tuple[str, int]:
    """Gets the most recent checkpoint from the previous run the resume the training.

    Args:
        files (list[str]): _description_
        prefix (str): _description_

    Returns:
        tuple[str, int]: <file name, generation number>
    """
    def get_gen_num_from_name(file_name: str) -> int:
        if file_name[-1] == '-':
            raise ValueError(f"There is something really wrong. This checkpoint file is missing a gen number: {file_name}")
        max_gen_num_len = len(str(GENERATIONS))
        postfix = file_name[ -max_gen_num_len :]
        for i in range(len(postfix)):
            if postfix[i] == '-':
                # We found the dash, the rest is the gen number
                return int(postfix[i+1:])
        else:
            # We had no '-', so this whole thing must be the gen number
            return int(postfix)
    
    file_details = ["", 0]
    prefixed = [fn for fn in files if prefix in fn] # Files containing the prefix
    for name in prefixed:
        gen = get_gen_num_from_name(name)
        if gen > file_details[1]:
            file_details = (name, gen)

    return file_details


parser = ArgumentParser()
parser.add_argument("-r", "--reset", dest="reset", action="store_true", default=False,
                    help="Reset training to not use previous checkpoints", metavar="FILE")
parser.add_argument("-q", "--quiet",
                    # action="store_false", dest="verbose", default=True,
                    action="store_true", dest="quiet", default=False,
                    help="don't print status messages to stdout. Unused")

args = parser.parse_args()

if __name__ == "__main__":
    # Add reporters, including a Checkpointer
    if CACHE_CHECKPOINTS:
        # Setup checkpoints
        curr_fitness_checkpoints = f"{CHECKPOINTS_PATH}/{FITNESS_VERSION}"
        pathlib.Path(curr_fitness_checkpoints).mkdir(parents=True, exist_ok=True)
        ### Find the run that we need to use
        # Get run directories
        runs = os.listdir(curr_fitness_checkpoints)
        run_val = 1
        for i in range(1, 10):
            if f"run_{i}" not in runs:
                if not RESTORE_CHECKPOINTS or args["reset"]:
                    # We are not restoring from checkpoints, so we need to make a new directory, which would be the i'th run dir
                    run_val = i
                break
        else:
            # If this happens then I have been running too many runs and I need to think of changing the fitnesss function
            raise Exception("Youve been trying this fitness function too many times. Fix the problem.")

        # We are going to be creating new checkpoint files
        this_runs_checkpoints = f"{curr_fitness_checkpoints}/run_{i}"
        pathlib.Path(this_runs_checkpoints).mkdir(parents=True, exist_ok=True)

        # Generation numbers we are starting on for each trainer. Used to determine if we need to train margit
        # first to catch up to tarnished (incase a run is stopped during margit's training, meaning he will be
        # behind in training one full cycle)
        start_gen_nums = [0, 0]
        if RESTORE_CHECKPOINTS and not args["reset"]:
            # We gotta find the right run to restore
            existing_checkpoint_files = os.listdir(this_runs_checkpoints)
            if existing_checkpoint_files: 

                tarn_checkpoint, start_gen_nums[0] = get_newest_checkpoint_file(existing_checkpoint_files, TARNISHED_CHECKPOINT_PREFIX)
                checkpointer_tarnished = OneIndexedCheckpointer.restore_checkpoint(tarn_checkpoint)

                margit_checkpoint, start_gen_nums[1] = get_newest_checkpoint_file(existing_checkpoint_files, MARGIT_CHECKPOINT_PREFIX)
                checkpointer_margit = OneIndexedCheckpointer.restore_checkpoint(margit_checkpoint)
            else:
                # We didn't have any existing checkpoints within the run's folder
                print("Warning, attempted to restore checkpoints, but no checkpoints were present. If this was expected, disregard.")

        checkpointer_tarnished = OneIndexedCheckpointer(generation_interval=CHECKPOINT_INTERVAL, filename_prefix=f'{this_runs_checkpoints}/{TARNISHED_CHECKPOINT_PREFIX}')
        checkpointer_margit = OneIndexedCheckpointer(generation_interval=CHECKPOINT_INTERVAL, filename_prefix=f'{this_runs_checkpoints}/{MARGIT_CHECKPOINT_PREFIX}')
        
        population_tarnished.add_reporter(neat.StdOutReporter(True))
        population_tarnished.add_reporter(neat.StatisticsReporter())
        population_tarnished.add_reporter(checkpointer_tarnished)
        population_margit.add_reporter(neat.StdOutReporter(True))
        population_margit.add_reporter(neat.StatisticsReporter())
        population_margit.add_reporter(checkpointer_margit)
    
    try:
        if start_gen_nums[0] > start_gen_nums[1]:
            # Margit is behind tarnished because we cancelled run during his training
            # Let him catch up with one cycle before going into loop
            curr_gen = start_gen_nums[1]
            generations_to_catchup = start_gen_nums[0] - start_gen_nums[1]
            curr_trainer = "Margit"
            winner_margit = population_margit.run(lambda genomes, config: eval_genomes(population_tarnished.population, genomes, tarnished_neat_config, config), n=generations_to_catchup)
        
        # Co train margit/tarnished so they learn together
        for gen in range(start_gen_nums[0], GENERATIONS, TRAINING_INTERVAL):
            # Run NEAT for player and enemy separately
            curr_gen = gen
            curr_trainer = "Tarnished"
            winner_tarnished = population_tarnished.run(lambda genomes, config: eval_genomes(genomes, population_margit.population, config, margit_neat_config), n=TRAINING_INTERVAL)
            curr_gen = gen
            curr_trainer = "Margit"
            winner_margit = population_margit.run(lambda genomes, config: eval_genomes(population_tarnished.population, genomes, tarnished_neat_config, config), n=TRAINING_INTERVAL)
    except Exception as e:
        with open("debug.txt", "w") as f:
            f.write(str(e))
        raise
    

pygame.quit()
