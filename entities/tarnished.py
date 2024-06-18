import pygame

from .base import Entity
from .actions import Actions

class Tarnished(Entity):
    """_summary_

    Args:
        Entity (_type_): _description_

    Actions, in order of priority:
        Attack (Will supercede all actions following this)
        Move in cardinal directions
        Dodge (Will supercede all actions following this)
        Turn
    """

    def __init__(self):
        self.name = "Tarnished"

        self.health = 3
        self.max_health = 3

        self.x = 600
        self.y = 600

        self.width = 100
        self.height = 100
        
        self.default_rect_color = "green"
        self.pygame_obj = pygame.Rect(self.x, self.y, self.width, self.height)

    def do_actions(self, actions):
        """Handle all actions provided

        Args:
            actions (_type_): _description_
        """
        # TODO: Check if dodging, as we will need to keep moving during that
        if self.busy():
            # Tarnished is currently busy, and cannot act.
            self.time_in_action -= 1
        
        if not actions:
            return
        
        moves = [Actions.PFORWARD, Actions.PBACK, Actions.PLEFT, Actions.PRIGHT]
        moves = [x for x in actions if x in moves]
        if moves:
            # We have some moves to do
            print("We have to move, heres our actions: ")
            print(moves)
            self.move(moves)