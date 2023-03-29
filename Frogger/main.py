"""
Author: Ernesto Auerbach
Date Last Modified: 26-March-2023
"""

""" ==== Import necessary modules ==== """
import pygame
from random import *
from pygame.locals import *
from time import sleep

""" ==== Define constants ==== """
SCREEN_WIDTH = 879
SCREEN_HEIGHT = 600
FPS = 300

""" ==== Define colors ==== """
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

""" ==== Define classes ==== """
# Class for the player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the player image and set its initial position
        self.image = pygame.image.load("Assets/frogger.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        # Move the player based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
        elif keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 10
        elif keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 8
        elif keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += 8

# Class for the car sprite
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        # Load the car image and set its initial position and speed
        self.image = pygame.image.load("Assets/car.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        # Move the car horizontally and wrap around when it goes offscreen
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

# Class for the score sprite
class Score(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Set the initial score and font for displaying it
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render("Score: " + str(self.score), True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def add_score(self, points):
        # Add points to the score and update the image to display the new score
        self.score += points
        self.image = self.font.render("Score: " + str(self.score), True, BLACK)

    def reset(self):
        # Reset the score to 0 and remove all car sprites
        self.score = 0
        self.image = self.font.render("Score: " + str(self.score), True, BLACK)
        for car in car_sprites:
            car.kill()
            all_sprites.remove(car)

# Class for the end line sprite
class EndLine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a black line across the screen to represent the end line
        self.image = pygame.Surface((SCREEN_WIDTH, 1))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 50

""" ==== Main Program ==== """
# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the game window
pygame.display.set_caption("Frogger")

# Create a clock to control the frame rate of the game
clock = pygame.time.Clock()

# Create the player sprite and add it to the all_sprites group
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Load the background image and add it to the all_sprites group
bg = pygame.image.load("Assets/background.png")
all_sprites.add(player)

# Create the car sprites and add them to the car_sprites group and all_sprites group
car_sprites = pygame.sprite.Group()

def car_Spawn(difficulty):
    for i in range(difficulty):
        x = randrange(0, SCREEN_WIDTH)
        y1 = randrange(100, 250, 50)
        y2 = randrange(400, 550, 50)
        speed1 = randrange(1, 5)
        speed2 = randrange(-5, -1)
        car1 = Car(x, y1, speed1)
        car2 = Car(x, y2, speed2)
        car_sprites.add(car1)
        all_sprites.add(car1)
        car_sprites.add(car2)
        all_sprites.add(car2)

# Create the score sprite and add it to the all_sprites group
score = Score(10, 10)
all_sprites.add(score)

# Create the end line sprite and add it to the all_sprites group
end_line = EndLine()
all_sprites.add(end_line)

# Spawn the initial set of cars with difficulty level 1
difficulty = 1
car_Spawn(difficulty)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # Update sprites
    all_sprites.update()

    # Check for collision between player and cars
    if pygame.sprite.spritecollide(player, car_sprites, False):
        # If the player collides with a car, reset the score and the player's position, and respawn the cars
        score.reset()
        player.rect.centerx = SCREEN_WIDTH // 2
        player.rect.bottom = SCREEN_HEIGHT
        difficulty = 1
        sleep(0.5)
        car_Spawn(difficulty)

    # Check if player reached end line
    if pygame.sprite.collide_rect(player, end_line):
        # If the player reaches the end line, increase the score, increase the difficulty level, speed up the cars, reset the player's position, and respawn the cars
        score.add_score(1)
        difficulty += 1
        player.rect.centerx = SCREEN_WIDTH // 2
        player.rect.bottom = SCREEN_HEIGHT
        for car in car_sprites:
            car.speed += 1
        sleep(0.5)
        car_Spawn(difficulty)

    # Draw screen
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Clean up Pygame
pygame.quit()