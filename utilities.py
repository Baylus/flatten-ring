import pygame
import pygame.font

# Initialize Pygame and the font module
pygame.init()
pygame.font.init()

# Define a function to draw text
def draw_text(surface, text, x, y, font_size=20, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def calculate_new_xy(old_xy, speed, angle_in_degrees):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return old_xy + move_vec

def draw_health_bar(surface, x, y, width, height, current_health = 5, max_health = 10, name = ""):
    # Calculate the health ratio
    health_ratio = current_health / max_health
    
    # Define the colors
    border_color = (255, 255, 255)  # White
    health_color = (0, 255, 0)  # Green
    background_color = (255, 0, 0)  # Red
    
    # Draw the background (full bar)
    pygame.draw.rect(surface, background_color, (x, y, width, height))
    
    # Draw the current health bar
    pygame.draw.rect(surface, health_color, (x, y, width * health_ratio, height))
    
    # Draw the border
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2)

    # Draw the name below the health bar
    draw_text(surface, name, x + width // 2, y + height + 5, font_size=20, color=(255, 255, 255))