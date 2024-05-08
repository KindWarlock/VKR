import pygame
import pymunk
from scipy.constants import G
from utils.utils import flipy


class Attractor(pygame.sprite.Sprite):
    def __init__(self, space, position=(300, 400), radius=30, mass=4000000000000000):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.mass = mass
        self.position = position
        # self.outer_radius =

        self.body = pymunk.Body(mass, 0, pymunk.Body.STATIC)
        self.body.position = self.position

        self.radius = int(radius)
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = 10
        self.shape.elasticity = 0
        space.add(self.body, self.shape)
        self.space = space

    def drawShape(self, screen):
        pos = (self.body.position.x, flipy(self.body.position.y))
        pygame.draw.circle(screen, pygame.Color('yellow'), pos, self.radius)

    def getForce(self, ball):
        center = self.body.local_to_world(self.body.center_of_gravity)
        dist = center.get_distance(ball.body.position)
        return G * self.mass * ball.body.mass / (dist * dist)

    def delete(self):
        self.space.remove(self.shape, self.body)
