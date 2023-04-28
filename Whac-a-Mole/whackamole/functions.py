import os

from .constants import Constants
from .variables import assetPath_images, assetPath_sounds

""" function to add the directory to image file names"""


# get the center of objects. dx and dy are to change it
def getCenter(thing, dx=0, dy=0):
    return Constants.GAMEWIDTH / 2 - (thing.get_width() / 2) + dx, Constants.GAMEHEIGHT / 2 - (thing.get_height() / 2) \
           + dy


# function to add the directory to image file names
def image(value):
    return os.path.join(assetPath_images, value)


def audio(value):
    return os.path.join(assetPath_sounds, value)
