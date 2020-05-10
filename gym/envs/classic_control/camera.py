import pygame

class Camera():
    def __init__(self):
        self.CENTER_X = int(pygame.display.Info().current_w / 2)
        self.CENTER_Y = int(pygame.display.Info().current_h / 2)
        self.x = 0
        self.y = 0

    def set_pos(self, x, y):
        self.x = x - self.CENTER_X
        self.y = y - self.CENTER_Y

