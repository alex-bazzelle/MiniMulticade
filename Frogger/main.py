"""
Author: Ernesto Auerbach
Date Last Modified: 26-March-2023
"""

""" ==== Import necessary modules ==== """
import pygame
from random import *
from pygame.locals import *
from time import sleep
import os

DEBUG = False
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
# path for all the assets
assetPath_images = "Assets\images"
assetPath_sounds = "Assets\sounds"

""" ==== Define classes ==== """


class MainMenu:
    def __init__(self):
        self.blank = pygame.image.load(image("menu3.jpg"))
        self.buttonPos = self.blank.get_width() / 2
        self.resume = pygame.image.load(image("resume.png"))
        self.resumePos = getCenter(self.resume, -10, (SCREEN_HEIGHT / 7.2))
        self.exit = pygame.image.load(image("exit.png"))
        self.exitPos = getCenter(self.exit, -10, (SCREEN_HEIGHT / 2.9))
        self.overlay = pygame.image.load(image("selectOverlay.png"))
        self.selected = "resume"
        self.cooldown = 0

    def update(self):
        screen.blit(self.blank, getCenter(self.blank))
        screen.blit(self.resume, self.resumePos)
        screen.blit(self.exit, self.exitPos)
        if self.selected == "resume":
            screen.blit(self.overlay, self.resumePos)
        if self.selected == "exit":
            screen.blit(self.overlay, self.exitPos)
        if DEBUG:
            print("pause update")

    def cooldownReset(self):
        self.cooldown = 100


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

    def remove_score(self, point):
        # Add points to the score and update the image to display the new score
        self.score -= point
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

    def set_point(self, point):
        # Add points to the score and update the image to display the new difficulty level
        self.difficulty = point
        self.image = self.font.render("Difficulty: " + str(self.difficulty), True, BLACK)

    def reset(self):
        # Reset the difficulty to 0
        self.difficulty = 1
        self.image = self.font.render("Difficulty: " + str(self.difficulty), True, BLACK)


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


