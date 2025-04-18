#Extern Imports
import pygame
import math

class Pellet:
    def __init__(self, screen_width, screen_height, posX, posY, rot):
        #Constants
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 12
        self.rot = rot
        self.rad = math.radians(self.rot)
        self.velX = self.speed * math.cos(self.rad)
        self.velY = -self.speed * math.sin(self.rad)

        try:
            self.sprite = pygame.image.load("Assets/Sprites/pellet.png").convert_alpha()
        except pygame.error as message:
            print("Could not load sprite: Assets/Sprites/pellet.png")
            raise SystemExit(message)

        #Variables
        self.posX = posX
        self.posY = posY
        self.sprite_image = self.sprite
        self.rect = self.sprite_image.get_rect()
        self.rect.center = (self.posX, self.posY)

    def update(self):
        """Updates the pellet's position"""
        self.posX += self.velX
        self.posY += self.velY
        self.rect.center = (self.posX, self.posY)

        if self.posX > self.screen_width + self.sprite_image.get_width():
            self.posX = 0
        elif self.posX < -self.sprite_image.get_width():
            self.posX = self.screen_width

        if self.posY > self.screen_height + self.sprite_image.get_width():
            self.posY = 0
        elif self.posY < -self.sprite_image.get_width():
            self.posY = self.screen_height

        self.sprite_image = pygame.transform.rotate(self.sprite, self.rot)
        self.rect = self.sprite_image.get_rect(center=self.rect.center)

    def draw(self, screen):
        """Draw pellet onto the screen"""
        screen.blit(self.sprite_image, self.rect)

    def position(self):
        """Returns the positon of pellet"""
        return (self.posX, self.posY)
        
