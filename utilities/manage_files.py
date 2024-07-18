import json
import os
import pathlib
import shutil

from config.settings import GAMESTATES_PATH


def clean_gamestates(args):
    print("Cleaning up old data")
    # DELETE GAME STATES #
    print("Cleaning up old game states")
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

    print("remove debug.txt")
    # Delete debug file to ensure we arent looking at old exceptions
    pathlib.Path.unlink("debug.txt", missing_ok=True)


def write_gamestate_to_file(game_result):
    # TODO: Use pickle to write this to a file to save on space.
    #       This will cause us not to be able to read the game results ourselves.
    pop = game_result["population"]
    gen = game_result["generation"]
    file_name = str(pop)
    file_name += ".json"
    file_name = file_name.replace(":", "_")
    with open(f"{GAMESTATES_PATH}/gen_{gen}/{file_name}", 'w') as f:
        # Don't need to prettify it, we arent reading as many of them as before. 
        # This will save space
        # json.dump(game_result, f, indent=4)
        json.dump(game_result, f)

def read_gamestate_from_file(file_name):
    # TODO: Once using pickle for writing, use it here.
    with open(file_name) as json_file:
        return json.loads(json_file)