# Class for the player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the player image and set its initial position
        self.image = pygame.image.load(image("frogger.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT
        self.velocityX = 8
        self.velocityY = 4

    def update(self):
        # Move the player based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocityX
        elif keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.velocityX
        elif keys[pygame.K_w] and self.rect.top > -5:
            self.rect.y -= self.velocityY
        elif keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.velocityY

    def stop_moving(self):
        self.velocityX = 0
        self.velocityY = 0

    def resume_moving(self, speedX, speedY):
        self.velocityX = speedX
        self.velocityY = speedY


# Class for the car sprite
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        # Load the car image and set its initial position and speed
        self.image = pygame.image.load(image("car.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def stop_moving(self):
        self.speed = 0

    def resume_moving(self, speed):
        self.speed = speed

    def update(self):
        # Move the car horizontally and wrap around when it goes offscreen
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH


""" ==== Define functions ==== """


# function to add the directory to image file names
def image(value):
    return os.path.join(assetPath_images, value)


def audio(value):
    return os.path.join(assetPath_sounds, value)


# get the center of objects. dx and dy are to change it
def getCenter(thing, dx=0, dy=0):
    return SCREEN_WIDTH / 2 - (thing.get_width() / 2) + dx, SCREEN_HEIGHT / 2 - (thing.get_height() / 2) + dy


def collide(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)


def death(lives):
    life.remove_life(1)
    if lives < 1 or lives == 0:
        global points
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
        bg = pygame.image.load(image("dead_frogger.png"))
        # Stop playing audio
        pygame.mixer.music.stop()
        # Load audio file
        pygame.mixer.music.load(audio("sound-frogger-squash.wav"))
        # Start playing audio
        pygame.mixer.music.play()
        screen.blit(bg, (((SCREEN_WIDTH // 2) // 3), 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        sleep(3)
        # Stop playing audio
        pygame.mixer.music.stop()
        # Load audio file
        pygame.mixer.music.load(audio("frogger-ringtone.mp3"))
        # Start playing audio
        pygame.mixer.music.play()
        bg = pygame.image.load(image("background.png"))
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        car_Spawn(difficulty)
        all_sprites.add(player)
    else:
        player.rect.centerx = SCREEN_WIDTH // 2
        player.rect.bottom = SCREEN_HEIGHT
        sleep(0.5)
    return lives, points


def car_Spawn(diff):
    for i in range(diff):
        x = randrange(0, SCREEN_WIDTH)
        overlapping = True
        speed = 4
        while overlapping:
            y1 = randrange(100, 250, 100)
            y2 = randrange(400, 550, 100)
            if y1 == y2:
                overlapping = True
            else:
                overlapping = False
        car1 = Car(x, y1, speed)
        car2 = Car(x, y2, -speed)
        car_sprites.add(car1)
        all_sprites.add(car1)
        car_sprites.add(car2)
        all_sprites.add(car2)


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
bg = pygame.image.load(image("background.png"))

# Create the car sprites and add them to the car_sprites group and all_sprites group
car_sprites = pygame.sprite.Group()

# Create the score sprite and add it to the all_sprites group
score = Score((SCREEN_WIDTH - (SCREEN_WIDTH - 10)), (SCREEN_HEIGHT - (SCREEN_HEIGHT - 10)))
# high_score = HighScore((SCREEN_WIDTH - 175), (SCREEN_HEIGHT - (SCREEN_HEIGHT - 10)))  # 420
all_sprites.add(score)
# all_sprites.add(high_score)

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

# Load audio file
pygame.mixer.music.load(audio("frogger-ringtone.mp3"))
# Start playing audio
pygame.mixer.music.play()

# Game loop
running = True
menu = MainMenu()
paused = False
alive = True
while running:
    # Handle events
    pygame.event.pump()
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            difficulty += 1
            difficult.set_point(difficulty)
            points += 1
            score.add_score(1)
            for car in car_sprites:
                car.kill()
            car_Spawn(difficulty)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            difficulty -= 1
            difficult.set_point(difficulty)
            points -= 1
            score.remove_score(1)
            for car in car_sprites:
                car.kill()
            car_Spawn(difficulty)

    if alive and not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and menu.cooldown < 0:
            menu.cooldownReset()
            paused = True
            # Stop playing audio
            pygame.mixer.music.stop()
            # Load audio file
            pygame.mixer.music.load(audio("frogger-music.mp3"))
            # Start playing audio
            pygame.mixer.music.play()
            if DEBUG:
                print("pause start")
        menu.cooldown -= 1

        # Update sprites
        all_sprites.update()
        for c1 in car_sprites:
            for c2 in car_sprites:
                if c1 != c2:
                    if pygame.sprite.collide_rect(c1, c2):
                        c1.kill()

        # Check for collision between player and cars
        if pygame.sprite.spritecollide(player, car_sprites, False):
            # If the player collides with a car, reset the score and the player's position, and respawn the cars
            lives -= 1
            lives, points = death(lives)

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
                player.velocityX += 2
                player.velocityY += 2
            difficult.set_point(difficulty)

            player.rect.centerx = SCREEN_WIDTH // 2
            player.rect.bottom = SCREEN_HEIGHT
            for car in car_sprites:
                car.kill()
            for car in car_sprites:
                car.speed += 1
            # Stop playing audio
            pygame.mixer.music.stop()
            # Load audio file
            pygame.mixer.music.load(audio("sound-frogger-coin-in.wav"))
            # Start playing audio
            pygame.mixer.music.play()
            sleep(0.5)
            # Stop playing audio
            pygame.mixer.music.stop()
            # Load audio file
            pygame.mixer.music.load(audio("frogger-ringtone.mp3"))
            # Start playing audio
            pygame.mixer.music.play()
            car_Spawn(difficulty)

        # Draw screen
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    elif alive and paused:
        keys = pygame.key.get_pressed()  # keys
        if keys[pygame.K_w]:  # UP KEY
            if menu.selected == "exit":
                menu.selected = "resume"
        if keys[pygame.K_s]:  # DOWN KEY
            if menu.selected == "resume":
                menu.selected = "exit"
        if keys[pygame.K_SPACE] and menu.selected == "exit":
            pygame.quit()
            exit()
        if ((keys[pygame.K_SPACE] and menu.selected == "resume") or (
                keys[pygame.K_ESCAPE]) and menu.cooldown < 0):
            if DEBUG:
                print("pause escape")
            # Stop playing audio
            pygame.mixer.music.stop()
            # Load audio file
            pygame.mixer.music.load(audio("frogger-ringtone.mp3"))
            # Start playing audio
            pygame.mixer.music.play()
            paused = False
            menu.cooldownReset()
        pygame.display.flip()
        menu.update()
        menu.cooldown -= 1

# Stop playing audio
pygame.mixer.music.stop()
# Clean up Pygame
pygame.quit()
