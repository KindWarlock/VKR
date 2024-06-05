import pygame
import pymunk
from scipy.constants import G
import utils.utils as utils


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
        self.shape.collision_type = 1

        space.add(self.body, self.shape)
        self.space = space

        imgPath = utils.getImgDir()
        self.img = utils.getImg(imgPath, 'lines_planet.png')
        self.img = pygame.transform.scale(self.img, (radius * 2, radius * 2))

    def draw(self, screen):
        pos = (self.body.position.x, utils.flipy(self.body.position.y))
        # pygame.draw.circle(screen, pygame.Color('yellow'), pos, self.radius)
        rect = self.img.get_rect(center=pos)
        screen.blit(self.img, rect)

    def getForce(self, ball):
        center = self.body.local_to_world(self.body.center_of_gravity)
        dist = center.get_distance(ball.body.position)
        return G * self.mass * ball.body.mass / (dist * dist)

    def delete(self):
        self.space.remove(self.shape, self.body)
