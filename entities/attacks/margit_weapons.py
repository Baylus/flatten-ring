import pygame
import math

from utilities import calculate_new_xy
from ..exceptions import CharacterDied, TarnishedDied

from .weapon import Weapon

class Slash(Weapon):
    """Margits regular slash attack. This will require coordination on the part of Margit
    so that the attack has some telegraphing time before it starts to actually swing.
    """
    def __init__(self, owner, target, image_url = "assets/margit_weapon.png", reversed = False, attack_duration = 10):
        super().__init__(owner, target, image_url, reversed=reversed, attack_duration=attack_duration)

        self.weapon_distance = 120
    
    def check_collisions(self):
        try:
            super().check_collisions()
        except CharacterDied:
            raise TarnishedDied("Tarnished Died by slash.")

class Dagger(Weapon):
    def __init__(self, owner, target, x, y, angle, speed, damage = 5, duration = 10):
        self.owner = owner
        self.target = target
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.time_left = duration
        self.damage = damage
        self.swinging = True # Used to check for collisions. Anytime a dagger exists, it must be active
        self.image = pygame.image.load("assets/margit_dagger.png")
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.time_left -= 1
        self.x, self.y = calculate_new_xy((self.x, self.y), self.speed, self.angle)

        # Update the rect position
        self.rect.center = (self.x, self.y)

        self.check_collisions()

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        surface.blit(rotated_image, self.rect.topleft)

    def check_collisions(self):
        try:
            super().check_collisions()
        except CharacterDied:
            raise TarnishedDied("Tarnished Died by Daggers.")