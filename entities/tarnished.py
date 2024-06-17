from .base import Entity

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
        
        # self. = 