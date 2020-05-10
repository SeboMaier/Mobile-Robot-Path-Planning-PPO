import pygame
import os
from loader import load_image


class Path(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bg_empty.png")
        self.image = pygame.transform.scale(self.image, (3945, 1628))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.x = 0
        self.y = 0

        # Realign the map
    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y

    def reset(self):
        self.image = load_image("bg_empty.png")
        self.image = pygame.transform.scale(self.image, (3945, 1628))
