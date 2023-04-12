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

""" ==== Define variables ==== """
lives = 3
points = 0
difficulty = 1


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
        self.velocityX = 8
        self.velocityY = 4

    def update(self):
        # Move the player based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocityX
        elif keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.velocityX
        elif keys[pygame.K_UP] and self.rect.top > -5:
            self.rect.y -= self.velocityY
        elif keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.velocityY


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

    def add_score(self, point):
        # Add points to the score and update the image to display the new score
        self.score += point
        self.image = self.font.render("Score: " + str(self.score), True, BLACK)

    def reset(self):
        # Reset the score to 0 and remove all car sprites
        self.score = 0
        self.image = self.font.render("Score: " + str(self.score), True, BLACK)
        for c in car_sprites:
            c.kill()
            all_sprites.remove(c)


class HighScore(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.image = self.font.render("HighScore WIP" + str(self.score), True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Difficulty(pygame.sprite.Sprite):
    def __init__(self, x, y, z):
        super().__init__()
        # Set the initial score and font for displaying it
        self.difficulty = z
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render("Difficulty: " + str(self.difficulty), True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def add_point(self, point):
        # Add points to the score and update the image to display the new difficulty level
        self.difficulty = point
        self.image = self.font.render("Difficulty: " + str(self.difficulty), True, BLACK)

    def reset(self):
        # Reset the difficulty to 0
        self.difficulty = 1
        self.image = self.font.render("Difficulty: " + str(self.difficulty), True, BLACK)


class Lives(pygame.sprite.Sprite):
    def __init__(self, x, y, z=lives):
        super().__init__()
        # Set the initial score and font for displaying it
        self.lives = z
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render("Lives: " + str(self.lives), True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def remove_life(self, point):
        # Remove points to the lives and update the image to display the new amount of lives
        self.lives -= point
        self.image = self.font.render("Lives: " + str(self.lives), True, BLACK)

    def reset(self):
        # Reset the lives counter to 3
        self.lives = 3
        self.image = self.font.render("Lives: " + str(self.lives), True, BLACK)


# Class for the end line sprite
class EndLine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a black line across the screen to represent the end line
        self.image = pygame.Surface((SCREEN_WIDTH, 1))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -1


""" ==== Define functions ==== """


def death(lives):
    life.remove_life(1)
    if lives < 1 or lives == 0:
        score.reset()
        difficult.reset()
        player.rect.centerx = SCREEN_WIDTH // 2
        player.rect.bottom = SCREEN_HEIGHT
        player.velocityX = 8
        player.velocityY = 4
        difficulty = 1
        Difficulty.difficulty = difficulty
        points = 0
        sleep(0.5)
        lives = 3
        life.reset()
        player.kill()
        bg = pygame.image.load("Assets/dead_frogger.png")
        screen.blit(bg, (((SCREEN_WIDTH // 2) // 3), 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        sleep(3)
        bg = pygame.image.load("Assets/background.png")
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        car_Spawn(difficulty)
        all_sprites.add(player)
    else:
        player.rect.centerx = SCREEN_WIDTH // 2
        player.rect.bottom = SCREEN_HEIGHT
        sleep(0.5)
    return lives


""" ==== Main Program ==== """
# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)

# Set the title of the game window
pygame.display.set_caption("Frogger")

# Create a clock to control the frame rate of the game
clock = pygame.time.Clock()

# Create the player sprite and add it to the all_sprites group
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Load the background image
bg = pygame.image.load("Assets/background.png")

# Create the car sprites and add them to the car_sprites group and all_sprites group
car_sprites = pygame.sprite.Group()


def car_Spawn(diff):
    for i in range(diff):
        x = randrange(0, SCREEN_WIDTH)
        y1 = randrange(100, 250, 50)
        y2 = randrange(400, 550, 50)
        speed = randrange(1, 5)
        car1 = Car(x, y1, speed)
        car2 = Car(x, y2, -speed)
        car_sprites.add(car1)
        all_sprites.add(car1)
        car_sprites.add(car2)
        all_sprites.add(car2)


# Create the score sprite and add it to the all_sprites group
score = Score((SCREEN_WIDTH - (SCREEN_WIDTH - 10)), (SCREEN_HEIGHT - (SCREEN_HEIGHT - 10)))
high_score = HighScore((SCREEN_WIDTH - 175), (SCREEN_HEIGHT - (SCREEN_HEIGHT - 10)))  # 420
all_sprites.add(score)
all_sprites.add(high_score)

# Create the end line sprite and add it to the all_sprites group
end_line = EndLine()
all_sprites.add(end_line)

# Create the difficulty sprite and add it to the all_sprites group
difficult = Difficulty(SCREEN_WIDTH - 180, (SCREEN_HEIGHT - 27), difficulty)
all_sprites.add(difficult)

# Create the lives sprite and add it to the all_sprites group
life = Lives((SCREEN_WIDTH - (SCREEN_WIDTH - 10)), SCREEN_HEIGHT - 25)
all_sprites.add(life)

# Spawn the initial set of cars with difficulty level 1
car_Spawn(difficulty)


# Game loop
running = True
while running:
    # Handle events
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # Update sprites
    all_sprites.update()

    # Check for collision between player and cars
    if pygame.sprite.spritecollide(player, car_sprites, False):
        # If the player collides with a car, reset the score and the player's position, and respawn the cars
        lives -= 1
        lives = death(lives)

    # Check if player reached end line
    if pygame.sprite.collide_rect(player, end_line):
        # If the player reaches the end line, increase the score, increase the difficulty level, speed up the cars,
        # reset the player's position, and respawn the cars
        score.add_score(1)
        points += 1

        # adjusts for difficulty level
        if points == 0:
            difficulty = 1
        elif 1 <= points <= 2:
            difficulty = 2
        elif 3 <= points <= 5:
            difficulty = 3
            player.velocityX = 9
            player.velocityY = 4.5
        elif 6 <= points <= 9:
            difficulty = 4
            player.velocityX = 10
            player.velocityY = 5
        elif 10 <= points <= 13:
            difficulty = 5
            player.velocityX = 11
            player.velocityY = 5.5
        elif 14 <= points <= 16:
            difficulty = 6
            player.velocityX = 12
            player.velocityY = 6
        else:
            difficulty += 1
            player.velocityX += 1
            player.velocityY += 1
        difficult.add_point(difficulty)

        player.rect.centerx = SCREEN_WIDTH // 2
        player.rect.bottom = SCREEN_HEIGHT
        for car in car_sprites:
            car.kill()
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
