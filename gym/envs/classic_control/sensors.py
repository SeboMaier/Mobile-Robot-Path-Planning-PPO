import pygame
from pygame.locals import *
import math
import os
import maps



def rot_center(image, rect, angle, cx, cy):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    if angle >= 360:
        angle -= 360
    if angle <= 0:
        rot_rect.bottomleft = cx, cy
    if 0 < angle <= 90:
        rot_rect.bottomright = cx, cy
    if 90 < angle <= 180:
        rot_rect.topright = cx, cy
    if 180< angle <= 270:
        rot_rect.topleft = cx, cy
    if 270 < angle < 360:
        rot_rect.bottomleft = cx, cy
    return rot_image, rot_rect

class Sensor(pygame.sprite.Sprite):
    def __init__(self, offset_angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 700), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.offsetangle = offset_angle
        self.image_orig = self.image
        self.rect = self.image.get_rect()
        self.CENTER_X = int(pygame.display.Info().current_w / 2)
        self.CENTER_Y = int(pygame.display.Info().current_h / 2)
        self.image, self.rect = rot_center(self.image, self.rect, offset_angle, self.CENTER_X, self.CENTER_Y)
        self.mask = pygame.mask.from_surface(self.image)
        self.delta = 700
        self.rotangle = 0




    def update(self, car_angle, cx, cy):
        self.rotangle = car_angle + self.offsetangle
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.rotangle, cx, cy)














