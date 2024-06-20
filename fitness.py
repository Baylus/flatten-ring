import math

from entities.actions import Actions, get_primary_action

class FitnessSettings:
    class Tarnished:
        MIN_DISTANCE_FOR_MAX_POINTS = 100
        MAX_PROXIMITY_POINTS_PER_UPDATE = 2
        DAMAGE_MULTIPLER = 15
        DIST_TRAVELED_MULT = 0.2 # Raw distance traveled
        NEW_ACTION_BONUS = 3

        REPEAT_ACTION_PENALTY = 1
        # This is the factor applied every single update for the number of repeated actions
        # for any given actions. e.g. say we have 10 repeated actions with penalty of 1 and 0.1 mult. We wouldnt end up with 1 total
        # we would have .1 from first update, .3 for second (2 penalties * MULT + 0.1 existing mult hit) .6, 1.0, 1.5, 2.1, etc...
        REPEAT_ACTION_MULT = 0.1

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

        REPEAT_ACTION_PENALTY = 1
        # This is the factor applied every single update for the number of repeated actions
        # for any given actions. e.g. say we have 10 repeated actions with penalty of 1 and 0.1 mult. We wouldnt end up with 1 total
        # we would have .1 from first update, .3 for second (2 penalties * MULT + 0.1 existing mult hit) .6, 1.0, 1.5, 2.1, etc...
        REPEAT_ACTION_MULT = 0.1

        # Margit's expected victory
        WIN = 100
        # Big draw loss on Margit, he should be pressuring Tarnished
        DRAW = -50
        # Major fitness points, Margit should not lose
        LOSS = -300

"""
Just a little primer for the game states since they are used a lot here

    {
        "winner": "draw",
        "tarnished_fitness": 408,
        "margit_fitness": 283,
        "game_version": "V0.1",
        "fitness_version": "V0.8",
        "notes": "Game stalemated",
        "game_states": [
            {
                "tick": 347,
                "tarnished": {
                    "state": {
                        "x": 600,
                        "y": 600,
                        "health": 100,
                        "max_health": 100,
                        "current_action": null,
                        "time_in_action": 0,
                        "angle": 0,
                        "moved": 0,
                        "weapons": {
                            "8": {}
                        }
                    },
                    "actions": [
                        7,
                        8
                    ]
                },
                "margit": {
                    "state": {
                        "x": 1200,
                        "y": 600,
                        "health": 300,
                        "max_health": 300,
                        "current_action": null,
                        "time_in_action": 0,
                        "angle": 180,
                        "moved": 0,
                        "weapons": {
                            "16": {},
                            "17": {},
                            "18": []
                        }
                    },
                    "actions": [
                        9,
                        12,
                        17,
                        18
                    ]
                }
            },
            ...
    }

Returns:
    _type_: _description_
"""

# Example game state
EX_GAME_STATE = {
    "winner": "draw",
    "tarnished_fitness": 408,
    "margit_fitness": 283,
    "game_version": "V0.1",
    "fitness_version": "V0.8",
    "notes": "Game stalemated",
    "game_states": [
        {
            "tick": 347,
            "tarnished": {
                "state": {
                    "x": 600,
                    "y": 600,
                    "health": 100,
                    "max_health": 100,
                    "current_action": None,
                    "time_in_action": 0,
                    "angle": 0,
                    "moved": 0,
                    "weapons": {
                        "8": {}
                    }
                },
                "actions": [
                    7,
                    8
                ]
            },
            "margit": {
                "state": {
                    "x": 1200,
                    "y": 600,
                    "health": 300,
                    "max_health": 300,
                    "current_action": None,
                    "time_in_action": 0,
                    "angle": 180,
                    "moved": 0,
                    "weapons": {
                        "16": {},
                        "17": {},
                        "18": []
                    }
                },
                "actions": [
                    9,
                    12,
                    17,
                    18
                ]
            }
        },
    ]
}

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
    last_action: Actions = None
    # Increasing penalty for repeated actions
    repeat_action_penalty = 0
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

        ### Penalty for choosing same actions as the last update
        curr_action = get_primary_action(last_state["tarnished"]["actions"])
        if not curr_action:
            # We really don't want them not moving
            repeat_action_penalty += settings.REPEAT_ACTION_PENALTY * 2
        elif last_action and last_action == curr_action:
            # We did the same thing last update
            repeat_action_penalty += settings.REPEAT_ACTION_PENALTY

            # CONSIDER: Moving this penalty out of this to punish every update even if this one wasnt a repeat
            fitness -= repeat_action_penalty * settings.REPEAT_ACTION_MULT

        last_action = curr_action
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
    last_action = None
    last_dist_traveled = None
    repeat_action_penalty = 0
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

        ### Penalty for choosing same actions as the last update
        curr_action = get_primary_action(last_state["margit"]["actions"])
        if not curr_action:
            # We really don't want them not moving
            repeat_action_penalty += settings.REPEAT_ACTION_PENALTY * 2
        elif last_action and last_action == curr_action:
            # We did the same thing last update
            repeat_action_penalty += settings.REPEAT_ACTION_PENALTY

            # CONSIDER: Moving this penalty out of this to punish every update even if this one wasnt a repeat
            fitness -= repeat_action_penalty * settings.REPEAT_ACTION_MULT
        
        # CONSIDER: Also giving a penalty for Margit choosing an attack two updates in a row

        last_action = curr_action
        last_distance = dist
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
