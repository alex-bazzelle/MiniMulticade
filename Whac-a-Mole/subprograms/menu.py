import pygame
from . import Game
from functions import image, getCenter
from .constants import GameConstants

DEBUG = False


class MainMenu():
    blank = pygame.image.load(image("menu4.png"))
    buttonPos = self.blank.get_width() / 2
    resume = pygame.image.load(image("resume.png"))
    resumePos = getCenter(self.resume, -10, (GameConstants.GAMEHEIGHT / 7.2))
    exit = pygame.image.load(image("exit.png"))
    exitPos = getCenter(self.exit, -10, (GameConstants.GAMEHEIGHT / 2.9))
    overlay = pygame.image.load(image("selectOverlay.png"))
    selected = "resume"
    cooldown = 0

    def update(self):
        self.screen.blit(self.blank, getCenter(self.blank))
        self.screen.blit(self.resume, self.resumePos)
        self.screen.blit(self.exit, self.exitPos)
        if self.selected == "resume":
            self.screen.blit(self.overlay, self.resumePos)
        if self.selected == "exit":
            self.screen.blit(self.overlay, self.exitPos)
        if DEBUG:
            print("pause update")

    def cooldownReset(self):
        self.cooldown = 15


menu = MainMenu()
