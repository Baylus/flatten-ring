import pygame

from .actions import Actions
from utilities import calculate_new_xy

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

    image_url: str
    default_rect_color: str = "red"
    # pygame_obj = None

    def __init__(self):
        super().__init__()
        # self.pygame_obj = pygame.Rect(self.x, self.y, self.width, self.height)
        pass

    def busy(self) -> bool:
        if self.current_action:
            if self.time_in_action > 0:
                return True
            else:
                # We still have our current action, but we finished it.
                self.current_action = None
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
        print(f"Old position {(self.x, self.y)}.... New pos {new_pos}")
        self.x, self.y = new_pos

        return move_ang

        
    def dodge(self):
        raise NotImplementedError

    def take_damage(self):
        raise NotImplementedError