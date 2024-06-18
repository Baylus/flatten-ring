import pygame

from .base import Entity
from .actions import Actions
from utilities import calculate_new_xy
from .exceptions import TarnishedDied
from settings import TPS, HEIGHT

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
    # dodgespeed: int = 10
    turn_speed = 7

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
        
        if self.busy():
            # Tarnished is currently busy, and cannot act.
            if self.current_action == Actions.PDODGE:
                new_pos = calculate_new_xy((self.x, self.y), self.velocity * 1.5, self.angle)
                self.x, self.y = new_pos

            self.time_in_action -= 1
            return
        
        # Trigger death if we have fell into ravine.
        if self.y > HEIGHT - 150 or self.y < 150:
            # We have fallen into pit
            self.health = 0
            raise TarnishedDied("Fell into pit")

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
        
        # Now is the appropriate time to dodge, almost entirely because we have 
        # the new movement angle we need to determine our trajectory. 
        if Actions.PDODGE in actions:
            # We are dodging
            self.current_action = Actions.PDODGE
            self.time_in_action = 30
            self.angle = move_ang
            return # Can't do any other actions now.

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