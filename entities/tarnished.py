import pygame

from utilities import calculate_new_xy
from settings import TPS, WIDTH, HEIGHT, TARNISHED_IMAGE
# from main import margit

from .base import Entity
from .actions import Actions
from .exceptions import TarnishedDied
from .weapon import Weapon

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
    turn_speed = 7
    weapon_damage = 5

    def __init__(self):
        self.name = "Tarnished"

        self.health = 3
        self.max_health = 3

        self.x = 600
        self.y = 600
        self.angle = 0

        self.width = 100
        self.height = 100
        
        self.default_rect_color = "green"
        self.pygame_obj = pygame.Rect(self.x, self.y, self.width, self.height)
        self.weapon = None

    def do_actions(self, actions):
        """Handle all actions provided

        Args:
            actions (_type_): _description_
        """
        def collide_walls():
            """Ensues that we are colliding with walls properly if we are going to hit them.
            """
            min_left = 150 + self.width / 2
            max_right = WIDTH - 150 - self.width / 2
            if self.x < min_left:
                self.x = min_left
            elif self.x > max_right:
                self.x = max_right
        try:
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
            
            # Try to attack
            if Actions.PATTACK in actions:
                # Start a swing
                self.current_action = Actions.PATTACK
                self.time_in_action = 10
                # NOTE: We have to set the damage back, because we will be using the current damage on the weapon
                # to disable the weapon from damaging the character again.
                self.weapon.damage = self.weapon_damage
                self.weapon.start_attack()
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
        finally:
            # No matter what, we are ensuring that we did not move into walls
            collide_walls()

    def update(self):
        self.weapon.update()

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(TARNISHED_IMAGE, -self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, new_rect.topleft)
        self.weapon.draw(surface)
    
    def give_target(self, target):
        """Determines target which instantiates the weapon.

        Args:
            target (Entity): Target to damage
        """
        self.weapon = Weapon(self, target)