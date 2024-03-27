import pygame as pg
import pymunk
from scipy.constants import G
from utils import flipy


class Attractor(pg.sprite.Sprite):
    def __init__(self, space, position=(300, 400), radius=30, mass=4000000000000000):
        pg.sprite.Sprite.__init__(self)
        self.radius = radius
        self.mass = mass
        self.position = position
        # self.outer_radius =

        self.body = pymunk.Body(mass, 0, pymunk.Body.STATIC)
        self.body.position = self.position

        self.radius = radius
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = 10
        self.shape.elasticity = 0
        space.add(self.body, self.shape)

    def draw_shape(self, screen):
        pos = (self.position[0], flipy(self.position[1]))
        pg.draw.circle(screen, (217, 143, 82), pos, self.radius)

    def get_force(self, ball):
        center = self.body.local_to_world(self.body.center_of_gravity)
        dist = center.get_distance(ball.body.position)
        return G * self.mass * ball.body.mass / (dist * dist)