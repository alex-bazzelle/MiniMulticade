import os
import pygame

from .constants import Constants, GameConstants
from .variables import assetPath_images, assetPath_sounds

DEBUG = False

def cooldownReset(cooldown):
    cooldown = 15

    
def main_menu(screen, selected="resume", cooldown=0):
    blank = pygame.image.load(image("menu4.png"))
    buttonPos = blank.get_width() / 2
    resume = pygame.image.load(image("resume.png"))
    resumePos = getCenter(resume, -10, (GameConstants.GAMEHEIGHT / 7.2))
    exit = pygame.image.load(image("exit.png"))
    exitPos = getCenter(exit, -10, (GameConstants.GAMEHEIGHT / 2.9))
    overlay = pygame.image.load(image("selectOverlay.png"))

    screen.blit(blank, getCenter(blank))
    screen.blit(resume, resumePos)
    screen.blit(exit, exitPos)

    if selected == "resume":
        screen.blit(overlay, resumePos)
    elif selected == "exit":
        screen.blit(overlay, exitPos)

    if DEBUG:
        print("pause update")

    cooldownReset(cooldown)


# get the center of objects. dx and dy are to change it
def getCenter(thing, dx=0, dy=0):
    return Constants.GAMEWIDTH / 2 - (thing.get_width() / 2) + dx, Constants.GAMEHEIGHT / 2 - (thing.get_height() / 2) \
           + dy


# function to add the directory to image file names
def image(value):
    return os.path.join(assetPath_images, value)


def audio(value):
    return os.path.join(assetPath_sounds, value)
