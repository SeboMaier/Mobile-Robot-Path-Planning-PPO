import pygame
import maps
from pygame.locals import *
import math
import numpy as np
from random import randint
import player
import camera
import holes
import path
import sensors
import gym
from gym import spaces

PATH = True
USE_SENSORS = True
SHOW_SENSORS = True


class Simulation(gym.Env):
    def __init__(self):
        metadata = {'render.modes': ['human']}
        pygame.init()

        self.action_space = spaces.Discrete(3)
        low = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        high = np.array([360, 4000, 4000, 700, 700, 700, 700, 700])

        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.score = 0
        self.stepscore = 0
        self.stepcount = 0
        self.realscore = 0
        self.previous_score = 0
        self.done = 0

        self.map_s = pygame.sprite.Group()
        self.player_s = pygame.sprite.Group()
        self.path_s = pygame.sprite.Group()
        self.hole_s = pygame.sprite.Group()
        self.sensor_s = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((1800, 1000))


        self.clock = pygame.time.Clock()
        self.CENTER_X = int(pygame.display.Info().current_w / 2)
        self.CENTER_Y = int(pygame.display.Info().current_h / 2)
        self.running = True
        start_angle = 270
        self.car = player.Player(start_angle)
        self.cam = camera.Camera()
        self.current_map = maps.Map()
        self.path = path.Path()


        # Sensoren erstellen
        if USE_SENSORS:
            self.sensor1 = sensors.Sensor(0)
            self.sensor2 = sensors.Sensor(30)
            self.sensor3 = sensors.Sensor(90)
            self.sensor4 = sensors.Sensor(270)
            self.sensor5 = sensors.Sensor(330)
            self.sensor_s.add(self.sensor1)
            self.sensor_s.add(self.sensor2)
            self.sensor_s.add(self.sensor3)
            self.sensor_s.add(self.sensor4)
            self.sensor_s.add(self.sensor5)

            # create new holes

        hole = holes.Holes()
        hole.add(self.hole_s)
        self.dist_x = hole.x - self.car.x
        self.dist_y = hole.y - self.car.y

        self.state = np.array([self.car.dir, self.dist_x, self.dist_y, self.sensor1.delta, self.sensor2.delta,
                               self.sensor3.delta, self.sensor4.delta, self.sensor5.delta])

        self.map_s.add(self.current_map)
        self.player_s.add(self.car)
        self.path_s.add(self.path)
        pygame.display.set_caption('RoboSimAI')
        pygame.mouse.set_visible(True)
        self.font = pygame.font.Font(None, 24)

        self.background = pygame.Surface(self.screen.get_size())

        self.background.fill((210, 210, 250))

    def step(self, action):
        # action[0] in range -1, 1: speed
        # action[1] in range -1, 1: steering
        # action[2] in range -1, 1: drill
        self.done = 0;
        self.stepscore = 0
        self.stepcount += 1

        for hole in self.hole_s.sprites():
            self.dist_x = hole.x - self.car.x
            self.dist_y = hole.y - self.car.y

        if action == 0:
            self.car.update()

        elif action == 1:
            self.car.steerleft()

        elif action == 2:
            self.car.steerright()

        self.path_s.update(self.cam.x, self.cam.y)
        self.hole_s.update(self.cam.x, self.cam.y)
        self.map_s.update(self.cam.x, self.cam.y)

        if USE_SENSORS:
            self.sensor_s.update(self.car.dir, self.CENTER_X, self.CENTER_Y)
            self.measure(self.sensor_s)


        if self.check_collision(self.car, self.map_s):
            self.done = 1
            self.stepscore -= 1
            self.car.reset()
            self.car.dir = 270

        if self.stepcount > 1000:
            self.done = 1
            self.car.reset()
            self.car.dir = 270

        if self.check_collision(self.car, self.hole_s):
            self.done = 1
            self.car.reset()
            self.car.dir = 270

        self.cam.set_pos(self.car.x, self.car.y)
        for hole in self.hole_s.sprites():
            self.score = (((hole.x - 900)**2 + (hole.y - 500)**2)**0.5 - ((hole.x - self.car.x)**2 + (hole.y - self.car.y)**2)**0.5)*0.01 - (self.stepcount * 0.02)

        self.stepscore = self.score - self.previous_score
        self.realscore += self.stepscore
        self.previous_score = self.score

        if self.done:
            self.stepscore = 0

        self.state = np.array([self.car.dir, self.dist_x, self.dist_y, self.sensor1.delta, self.sensor2.delta,
                               self.sensor3.delta, self.sensor4.delta, self.sensor5.delta])

        #render #######################################################
        pygame.event.pump()
        # Show text data.
        text_fps = self.font.render('FPS: ' + str(int(self.clock.get_fps())), 1, (255, 127, 0))
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)
        text_score = self.font.render("Score: " + str(self.realscore), 1, (255, 127, 0))
        textpos_score = text_score.get_rect(centery=50, centerx=150)
        if USE_SENSORS:
            text_s1 = self.font.render('S1: ' + str(int(self.sensor1.delta)), 1, (255, 127, 0))
            textpos_s1 = text_s1.get_rect(centery=75, centerx=60)
            text_s2 = self.font.render('S2: ' + str(int(self.sensor2.delta)), 1, (255, 127, 0))
            textpos_s2 = text_s1.get_rect(centery=100, centerx=60)
            text_s3 = self.font.render('S3: ' + str(int(self.sensor3.delta)), 1, (255, 127, 0))
            textpos_s3 = text_s1.get_rect(centery=125, centerx=60)
            text_s4 = self.font.render('S4: ' + str(int(self.sensor4.delta)), 1, (255, 127, 0))
            textpos_s4 = text_s1.get_rect(centery=150, centerx=60)
            text_s5 = self.font.render('S5: ' + str(int(self.sensor5.delta)), 1, (255, 127, 0))
            textpos_s5 = text_s1.get_rect(centery=175, centerx=60)

        self.screen.blit(self.background, (0, 0))
        if PATH:
            self.path.image.fill((255, 127, 0), Rect(self.car.x, self.car.y, 5, 5))

        self.path_s.draw(self.screen)
        self.map_s.draw(self.screen)
        if SHOW_SENSORS:
            self.sensor_s.draw(self.screen)
        self.player_s.draw(self.screen)
        self.hole_s.draw(self.screen)

        self.screen.blit(text_fps, textpos_fps)
        self.screen.blit(text_score, textpos_score)
        if USE_SENSORS:
            self.screen.blit(text_s1, textpos_s1)
            self.screen.blit(text_s2, textpos_s2)
            self.screen.blit(text_s3, textpos_s3)
            self.screen.blit(text_s4, textpos_s4)
            self.screen.blit(text_s5, textpos_s5)

        pygame.display.update()
        self.clock.tick(120)
        ###end render #################################

        return self.state, self.stepscore, self.done, {}

    def reset(self):
        self.stepscore = 0
        self.score = 0
        self.stepcount = 0
        self.previous_score = 0
        self.realscore = 0
        self.car.reset()

        if PATH:
            self.path.reset()
        self.score = 0
        # reset sensor values
        for r in self.sensor_s:
            r.delta = 700
        # create new holes
        self.hole_s.empty()
        hole = holes.Holes()
        hole.add(self.hole_s)
        self.car.dir = 270
        self.dist_x = hole.x - self.car.x
        self.dist_y = hole.y - self.car.y


        # create observation state array
        self.state = np.array([self.car.dir, self.dist_x, self.dist_y, self.sensor1.delta, self.sensor2.delta,
                               self.sensor3.delta, self.sensor4.delta, self.sensor5.delta])

        return self.state

    def render(self, mode='human'):
        pass

    def check_collision(self, sprite, sprite_group, dokill=False):
        spritelist = pygame.sprite.spritecollide(sprite, sprite_group, dokill, pygame.sprite.collide_mask)
        if spritelist:
            return spritelist
        else:
            return []

    def measure(self, sensor_s):
        for sensor in sensor_s:
            if sensor.rotangle >= 360:
                sensor.rotangle -= 360
            if sensor.rotangle <= 0:
                dx0 = sensor.rect.bottomleft[0]
                dx1 = sensor.rect.bottomleft[1]
            if 0 < sensor.rotangle <= 90:
                dx0 = sensor.rect.bottomright[0]
                dx1 = sensor.rect.bottomright[1]
            if 90 < sensor.rotangle <= 180:
                dx0 = sensor.rect.topright[0]
                dx1 = sensor.rect.topright[1]
            if 180 < sensor.rotangle <= 270:
                dx0 = sensor.rect.topleft[0]
                dx1 = sensor.rect.topleft[1]
            if 270 < sensor.rotangle < 360:
                dx0 = sensor.rect.bottomleft[0]
                dx1 = sensor.rect.bottomleft[1]

            offset_x = -self.current_map.rect.topleft[0] + sensor.rect.topleft[0]
            offset_y = -self.current_map.rect.topleft[1] + sensor.rect.topleft[1]
            sensor.mask = pygame.mask.from_surface(sensor.image)
            if self.current_map.mask.overlap(sensor.mask, (offset_x, offset_y)) is not None:
                ix, iy = self.current_map.mask.overlap(sensor.mask, (offset_x, offset_y))
                dx = - ix - self.current_map.rect.topleft[0] + dx0
                dy = - iy - self.current_map.rect.topleft[1] + dx1
                sensor.delta = math.sqrt(dx ** 2 + dy ** 2)
                if sensor.delta >= 700:
                    sensor.delta = 700
            else:
                sensor.delta = 700
