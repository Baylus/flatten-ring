import pygame
import math

from .weapon import Weapon

class Slash(Weapon):
    """Margits regular slash attack. This will require coordination on the part of Margit
    so that the attack has some telegraphing time before it starts to actually swing.
    """
    def __init__(self, owner, target, image_url = "assets/margit_weapon.png", reversed = False):
        self.owner = owner
        self.angle = 0
        self.swinging = False
        self.image = pygame.image.load(image_url)  # Load your weapon image
        self.rect = self.image.get_rect()
        self.target = target
        self.damage = 5

    # def start_attack(self):
    #     self.swinging = True
    #     self.angle = -90  # Reset angle at the start of the attack

    def update(self):
        if self.swinging:
            self.check_collisions()
            self.angle += 15  # Adjust the angle increment as needed
            if self.angle >= 100:
                self.swinging = False
                # self.angle = 0

    def draw(self, surface):
        if self.swinging:
            # Calculate the rotation angle based on the owner's angle and weapon's swing angle
            total_angle = self.owner.angle + self.angle
            rotated_image = pygame.transform.rotate(self.image, -total_angle)
            
            # Calculate the offset for the weapon's position
            offset_distance = 60  # Distance from the player's center to the weapon, adjust as needed
            offset_x = math.cos(math.radians(total_angle)) * offset_distance
            offset_y = -math.sin(math.radians(total_angle)) * offset_distance
            
            # Get the new rect for the rotated image
            new_rect = rotated_image.get_rect(center=(self.owner.x + offset_x, self.owner.y + offset_y))
            
            # Draw the rotated image on the screen
            surface.blit(rotated_image, new_rect.topleft)
            self.rect = new_rect
    
    def check_collisions(self):
        if self.swinging and self.get_hitbox().colliderect(pygame.Rect(self.target.x, self.target.y, self.target.width, self.target.height)):
            self.target.health -= self.damage
            print(f"{self.target.name} hit! Health: {self.target.health}")
            self.damage = 0