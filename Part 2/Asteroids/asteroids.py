#Extern Imports
import pygame
import sys
import random

#Internal Imports
from ship import Ship
from asteroid import Asteroid, AsteroidSprite

#Constants
width, height = 800, 600

#Set Up Pygame Environment
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroids")

#Global State
score = 0
asteroids = []
ship = Ship(width, height)

def main():
    clock = pygame.time.Clock()
    while True:
        #Asteroid Creation
        if len(asteroids) <= 3:
            asteroids.append(
                Asteroid(
                    width,
                    height,
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    random.choice([random.randint(0, int(width * 0.1)), random.randint(int(width * 0.9), width)]),
                    random.choice([random.randint(0, int(height * 0.1)), random.randint(int(height * 0.9), height)]),
                    random.randint(0, 360),
                    random.uniform(-1, 1),
                    random.choice([AsteroidSprite.LARGE, AsteroidSprite.MEDIUM, AsteroidSprite.SMALL]
                )
            )
        )
        
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

        #Update positions
        ship.update(keys)
        for asteroid in asteroids:
            asteroid.update()

        #Ship Firing
        ship_posX, ship_posY, ship_col_radius = ship.position_and_col_radius()
        ship_rot = ship.rotation()

        #Check for Asteroid-Pellet Collision

        #Check for Asteroid-Ship Collisions
        ship_posX, ship_posY, ship_col_radius = ship.position_and_col_radius()
        for asteroid in asteroids:
            asteroid_posX, asteroid_posY, asteroid_col_radius = asteroid.position_and_col_radius()

            dx = ship_posX - asteroid_posX
            dy = ship_posY - asteroid_posY

            dist_squared = dx*dx + dy*dy

            radii_sum = ship_col_radius + asteroid_col_radius

            radii_sum_squared = radii_sum * radii_sum

            #Game Over
            if dist_squared < radii_sum_squared:
                print("GAME OVER!!!")
                pygame.quit()
                sys.exit()

        #Drawing
        screen.fill((0, 0, 0)) #Black Background
        ship.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()
