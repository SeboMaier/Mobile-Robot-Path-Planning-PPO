import pygame
import maps
from pygame.locals import *
import math
import numpy as np

import player
import camera
import roborange
import holes
import path
import sensors
import gym
from gym import spaces

PATH = True


class Simulation(gym.Env):
    def __init__(self):
        metadata = {'render.modes': ['human']}
        pygame.init()

        self.action_space = spaces.Discrete(5)
        low = np.array([0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        high = np.array([4000, 4000, 360,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000])

        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.score = 0
        self.stepscore = 0
        self.stepcount = 0
        self.holescore = 12

        self.map_s = pygame.sprite.Group()
        self.player_s = pygame.sprite.Group()
        self.path_s = pygame.sprite.Group()
        self.hole_s = pygame.sprite.Group()
        self.range_s = pygame.sprite.Group()

        self.animation_count = 0

        self.screen = pygame.display.set_mode((1800, 1000))


        self.clock = pygame.time.Clock()
        self.CENTER_X = int(pygame.display.Info().current_w / 2)
        self.CENTER_Y = int(pygame.display.Info().current_h / 2)
        self.running = True
        self.car = player.Player()
        self.cam = camera.Camera()
        self.robrange = roborange.RoRange()
        self.current_map = maps.Map()
        self.path = path.Path()

        # create new holes
        for r in range(100):
            hole = holes.Holes()
            hole.add(self.hole_s)

        # create list of hole coordinates and IR´s
        self.holestate = []
        for hole in self.hole_s:
            self.holestate.append(hole.x)
            self.holestate.append(hole.y)

        # create observation state array
        self.state = np.array([self.car.x, self.car.y, self.car.dir])
        holearray = np.array(self.holestate)
        self.state = np.append(self.state, holearray)

        self.map_s.add(self.current_map)
        self.player_s.add(self.car)
        self.range_s.add(self.robrange)
        self.path_s.add(self.path)

        pygame.display.set_caption('RoboSimAI')
        pygame.mouse.set_visible(True)
        self.font = pygame.font.Font(None, 24)

        self.background = pygame.Surface(self.screen.get_size())

        self.background.fill((210, 210, 250))

    def step(self, action):
        # 0 scan; 1 up; 2 down; 3 left; 4 right
        self.stepscore = 0
        self.stepcount += 1
        self.holestate.clear()

        for hole in self.hole_s.sprites():
            self.holestate.append(hole.x)
            self.holestate.append(hole.y)

        len_holelist = len(self.holestate)
        append_length = 200 - len_holelist

        if action == 0:
            spritelist = self.check_collision(self.robrange, self.hole_s, True)
            self.stepscore += len(spritelist)*self.holescore
            self.stepscore -= 0.02

        if action == 1:
            self.car.animation(self.animation_count)
            if self.animation_count > 14:
                self.animation_count = 0
            self.animation_count += 1
            self.car.speed = 10
            self.robrange.speed = 10
            self.robrange.update()
            self.car.update()
            self.stepscore -= 0.02

        if action == 2:
            self.car.animation(self.animation_count)
            if self.animation_count > 14:
                self.animation_count = 0
            self.animation_count += 1
            self.car.speed = -10
            self.robrange.speed = -10
            self.robrange.update()
            self.car.update()
            self.stepscore -= 0.021


        if action == 3:
            self.car.steerleft()
            self.robrange.steerleft()
            self.car.animation(self.animation_count)
            if self.animation_count > 14:
                self.animation_count = 0
            self.animation_count += 1
            self.stepscore -= 0.02

        if action == 4:
            self.car.steerright()
            self.robrange.steerright()
            self.car.animation(self.animation_count)
            if self.animation_count > 14:
                self.animation_count = 0
            self.animation_count += 1
            self.stepscore -= 0.02

        self.score += self.stepscore
        self.path_s.update(self.cam.x, self.cam.y)
        self.hole_s.update(self.cam.x, self.cam.y)
        #self.range_s.update(self.cam.x, self.cam.y)
        self.map_s.update(self.cam.x, self.cam.y)
        #self.player_s.update(self.cam.x, self.cam.y)

        done = 0
        if self.score < -200:
            done = 1
        if self.stepcount > 2500:
            done = 1
        if not self.hole_s.sprites():
            done = 1
        self.cam.set_pos(self.car.x, self.car.y)

        if append_length == 0:
            self.state = np.array([self.car.x, self.car.y, self.car.dir])
            holearray = np.array(self.holestate)
            self.state = np.append(self.state, holearray)
        else:
            listofzeros = [0] * append_length
            self.state = np.array([self.car.x, self.car.y, self.car.dir])
            holearray = np.array(self.holestate)
            zeroarray = np.array(listofzeros)
            self.state = np.append(self.state, holearray)
            self.state = np.append(self.state, zeroarray)

        return self.state, self.stepscore, done, {}

    def reset(self):
        self.stepscore = 0
        self.score = 0
        self.stepcount = 0
        self.car.reset()
        if PATH:
            self.path.reset()
        self.score = 0
        self.robrange.reset()
        # reset sensor values
        # create new holes
        self.hole_s.empty()
        for r in range(100):
            hole = holes.Holes()
            hole.add(self.hole_s)

        # create list of hole coordinates and IR´s
        self.holestate = []
        for hole in self.hole_s:
            self.holestate.append(hole.x)
            self.holestate.append(hole.y)


        # create observation state array

        self.state = np.array([self.car.x, self.car.y, self.car.dir])
        holearray = np.array(self.holestate)
        self.state = np.append(self.state, holearray)

        return self.state

    def render(self, mode='human'):
        # Show text data.
        text_fps = self.font.render('FPS: ' + str(int(self.clock.get_fps())), 1, (255, 127, 0))
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)
        text_score = self.font.render("Score: " + str(self.score), 1, (255, 127, 0))
        textpos_score = text_score.get_rect(centery=50, centerx=60)

        self.screen.blit(self.background, (0, 0))
        if PATH:
            self.path.image.fill((255, 127, 0), Rect(self.car.x, self.car.y, 5, 5))

        self.path_s.draw(self.screen)
        self.range_s.draw(self.screen)
        self.map_s.draw(self.screen)
        self.player_s.draw(self.screen)
        self.hole_s.draw(self.screen)

        self.screen.blit(text_fps, textpos_fps)
        self.screen.blit(text_score, textpos_score)

        pygame.display.update()
        self.clock.tick(120)

    def check_collision(self, sprite, sprite_group, dokill=False):
        spritelist = pygame.sprite.spritecollide(sprite, sprite_group, dokill, pygame.sprite.collide_mask)
        if spritelist:
            return spritelist
        else:
            return []
