import pygame

def calculate_new_xy(old_xy, speed, angle_in_degrees):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return old_xy + move_vec