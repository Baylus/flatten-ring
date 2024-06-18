from .base import Entity
from .actions import Actions

class Margit(Entity):
    """_summary_

    Args:
        Entity (_type_): _description_

    Actions, in order of priority:
        Attack (Will supercede all actions following this)
        Move in cardinal directions
        Retreat (Will supercede all actions following this, except for daggers)
        Turn

    Attacks:
        Sky jump
        Slash
        Reverse Slash
        Whirlwind
        Daggers
            Two daggers shot towards player
    """

    def __init__(self):
        self.name = "Margit"

        self.health = 3000
        self.max_health = 3000
        

        self.x = 600
        self.y = 600

        self.width = 100
        self.height = 100
        
        # self. = 

    def do_actions(self, actions):
        """Handle all actions provided

        Args:
            actions (_type_): _description_
        """
        # TODO: Check if dodging, as we will need to keep moving during that
        if self.busy():
            # Tarnished is currently busy, and cannot act.
            self.time_in_action -= 1
        
        moves = [Actions.MFORWARD, Actions.MBACK, Actions.MLEFT, Actions.MRIGHT]
        moves = [x for x in actions if x in moves]
        if moves:
            # We have some moves to do
            self.move(moves)