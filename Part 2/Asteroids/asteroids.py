#Extern Imports
import pygame
import sys
import random

#Internal Imports
from ship import Ship
from asteroid import Asteroid, AsteroidSprite
from pellet import Pellet

#Constants
width, height = 800, 600
firing_cooldown = 45

#Set Up Pygame Environment
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroids")

def main():
    #Global State
    score = 0
    asteroids = []
    ship = Ship(width, height)
    pellets = []
    time_since_last_firing = firing_cooldown
    
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
        for pellet in pellets:
            pellet.update()

        #Ship Firing
        ship_posX, ship_posY, ship_col_radius = ship.position_and_col_radius()
        ship_rot = ship.rotation()
        if time_since_last_firing >= firing_cooldown:
            pellets = pellets[1:]
            if keys[pygame.K_SPACE]:
                pellets.append(
                    Pellet(width, height, ship_posX, ship_posY, ship_rot)
                )
                time_since_last_firing = 0
            

        #Check for Collisions
        ship_posX, ship_posY, ship_col_radius = ship.position_and_col_radius()
        for asteroid in asteroids:
            asteroid_posX, asteroid_posY, asteroid_col_radius = asteroid.position_and_col_radius()

            #SHIP
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

            #PELLET
            for pellet in pellets:
                pellet_posX, pellet_posY = pellet.position()
                dx = pellet_posX - asteroid_posX
                dy = pellet_posY - asteroid_posY
                dist_squared = dx*dx + dy*dy
                radii_squared = asteroid_col_radius * asteroid_col_radius

                if dist_squared < radii_squared:
                    pellets.pop(pellets.index(pellet))
                    to_score, asteroids_to_add = asteroid.destroy()
                    asteroids.pop(asteroids.index(asteroid))
                    asteroids += asteroids_to_add
                    score += to_score
                    break
                

        #Drawing
        screen.fill((0, 0, 0)) #Black Background
        ship.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        for pellet in pellets:
            pellet.draw(screen)
        
        pygame.display.flip()

        time_since_last_firing += 1
        
        clock.tick(60)

if __name__ == "__main__":
    main()
