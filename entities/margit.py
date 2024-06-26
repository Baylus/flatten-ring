import pygame

from config.settings import TPS, WIDTH, HEIGHT, MARGIT_IMAGE, HEALTH_BAR_HEIGHTS, HEALTH_BAR_WIDTHS, DEFAULT_HEALTH_BAR_PADDING
from utilities import calculate_new_xy, draw_health_bar

from .base import Entity
from .actions import Actions
from .attacks.margit_weapons import Slash, Dagger

class Margit(Entity):
    """Margit, the enemy boss.

    Generally Margit is much slower than the Tarnished both in speed and turn speed, but has more hp, 
    and no dodge (MAY CHANGE, but it will be more cumbersome if it is added).

    Margit will have more hp and cannot fall off the platform, but will have less
    access to inputs from the player, like what their angle is to dodge the Tarnished's
    attacks or to predict where they will exit dodge from.

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
        self.hitbox_coefficient = 1.1

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
                "speed": 50,
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
                self.time_left_in_action -= 1
                self.lead_time_before_action -= 1
                if self.lead_time_before_action == 0:
                    # print("We are done with lead time for margit attack")
                    # We have to start the attacks
                    if self.current_action == Actions.MSLASH:
                        # Doing regular slash attack
                        self.slash.start_attack()
                    elif self.current_action == Actions.MREVSLASH:
                        # Doing regular slash attack
                        self.rev_slash.start_attack()
                    elif self.current_action == Actions.MDAGGERS:
                        # We actually are going to be creating the daggers here, as opposed to "starting" them
                        self.make_dagger()
                return
            
            if not actions:
                return
            
            # Try to attack
            moves = [Actions.MSLASH, Actions.MREVSLASH, Actions.MDAGGERS]
            moves = [x for x in actions if x in moves]
            if moves:
                # print("Starting Margit attack")
                # Start a swing
                if Actions.MSLASH in moves:
                    self.current_action = Actions.MSLASH
                    self.time_left_in_action = self.weapon_details[Actions.MSLASH]["attack_time"]
                    # NOTE: We have to set the damage back, because we will be using the current damage on the weapon
                    # to disable the weapon from damaging the character again.
                    self.slash.damage = self.weapon_details[Actions.MSLASH]["damage"]
                    self.lead_time_before_action = self.weapon_details[Actions.MSLASH]["lead_time"]
                elif Actions.MREVSLASH in moves:
                    self.current_action = Actions.MREVSLASH
                    self.time_left_in_action = self.weapon_details[Actions.MREVSLASH]["attack_time"]
                    # NOTE: We have to set the damage back, because we will be using the current damage on the weapon
                    # to disable the weapon from damaging the character again.
                    self.slash.damage = self.weapon_details[Actions.MREVSLASH]["damage"]
                    self.lead_time_before_action = self.weapon_details[Actions.MREVSLASH]["lead_time"]
                elif Actions.MDAGGERS in moves:
                    self.current_action = Actions.MDAGGERS
                    self.time_left_in_action = self.weapon_details[Actions.MDAGGERS]["attack_time"]
                    self.lead_time_before_action = self.weapon_details[Actions.MDAGGERS]["lead_time"]
                
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
                if moves[0] == Actions.MTURNL:
                    self.angle -= self.turn_speed
                else:
                    self.angle += self.turn_speed
        finally:
            stay_in_arena()

    def update(self):
        if self.current_action and self.lead_time_before_action < 1:
            # print("we are processing updates on margits attacks")
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
        if self.current_action and self.lead_time_before_action < 1:
            if Actions.MSLASH == self.current_action:
                self.slash.draw(surface)
            elif Actions.MREVSLASH == self.current_action:
                self.rev_slash.draw(surface)
        
        for x in self.daggers:
            x.draw(surface)
        
        
        draw_health_bar(
            surface,
            WIDTH - HEALTH_BAR_WIDTHS - DEFAULT_HEALTH_BAR_PADDING,
            HEALTH_BAR_HEIGHTS + DEFAULT_HEALTH_BAR_PADDING,
            HEALTH_BAR_WIDTHS,
            HEALTH_BAR_HEIGHTS,
            self.health,
            self.max_health,
            self.name)
        
    def get_state(self):
        state = super().get_state()
        state["weapons"] = {
            Actions.MSLASH: self.slash.get_state(),
            Actions.MREVSLASH: self.rev_slash.get_state(),
            Actions.MDAGGERS: [x.get_state() for x in self.daggers]
        }

        return state

    def set_state(self, state: dict):
        """Uses input state to set and configure Margit and his weapons.

        Organized like the output from 'get_state'

        Args:
            state (dict): _description_
        """
        super().set_state(state)
        # Update weapons
        slash_state = state["weapons"][str(Actions.MSLASH)]
        if slash_state:
            # This weapon was being used.
            self.slash.set_state(slash_state)
        else:
            # We arent attacking in new state, so make sure weapon is stopped.
            self.slash.stop_attack()
        
        rev_slash_state = state["weapons"][str(Actions.MREVSLASH)]
        if rev_slash_state:
            # This weapon was being used.
            self.rev_slash.set_state(rev_slash_state)
        else:
            # We arent attacking in new state, so make sure weapon is stopped.
            self.rev_slash.stop_attack()
        
        daggers_state = state["weapons"][str(Actions.MDAGGERS)]
        if daggers_state:
            # There are existing daggers in new state.
            for i in range(len(daggers_state)):
                # For each dagger, either update current daggers or add new ones
                if len(self.daggers) > i:
                    # There is an existing dagger capable of updating to this state
                    self.daggers[i].set_state(daggers_state[i])
                else:
                    # We have more daggers in new state than in current one. Add more
                    new_dagger = daggers_state[i]
                    self.make_dagger(new_dagger["x"], new_dagger["y"], new_dagger["angle"])
            
            # Now we got done with making all the daggers. If there are anymore left 
            # in current daggers, we need to remove them.
            while len(self.daggers) > len(daggers_state):
                self.daggers.pop()
    
    def give_target(self, target):
        """Determines target which instantiates the weapon.

        Args:
            target (Entity): Target to damage
        """
        self.target = target
        self.slash = Slash(self, target)
        self.rev_slash = Slash(self, target, reversed=True)

    def make_dagger(self, x = None, y = None, angle = None, speed = None, dmg = None):
        x = x or self.x # default to self.x
        y = y or self.y # default to self.y
        angle = angle or self.angle # default to self.angle

        speed = speed or self.weapon_details[Actions.MDAGGERS]["speed"]
        dmg = dmg or self.weapon_details[Actions.MDAGGERS]["damage"]
        self.daggers.append(Dagger(self, self.target, x, y, angle, speed, dmg))