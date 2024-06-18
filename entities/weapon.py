import pygame
import math

class Weapon:
    def __init__(self, owner):
        self.owner = owner
        self.angle = 0
        self.swinging = False
        self.image = pygame.image.load("assets/tarnished_right_slash.png")  # Load your weapon image
        self.rect = self.image.get_rect()

    def start_attack(self):
        self.swinging = True
        self.angle = 0  # Reset angle at the start of the attack

    def update(self):
        if self.swinging:
            self.angle += 10  # Adjust the angle increment as needed
            if self.angle >= 180:
                self.swinging = False

    def draw(self, surface):
        if self.swinging:
            rotated_image = pygame.transform.rotate(self.image, -self.owner.angle + self.angle)
            offset_x = math.cos(math.radians(self.owner.angle - self.angle)) * 50  # Adjust the offset
            offset_y = -math.sin(math.radians(self.owner.angle - self.angle)) * 50  # Adjust the offset
            new_rect = rotated_image.get_rect(center=(self.owner.x + offset_x, self.owner.y + offset_y))
            surface.blit(rotated_image, new_rect.topleft)
            self.rect = new_rect

    def get_hitbox(self):
        return self.rect