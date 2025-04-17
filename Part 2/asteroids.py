import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions
width, height = 600, 400
screen = pygame.display.set_mode((width, height))

# Set window title
pygame.display.set_caption("Minimal Pygame Example")

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))  # Black background

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
