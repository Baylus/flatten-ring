import pygame
import math

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
        self.target = target
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

    def update(self):
        if self.swinging:
            self.check_collisions()
            self.angle += self.angle_speed  # Adjust the angle increment as needed
            if not self.reversed and self.angle >= self.end_angle_offset:
                print(f"We have ended our swing. current angle {self.angle}, end angle {self.end_angle_offset}")
                self.swinging = False
            elif self.reversed and self.angle <= self.end_angle_offset:
                print(f"We have ended our reversed swing. current angle {self.angle}, end angle {self.end_angle_offset}")
                self.swinging = False


    def draw(self, surface):
        if self.swinging:
            # Calculate the rotation angle based on the owner's angle and weapon's swing angle
            total_angle = self.owner.angle + self.angle
            print(f"Calculating weapon angle: {total_angle} = {self.owner.angle} + {self.angle}")
            rotated_image = pygame.transform.rotate(self.image, total_angle)
            
            # Calculate the offset for the weapon's position
            offset_distance = self.weapon_distance  # Distance from the player's center to the weapon, adjust as needed
            offset_x = math.cos(math.radians(total_angle)) * offset_distance
            offset_y = -math.sin(math.radians(total_angle)) * offset_distance
            
            # Get the new rect for the rotated image
            new_rect = rotated_image.get_rect(center=(self.owner.x + offset_x, self.owner.y + offset_y))
            
            # Draw the rotated image on the screen
            surface.blit(rotated_image, new_rect.topleft)
            self.rect = new_rect

    def get_hitbox(self):
        return self.rect
    
    def check_collisions(self):
        # TODO: Update this to make margit's collision box smaller. Its too fat right now.
        if self.swinging and self.get_hitbox().colliderect(pygame.Rect(self.target.x, self.target.y, self.target.width, self.target.height)):
            self.target.health -= self.damage
            print(f"{self.target.name} hit! Health: {self.target.health}")
            self.damage = 0 # To prevent the enemy from taking damage twice from the same swing/ability