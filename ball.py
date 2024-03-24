import pygame as pg
import pymunk 
import numpy as np

class Ball:
    def __init__(self, x, y, space, radius=10) -> None:
        mass = 10
        moment = 100
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        
        self.radius = radius
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = 0.5
        self.shape.collision_type = 2

        space.add(self.body, self.shape)

    def draw(self):
        pass

    def apply_force(self, force):
        pass

    def update(self):
        pass

class BallPh:
    def __init__(self, x, y, radius=10):
        # self.velocity = np.array([0, 0], dtype=float)
        self.acceleration = np.array([0, 0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)

        self.position = np.array([x, y], dtype=float)
        self.position_old = np.array([x, y], dtype=float)
        
        self.radius = radius


    def draw(self, screen):
        pg.draw.circle(screen, pg.Color("blue"), self.position, self.radius, 1)

    def apply_force(self, force):
        self.acceleration += force

    def update(self, dt):
        self.velocity = self.position - self.position_old
        self.position_old[0] = self.position[0]
        self.position_old[1] = self.position[1]
        #self.position += (np.rint(self.velocity)).astype(int)
        self.position += self.velocity + self.acceleration * dt * dt
        self.acceleration *= 0 
