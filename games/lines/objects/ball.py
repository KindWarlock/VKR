import pygame as pg
import pymunk
import numpy as np

from threading import Timer
import random

import config
from utils.utils import flipy


class Ball:
    def __init__(self, x, y, space, screen, radius=config.BALL_RADIUS) -> None:
        mass = 10
        moment = 1000

        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y

        self.radius = radius
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = 10
        self.shape.elasticity = 0.1

        self.space = space
        self.screen = screen
        space.add(self.body, self.shape)
        self.is_in_box = False

    def draw(self):
        x, y = self.body.position.x, flipy(self.body.position.y)
        pg.draw.circle(self.screen, pg.Color("red"), (x, y), self.radius, 0)

    def in_box(self, box, balls_list, ball_ref):
        if self.is_in_box:
            return False

        x = self.body.position.x
        y = flipy(self.body.position.y)
        box_x, box_y, box_w, box_h = box.body.position.x, flipy(
            box.body.position.y), config.BOX_WIDTH, config.BOX_HEIGHT
        is_higher = y + self.radius < box_y
        is_lower = y - self.radius > box_y + box_h
        is_right = x - self.radius > box_x + box_w
        is_left = x + self.radius < box_x

        if is_higher or is_lower:
            return False
        if is_right or is_left:
            return False

        self.is_in_box = True
        Timer(3, self._delete, (balls_list, ball_ref)).start()
        return True

    def _delete(self, balls_list, ball_ref):
        self.space.remove(self.shape, self.body)
        balls_list.remove(ball_ref)

    def spawn(space, screen):
        y = -config.BALL_RADIUS - 10
        x = random.randint(config.BALL_RADIUS + 10,
                           config.SCREEN_WIDTH - config.BALL_RADIUS - 10)

        return Ball(x, flipy(y), space, screen)


class BallPh:
    def __init__(self, x, y, radius=10):
        # self.velocity = np.array([0, 0], dtype=float)
        self.acceleration = np.array([0, 0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)

        self.position = np.array([x, y], dtype=float)
        self.position_old = np.array([x, y], dtype=float)
        self.position_temp = np.array([x, y], dtype=float)

        self.bounce = 0.9
        self.radius = radius

    def draw(self, screen):
        pg.draw.circle(screen, pg.Color("blue"), self.position, self.radius, 1)

    def apply_force(self, force):
        self.acceleration += force

    def update(self, dt):
        self.velocity = self.position - self.position_old
        # self.position_temp[0] = self.position[0]
        # self.position_temp[1] = self.position[1]
        self.position_old[0] = self.position[0]
        self.position_old[1] = self.position[1]

        self.position += self.velocity + self.acceleration * dt * dt
        self.acceleration *= 0

    def update_old_pos(self, old_pos):
        # self.position_old[0] = self.position_temp[0]
        # self.position_old[1] = self.position_temp[1]
        self.position_old[0] = old_pos[0]
        self.position_old[1] = old_pos[1]
