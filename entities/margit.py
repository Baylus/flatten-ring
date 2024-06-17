from .base import Entity

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