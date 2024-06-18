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
        self.angle = 0 # TRYING TO ADJUST THIS LINE

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
        move_ang = self.angle
        if moves:
            # We have some moves to do
            print("We have to move, heres our actions: ")
            print(moves)
            move_ang = self.move(moves)
        # Now is the appropriate time to dodge, because we have the new angle at which we are
        # going.
        if Actions.PDODGE in actions:
            # We are dodging
            pass

        moves = [Actions.PTURNL, Actions.PTURNR]
        moves = [x for x in actions if x in moves]
        if len(moves) == 1:
            # We have to turn
            print(f"We have to turn: {moves[0]}")
            if moves[0] == Actions.PTURNL:
                self.angle -= self.turn_speed
            else:
                self.angle += self.turn_speed

    def dodge(self):
        """Commence dodge
        """
        # Find out angle at which we are dodging