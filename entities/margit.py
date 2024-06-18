import pygame

from settings import TPS, WIDTH, HEIGHT, MARGIT_IMAGE
from .base import Entity
from .actions import Actions
from .attacks.margit_weapons import Slash, Dagger

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

        self.health = 300
        self.max_health = 300
        self.target = None

        self.x = 1200
        self.y = 600
        self.angle = 180

        self.width = 100
        self.height = 100

        self.weapon_details = {
            Actions.MSLASH: {
                "damage": 8,
                "lead_time": 7,
                "attack_time": 15 # Total time spent locked, including lead time
            },
            Actions.MREVSLASH: {
                "damage": 5,
                "lead_time": 4,
                "attack_time": 10
            },
            Actions.MDAGGERS: {
                "damage": 3,
                "lead_time": 2,
                "attack_time": 5
            }
        }

        self.slash: Slash = None
        self.rev_slash: Slash = None
        self.daggers: list[Dagger] = []
        
        self.lead_time_before_action: int = 0

    def do_actions(self, actions):
        """Handle all actions provided

        Args:
            actions (_type_): _description_
        """
        
        def stay_in_arena():
            """Ensues that we are colliding with walls properly if we are going to hit them.
            This also enforces, unlike the tarnished, that Margit never falls into the ravine.
            This is because Elden ring also enforces it, and I dont want the Tarnished to try to take
            extreme measures trying to bait margit to fall into the ravine to "cheat" the system.
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
                # Margit is currently busy, and cannot act.
                self.time_in_action -= 1
                self.lead_time_before_action -= 1
                if self.lead_time_before_action == 0:
                    # We have to start the attacks
                    if self.current_action == Actions.MSLASH:
                        # Doing regular slash attack
                        self.slash.start_attack()
                    elif self.current_action == Actions.MREVSLASH:
                        # Doing regular slash attack
                        self.slash.start_attack()
                    elif self.current_action == Actions.MDAGGERS:
                        # We actually are going to be creating the daggers here, as opposed to "starting" them
                        dspeed = self.weapon_details[Actions.MDAGGERS]["speed"]
                        ddmg = self.weapon_details[Actions.MDAGGERS]["damage"]
                        self.daggers.append(Dagger(self.x, self.y, self.angle, dspeed, ddmg))
                return
            
            if not actions:
                return
            
            # Try to attack
            moves = [Actions.MSLASH, Actions.MREVSLASH, Actions.MDAGGERS]
            moves = [x for x in actions if x in moves]
            if moves:
                print("Starting Margit attack")
                # Start a swing
                if Actions.MSLASH in moves:
                    self.current_action = Actions.MSLASH
                    self.time_in_action = self.weapon_details[Actions.MSLASH]["attack_time"]
                    # NOTE: We have to set the damage back, because we will be using the current damage on the weapon
                    # to disable the weapon from damaging the character again.
                    self.slash.damage = self.weapon_details[Actions.MSLASH]["damage"]
                    self.lead_time_before_action = self.weapon_details[Actions.MSLASH]["lead_time"]
                elif Actions.MREVSLASH in moves:
                    self.current_action = Actions.MREVSLASH
                    self.time_in_action = self.weapon_details[Actions.MREVSLASH]["attack_time"]
                    # NOTE: We have to set the damage back, because we will be using the current damage on the weapon
                    # to disable the weapon from damaging the character again.
                    self.slash.damage = self.weapon_details[Actions.MREVSLASH]["damage"]
                    self.lead_time_before_action = self.weapon_details[Actions.MREVSLASH]["lead_time"]
                elif Actions.MDAGGERS in moves:
                    pass
                
                return

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
        if self.current_action and self.lead_time_before_action < 1:
            print("we are processing updates on margits attacks")
            # We don't have to wait any longer before our attack can start
            if self.current_action == Actions.MSLASH:
                self.slash.update()
            elif self.current_action == Actions.MREVSLASH:
                self.rev_slash.update()
        
        if self.daggers:
            for x in self.daggers[:]: # Copy list because we will be removing elements from it.
                if x.time_left < 1:
                    self.daggers.remove(x)
                else:
                    x.update()
    
    def draw(self, surface):
        rotated_image = pygame.transform.rotate(MARGIT_IMAGE, -self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, new_rect.topleft)
        if Actions.MSLASH == self.current_action:
            self.slash.draw(surface)
        elif Actions.MREVSLASH == self.current_action:
            self.rev_slash.draw(surface)
        
        for x in self.daggers:
            x.draw()
        
    
    
    def give_target(self, target):
        """Determines target which instantiates the weapon.

        Args:
            target (Entity): Target to damage
        """
        self.target = target
        self.slash = Slash(self, target)
        self.rev_slash = Slash(self, target, reversed=True)
