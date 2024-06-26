import pygame
import math

from ..base import Entity
from config.settings import SILENT

class Weapon:
    def __init__(self, owner, target, image_url = "assets/tarnished_right_slash.png", reversed = False, cone_angle = 90, attack_duration = 10):
        """_summary_

        Args:
            owner (_type_): _description_
            target (_type_): _description_
            image_url (str, optional): _description_. Defaults to "assets/tarnished_right_slash.png".
            reversed (bool, optional): _description_. Defaults to False.
            cone_angle (int, optional): How wide of a cone the strike will be. Defaults to 90.
        # TODO: Finish annotating inputs
        """
        self.owner = owner
        self.angle = 0
        self.swinging = False
        self.image = pygame.image.load(image_url)  # Load your weapon image
        self.rect = self.image.get_rect()
        self.target: Entity = target
        self.damage = 5

        self.weapon_distance = 60

        # NOTE: All the math that goes behind this reversed variable seems to be backwards to me.
        # However, whenever I try to adjust it to fit what I think is happening, it either doesnt
        # swing, or starts spinning the wrong way, so I am leaving it as is.
        self.reversed = reversed # Is swing coming from left?
        if self.reversed:
            self.start_angle_offset = cone_angle
            self.end_angle_offset = -cone_angle
        else: # Swing from left
            self.start_angle_offset = -cone_angle
            self.end_angle_offset = cone_angle
        
        self.angle_speed = cone_angle * 2 / attack_duration
        if self.reversed:
            # Since its not reversed, we are actually subtracting the angle
            self.angle_speed = -self.angle_speed
    
    def start_attack(self):
        self.swinging = True
        self.angle = self.start_angle_offset  # Reset angle at the start of the attack

    def stop_attack(self):
        self.swinging = False

    def update(self):
        if self.swinging:
            self.check_collisions()
            self.angle += self.angle_speed  # Adjust the angle increment as needed
            if not self.reversed and self.angle >= self.end_angle_offset:
                if not SILENT:
                    print(f"We have ended our swing. current angle {self.angle}, end angle {self.end_angle_offset}")
                self.swinging = False
            elif self.reversed and self.angle <= self.end_angle_offset:
                if not SILENT:
                    print(f"We have ended our reversed swing. current angle {self.angle}, end angle {self.end_angle_offset}")
                self.swinging = False


    def draw(self, surface):
        if self.swinging:
            # Negative so that we are swinging the right way. DO NOT TOUCH THIS!!!!
            total_angle = self.owner.angle - self.angle
            # print(f"Calculating weapon angle: {total_angle} = {self.owner.angle} + {self.angle}")
            rotated_image = pygame.transform.rotate(self.image, -total_angle)
            
            offset_distance = self.weapon_distance
            offset_x = math.cos(math.radians(total_angle)) * offset_distance
            offset_y = math.sin(math.radians(total_angle)) * offset_distance
            
            # Get the new rect for the rotated image
            new_rect = rotated_image.get_rect(center=(self.owner.x + offset_x, self.owner.y + offset_y))
            
            # Draw the rotated image on the screen
            surface.blit(rotated_image, new_rect.topleft)
            self.rect = new_rect

    def get_hitbox(self):
        return self.rect
    
    def get_state(self):
        """We should only need the status of the weapon if it is currently attacking.
        """
        status = {}
        if self.swinging:
            status["x"] = self.rect.x
            status["y"] = self.rect.y
            # Negative so that we are swinging the right way. DO NOT TOUCH THIS!!!!
            # WARNING: IF THIS CHANGES, UPDATE set_state
            total_angle = self.owner.angle - self.angle
            status["angle"] = total_angle

        return status
    
    def set_state(self, state):
        """Opposite of get_state. Configure current state to match provided one

        Used during replays

        Args:
            state (dict): State we want to mimic
        """
        # TODO: This
        self.swinging = True
        self.x = state["x"]
        self.y = state["y"]
        # Angle is different, we have to unpack it like we packed it in the get_state()
        # WARNING: IF THIS CHANGES, UPDATE get_state
        self.angle = state["angle"] + self.owner.angle
    
    def check_collisions(self):
        # TODO: Update this to make margit's collision box smaller. Its too fat right now.
        # if self.swinging and self.get_hitbox().colliderect(pygame.Rect(self.target.x, self.target.y, self.target.width, self.target.height)):
        if self.swinging and self.get_hitbox().colliderect(self.target.get_hitbox()):
            dmgtaken = self.target.take_damage(self.damage)
            if dmgtaken:
                if not SILENT:
                    print(f"{self.target.name} hit for {dmgtaken}! Health: {self.target.health}")
                self.damage = 0 # To prevent the enemy from taking damage twice from the same swing/ability