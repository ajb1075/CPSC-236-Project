#Extern Imports
import pygame
import sys

#Internal Imports
from ship import Ship

#Constants
width, height = 800, 600

#Set Up Pygame Environment
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroids")

#Global State
score = 0
ship = Ship(width, height)

def main():
    clock = pygame.time.Clock()
    while True:
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship.rotate(False)  # Rotate counter-clockwise
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship.rotate(True)   # Rotate clockwise
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ship.accelerate()   # Accelerate forward
        ship.update(keys)
        ship.handle_screen_edge_collision(width, height)

        #Drawing
        screen.fill((0, 0, 0)) #Black Background
        ship.draw(screen)
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()
