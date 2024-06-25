import pygame

from utilities import calculate_new_xy
from config.settings import *

from .exceptions import CharacterDied
from .actions import Actions

class Entity():
    name: str
    health: int = 100
    max_health: int = 100
    iframes: int = 0    # Not default, remaining iframes
    velocity: int = 5

    current_action: int = None # May be used for playbacks or actions that lock you out of others, or are dangerous to opponent
    time_in_action: int = 0 # Time remaining while locked in current action, in ticks

    x: int = 1000
    y: int = 600
    width: int = 100
    height: int = 100
    angle: int = 0 # Where it is currently looking
    turn_speed: int = 5 # How fast the character can rotate, degrees/tick

    hitbox_coefficient = 1

    # Statistics
    moved = 0

    def __init__(self):
        super().__init__()
        # self.pygame_obj = pygame.Rect(self.x, self.y, self.width, self.height)
        pass

    def busy(self) -> bool:
        if self.current_action:
            if self.time_left_in_action > 0:
                return True
            else:
                # We still have our current action, but we finished it.
                self.current_action = None
                self.time_left_in_action = 0 # Make sure its reset properly
                return False
        return False
    
    def do_actions(self, actions):
        raise NotImplementedError

    def attack(self):
        raise NotImplementedError

    def move(self, actions: list[Actions]) -> int:
        """Moves at a certain angle depending on current look angle and which directions we are moving to.

        Args:
            actions (list[Actions]): _description_

        Returns:
            int: The angle at which we were moving.
        """
        # CONSIDER: Adjust distance traveled when moving backwards.
        ang_offset = 0
        if len(actions) > 1:
            # If we are moving in more than one way.
            if any([True for x in [Actions.PFORWARD, Actions.MFORWARD] if x in actions]):
                # Check if moving left
                if any([True for x in [Actions.PLEFT, Actions.MLEFT] if x in actions]):
                    # We are moving forward left
                    ang_offset = -45
                else:
                    # We are moving forward right
                    ang_offset = 45
            else:
                # We are moving backwards
                if any([True for x in [Actions.PLEFT, Actions.MLEFT] if x in actions]):
                    # We are moving backward left
                    ang_offset = -135
                else:
                    # We are moving backward right
                    ang_offset = 135
        else:
            # We only have one direction we are traveling. NOTE: Dont need to check
            # if it is forwards, the offset will be 0 in that case.
            if any([True for x in [Actions.PLEFT, Actions.MLEFT] if x in actions]):
                ang_offset = -90
            if any([True for x in [Actions.PRIGHT, Actions.MRIGHT] if x in actions]):
                ang_offset = 90
            if any([True for x in [Actions.PBACK, Actions.MBACK] if x in actions]):
                ang_offset = 180
        
        # Find movement angle and adjust distance
        move_ang = self.angle + ang_offset
        new_pos = calculate_new_xy((self.x, self.y), self.velocity, move_ang)
        if not SILENT:
            print(f"Old position {(self.x, self.y)}.... New pos {new_pos}")
        self.x, self.y = new_pos

        self.moved += self.velocity

        return move_ang


    def get_state(self) -> dict:
        """Gets the total status needed for a given character for the game state

        Returns:
            Dictionary of the following items
                x position
                y position

        """
        status = {}
        status["x"] = self.x
        status["y"] = self.y
        status["health"] = self.health
        status["max_health"] = self.max_health
        status["current_action"] = self.current_action
        status["time_in_action"] = self.time_in_action
        status["angle"] = self.angle
        status["moved"] = self.moved

        return status

    def set_state(self, state: dict):
        """Uses output from 'get_state' to set the current configuration of the entity

        Used for replays to easily manipulate entities.
        """
        self.x = state["x"]
        self.y = state["y"]
        self.health = state["health"]
        self.max_health = state["max_health"]
        self.current_action = state["current_action"]

    def take_damage(self, damage: int) -> int:
        """Forces character to take specified amount of damage

        Args:
            damage (int): Number of damage to take

        Raises:
            CharacterDied: Characters health reached 0 or less

        Returns:
            int: Number of damage taken
        """
        if self.iframes > 0:
            if not SILENT:
                print("Entity would have been hit, but currently has invincibility frames")
        else:
            self.health -= damage
            if self.health < 1:
                raise CharacterDied
            return damage
        return 0

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width * self.hitbox_coefficient, self.height * self.hitbox_coefficient)