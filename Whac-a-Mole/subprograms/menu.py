import pygame
from . import Game
from functions import image, getCenter
from .constants import GameConstants

DEBUG = False


class MainMenu(Game):
    def __init__(self):
        super().__init__()
        self.blank = pygame.image.load(image("menu4.png"))
        self.buttonPos = self.blank.get_width() / 2
        self.resume = pygame.image.load(image("resume.png"))
        self.resumePos = getCenter(self.resume, -10, (GameConstants.GAMEHEIGHT / 7.2))
        self.exit = pygame.image.load(image("exit.png"))
        self.exitPos = getCenter(self.exit, -10, (GameConstants.GAMEHEIGHT / 2.9))
        self.overlay = pygame.image.load(image("selectOverlay.png"))
        self.selected = "resume"
        self.cooldown = 0

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
