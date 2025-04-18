#Extern Imports
import pygame
from enum import Enum
import math
import sys

class ShipSprite(Enum):
    SHIP = "Assets/Sprites/ship.png" #No thrust of any king
    SHIP_CCW = "Assets/Sprites/shipCCW.png" #Rotating Counter-Clockwise
    SHIP_CW = "Assets/Sprites/shipCW.png" #Rotating Clockwise
    SHIP_T = "Assets/Sprites/shipT.png" #Thrusting
    SHIP_TCCW = "Assets/Sprites/shipTCCW.png" #Thrusting and Rotating Counter-Clockwise
    SHIP_TCW = "Assets/Sprites/shipTCW.png" #Thrusting and Rotating Clockwise
    
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

class Ship:
    def __init__(self, screen_width, screen_height):
        
        #Constants
        self.rot_speed = 4 #Degrees per update
        self.acceleration = 0.1
        self.max_speed = 5
        self.friction = 0.99
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.col_radius = 14.5

        #Variables
        self.sprite = ShipSprite.SHIP
        self.sprite.load()        
        self.sprite_image = self.sprite.get_image()
        self.posX = screen_width // 2
        self.posY = screen_height // 2
        self.rect = self.sprite_image.get_rect()
        self.rect.center = (self.posX, self.posY)
        self.momX = 0
        self.momY = 0
        self.rot = 90

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.sprite.load()
        self.sprite_image = self.sprite.get_image()
        self.rect = self.sprite_image.get_rect(center=self.rect.center)

    def rotate(self, clockwise: bool):
        """Rotates the ship"""
        if clockwise:
            self.rot -= self.rot_speed
        else:
            self.rot += self.rot_speed

    def accelerate(self):
        """Applies thrust to the ship"""
        rad = math.radians(self.rot)
        
        self.momX += self.acceleration * math.cos(rad)
        self.momY -= self.acceleration * math.sin(rad)

        speed = math.sqrt(self.momX**2 + self.momY**2)
        if speed > self.max_speed:
            scaleFactor = self.max_speed/speed
            self.momX *= scaleFactor
            self.momY *= scaleFactor

    def update(self, keys):
        """Updates the ship's position, applies friction, and rotates the sprite."""
        #Apply Friction
        self.momX *= self.friction
        self.momY *= self.friction

        # Update position
        self.posX += self.momX
        self.posY += self.momY
        self.rect.center = (self.posX, self.posY)

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.set_sprite(ShipSprite.SHIP_TCCW)
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.set_sprite(ShipSprite.SHIP_TCW)
        elif (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.set_sprite(ShipSprite.SHIP_T)
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.set_sprite(ShipSprite.SHIP_CCW)
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.set_sprite(ShipSprite.SHIP_CW)
        else:
            self.set_sprite(ShipSprite.SHIP)

        #Handle Screen Edges
        if self.posX > self.screen_width + self.sprite_image.get_width():
            self.posX = 0
        elif self.posX < -self.sprite_image.get_width():
            self.posX = self.screen_width

        if self.posY > self.screen_height + self.sprite_image.get_width():
            self.posY = 0
        elif self.posY < -self.sprite_image.get_width():
            self.posY = self.screen_height

        self.sprite_image = pygame.transform.rotate(self.sprite.get_image(), self.rot)
        self.rect = self.sprite_image.get_rect(center=self.rect.center)

    def draw(self, screen):
        """Draw ship onto the screen"""
        screen.blit(self.sprite_image, self.rect)

    def position_and_col_radius(self):
        """Returns ship position and collision radius"""
        return self.posX, self.posY, self.col_radius

    def rotation(self):
        """Returns the rotation of the ship"""
        return self.rot

#TEST   
if __name__ == "__main__":
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ship Test")

    ship = Ship(screen_width, screen_height)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship.rotate(False)  # Rotate counter-clockwise
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship.rotate(True)   # Rotate clockwise
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ship.accelerate()   # Accelerate forward

        ship.update(keys)

        screen.fill((0, 0, 0))  # Black background
        ship.draw(screen)

        pygame.display.flip()

        clock.tick(60)
