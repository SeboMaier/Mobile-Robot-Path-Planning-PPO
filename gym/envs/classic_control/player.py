import os, sys, pygame, math, maps
from pygame.locals import *
from random import randint
from loader import load_image



# Rotate robot.
def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

#define car as Player.
class Player(pygame.sprite.Sprite):
    def __init__(self, start_angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('an1_trans.png', False)
        self.image_1 = load_image('an2_trans.png', False)
        #self.image = pygame.transform.scale(self.image, (60, 100))
        #self.image_1 = pygame.transform.scale(self.image_1, (60, 100))
        self.rect = self.image.get_rect()
        self.rect_1 = self.image_1.get_rect()

        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        CENTER_X = int(pygame.display.Info().current_w /2)
        CENTER_Y = int(pygame.display.Info().current_h /2)
        self.x = CENTER_X
        self.y = CENTER_Y

        self.rect.topleft = (self.x - 100, self.y - 200)
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0

        self.dir = start_angle
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.speed = 10
        self.steering = 3

    def reset(self):
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.x = int(pygame.display.Info().current_w / 2)
        self.y = int(pygame.display.Info().current_h / 2)

        self.mask = pygame.mask.from_surface(self.image)

    def steerright(self):
        #steerright is negative self.steering
        self.dir = self.dir-self.steering
        if self.dir < 0:
            self.dir = 360
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.mask = pygame.mask.from_surface(self.image)

    def steerleft(self):
        #steerright is negative self.steering
        self.dir = self.dir+self.steering
        if self.dir > 360:
            self.dir = 0
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))

    def animation(self, animation_count):
        if animation_count < 7:
            self.image = self.image_orig
            self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        else:
            self.image = self.image_1
            self.image, self.rect = rot_center(self.image_1, self.rect, self.dir)








