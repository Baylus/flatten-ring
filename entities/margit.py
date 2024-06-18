import pygame

from settings import TPS, WIDTH, HEIGHT, MARGIT_IMAGE
from .base import Entity
from .actions import Actions
from .attacks.margit_weapons import Slash

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
        self.target = None

        self.x = 1200
        self.y = 600
        self.angle = 180

        self.width = 100
        self.height = 100

        self.weapon_details = {
            Actions.MSLASH: {
                "object": None,
                "damage": 8,
                "lead_time": 7,
                "attack_time": 15
            },
            Actions.MREVSLASH: {
                "object": None,
                "damage": 5,
                "lead_time": 5,
                "attack_time": 12
            },
            Actions.MDAGGERS: {
                "object": None,
                "damage": 3,
                "lead_time": 2,
                "attack_time": 5
            }
        }

        self.slash: Slash = None
        self.rev_slash = None
        self.bullets = []
        
        self.lead_time_before_action: int = 0

    def do_actions(self, actions):
        """Handle all actions provided

        Args:
            actions (_type_): _description_
        """
        
        def stay_in_arena():
            """Ensues that we are colliding with walls properly if we are going to hit them.
            """
            w = self.width / 2
            min_left = 150 + w
            max_right = WIDTH - 150 - w
            max_up = 150 + w
            min_down = HEIGHT - 150 - w

            if self.x < min_left: # Collide left
                self.x = min_left
            elif self.x > max_right: # Collide right
                self.x = max_right
            
            if self.y < max_up: # Don't fall up
                self.y = max_up
            elif self.y > min_down: # Don't fall down
                self.y = min_down
        try:
            # TODO: Check if dodging, as we will need to keep moving during that
            if self.busy():
                # Tarnished is currently busy, and cannot act.
                self.time_in_action -= 1
            
            moves = [Actions.MFORWARD, Actions.MBACK, Actions.MLEFT, Actions.MRIGHT]
            moves = [x for x in actions if x in moves]
            if moves:
                # We have some moves to do
                self.move(moves)

            
            moves = [Actions.MTURNL, Actions.MTURNR]
            moves = [x for x in actions if x in moves]
            if len(moves) == 1:
                # We have to turn
                print(f"We have to turn: {moves[0]}")
                if moves[0] == Actions.MTURNL:
                    self.angle -= self.turn_speed
                else:
                    self.angle += self.turn_speed
        finally:
            stay_in_arena()

    def update(self):
        # self.weapon.update()
        pass
    
    def draw(self, surface):
        rotated_image = pygame.transform.rotate(MARGIT_IMAGE, -self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, new_rect.topleft)
        # self.weapon.draw(surface)
    
    
    def give_target(self, target):
        """Determines target which instantiates the weapon.

        Args:
            target (Entity): Target to damage
        """
        self.target = target
        self.slash = Slash(self, target)
