import pygame as pg
import pymunk 

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