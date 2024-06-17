import pygame
import sys

WIDTH, HEIGHT = 1000, 1000
pygame.display.set_caption("2D Game")

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic here

        # Drawing code here
        screen.fill((0, 0, 0))  # Clear the screen with black

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()