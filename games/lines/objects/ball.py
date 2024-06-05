import pygame
import pymunk

from threading import Timer
import random

import utils.utils as utils
from utils.config_utils import ConfigUtils


class Ball:
    RADIUS = 10

    def __init__(self, x, y, space, screen) -> None:
        mass = 20
        moment = 1000

        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y

        self.radius = Ball.RADIUS
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
        self.shape.friction = 10
        self.shape.elasticity = 0.1
        self.shape.collision_type = 2

        self.space = space
        self.screen = screen
        space.add(self.body, self.shape)
        self.is_in_box = False

        self.soundMissed = pygame.mixer.Sound(utils.getSound('falling.ogg'))
        self.soundHit = pygame.mixer.Sound(utils.getSound('e.ogg'))

        imgPath = utils.getImgDir()
        self.img = utils.getImg(imgPath, 'lines_ball.png')
        self.img = pygame.transform.scale(
            self.img, (self.radius * 2, self.radius * 2))

    def draw(self):
        pos = (self.body.position.x, utils.flipy(self.body.position.y))
        # pygame.draw.circle(self.screen, pygame.Color(
        #     "red"), (x, y), self.radius, 0)

        # rot = ball.body.rotation_vector
        # p = int(v.x), int(flipy(v.y))
        # p2 = p + Vec2d(rot.x, -rot.y) * r * 0.9
        # p2 = int(p2.x), int(p2.y)
        # pygame.draw.circle(screen, pygame.Color("blue"), p, int(r), 2)
        # pygame.draw.line(screen, pygame.Color("red"), p, p2)
        angle = self.body.angle

        img = pygame.transform.rotate(self.img, angle)
        rect = img.get_rect(center=pos)
        self.screen.blit(img, rect)

    def inBox(self, box, balls_list, ball_ref):
        if self.is_in_box:
            return False

        x = self.body.position.x
        y = utils.flipy(self.body.position.y)
        box_x, box_y, box_w, box_h = box.body.position.x, utils.flipy(
            box.body.position.y), box.rect[2], box.rect[3]
        is_higher = y + self.radius < box_y
        is_lower = y - self.radius > box_y + box_h
        is_right = x - self.radius > box_x + box_w
        is_left = x + self.radius < box_x

        if is_higher or is_lower:
            return False
        if is_right or is_left:
            return False

        self.soundHit.play()
        self.is_in_box = True
        Timer(3, self.delete, (balls_list, ball_ref)).start()
        return True

    def delete(self, balls_list, ball_ref):
        self.space.remove(self.shape, self.body)
        balls_list.remove(ball_ref)

    def spawn(space, screen):
        y = -Ball.RADIUS - 10
        x = random.randint(Ball.RADIUS + 10,
                           ConfigUtils().getScreenParams()[0] - Ball.RADIUS - 10)

        return Ball(x, utils.flipy(y), space, screen)

    @property
    def isAbsent(self):
        return self.screen.get_height() < utils.flipy(self.body.position.y) - self.radius
