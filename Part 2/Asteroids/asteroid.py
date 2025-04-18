#Extern Imports
import pygame
from enum import Enum
import random
import sys

class AsteroidSprite(Enum):
    LARGE = "Assets/Sprites/asteroidL.png"
    MEDIUM = "Assets/Sprites/asteroidM.png"
    SMALL = "Assets/Sprites/asteroidS.png"

    def __new__(cls, image_path):
        obj = object.__new__(cls)  # Create the enum member
        obj._value_ = image_path  # Store the image path
        return obj

    def __init__(self, image_path):
        self.image = None  # Initialize the image to None

    def load(self):
        """Load image from Assets/Sprites/"""
        try:
            self.image = pygame.image.load(self.value).convert_alpha()
        except pygame.error as message:
            print(f"Could not load sprite: {self.value}")
            raise SystemExit(message)

    def get_image(self):
        """Returns the loaded image"""
        return self.image

class Asteroid:
    def __init__(self, screen_width, screen_height, speedX, speedY, posX, posY, rot, rot_speed, sprite):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = (speedX, speedY)
        self.posX = posX
        self.posY = posY
        self.rot = rot
        self.rot_speed = rot_speed
        self.sprite = sprite
        self.sprite.load()
        self.sprite_image = self.sprite.get_image()
        self.rect = self.sprite_image.get_rect()
        self.rect.center = (self.posX, self.posY)

    def update(self):
        """Updates the asteroid's position, and rotates it"""
        self.posX += self.speed[0]
        self.posY += self.speed[1]
        self.rot += self.rot_speed
        self.rot %= 360

        self.rect.center = (self.posX, self.posY)

        self.rotated_image = pygame.transform.rotate(self.sprite_image, self.rot)
        self.rect = self.rotated_image.get_rect(center = self.rect.center)

        #Handle screen edge
        if self.posX > self.screen_width + self.sprite_image.get_width() * 1.5:
            self.posX = 0
        elif self.posX < -self.sprite_image.get_width() * 1.5:
            self.posX = self.screen_width

        if self.posY > self.screen_height + self.sprite_image.get_height() * 1.5:
            self.posY = 0
        elif self.posY < -self.sprite_image.get_height() * 1.5:
            self.posY = self.screen_height

        self.sprite_image = pygame.transform.rotate(self.sprite.get_image(), self.rot)
        self.rect = self.sprite_image.get_rect(center = (self.posX, self.posY))     

    def draw(self, screen):
        """Draw asteroid onto the screen"""
        screen.blit(self.sprite_image, self.rect)
    
    def destroy(self):
        """When asteroid is destroyed"""
        #Large (3 pts), split into 2-3 medium
        #Medium (2 pts), split into 2-4 small
        #Small (1 pt), destroy
        #return score (and new asteroid instances if any)

        score = 0
        new_asteroids = []

        if self.sprite == AsteroidSprite.LARGE:
            score = 3
            for _ in range(random.randint(2, 3)):
                #Create new medium asteroids
                new_speedX = random.uniform(-1.5, 1.5)
                new_speedY = random.uniform(-1.5, 1.5)
                new_asteroids.append(
                    Asteroid(
                        self.screen_width, self.screen_height,
                        new_speedX, new_speedY,
                        self.posX, self.posY,
                        random.randint(0, 360),
                        random.uniform(-2, 2),
                        AsteroidSprite.MEDIUM)
                )
        elif self.sprite == AsteroidSprite.MEDIUM:
            score = 2
            for _ in range(random.randint(2, 3)):
                #Create new medium asteroids
                new_speedX = random.uniform(-2, 2)
                new_speedY = random.uniform(-2, 2)
                new_asteroids.append(
                    Asteroid(
                        self.screen_width, self.screen_height,
                        new_speedX, new_speedY,
                        self.posX, self.posY,
                        random.randint(0, 360),
                        random.uniform(-2.5, 2.5),
                        AsteroidSprite.SMALL)
                )
        else:
            score = 1

        return score, new_asteroids

#TEST
if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Asteroid Test")

    asteroids = []
    for _ in range(5):  # Create 5 initial asteroids
        asteroids.append(
            Asteroid(
                screen_width,
                screen_height,
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.randint(0, screen_width),
                random.randint(0, screen_height),
                random.randint(0, 360),
                random.uniform(-1, 1),
                random.choice([AsteroidSprite.LARGE, AsteroidSprite.MEDIUM, AsteroidSprite.SMALL]),
            )
        )

    last_destroy_time = pygame.time.get_ticks() # Use pygame's time
    destroy_interval = 2000  # Destroy every 2 seconds (in milliseconds)

    clock = pygame.time.Clock()  # Create a clock object

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Clear the screen

        current_time = pygame.time.get_ticks()  # Use pygame's time
        if current_time - last_destroy_time >= destroy_interval:
            last_destroy_time = current_time

            # Destroy all asteroids and replace them with new ones
            new_asteroids = []
            for asteroid in asteroids:
                score, split_asteroids = asteroid.destroy()
                new_asteroids.extend(split_asteroids)  # Add all split asteroids

            asteroids = [] #Clear the old asteroids
            asteroids.extend(new_asteroids)
            if not asteroids:  # If no asteroids left, create a new large one
                asteroids.append(Asteroid(screen_width,screen_height,random.uniform(-1, 1),random.uniform(-1, 1),random.randint(0, screen_width),random.randint(0, screen_height),random.randint(0, 360),random.uniform(-1, 1),AsteroidSprite.LARGE))

            #Ensure there are always SOME asteroids in the game.  This prevents errors.
            if len(asteroids) == 0:
                asteroids.append(Asteroid(screen_width,screen_height,random.uniform(-1, 1),random.uniform(-1, 1),random.randint(0, screen_width),random.randint(0, screen_height),random.randint(0, 360),random.uniform(-1, 1),AsteroidSprite.LARGE))

        # Update and draw asteroids
        for asteroid in asteroids:
            asteroid.update()
            asteroid.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # Limit frame rate to 60 FPS.  Handles time.sleep() internally
