import os, sys, pygame
from pygame.locals import *


# Load an image
def load_image(file, transparent=True):
    fullname = os.path.join('imgs', file)
    image = pygame.image.load(fullname)
    if transparent:
        image = image.convert()
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image
