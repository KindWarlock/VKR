import pygame
import pymunk
import pymunk.pygame_util

import utils.utils as utils
from utils.config_utils import ConfigUtils


class Box:
    def __init__(self, space, screen, x, y, w, h) -> None:
        self.space = space
        self.body = pymunk.Body(0, 0, pymunk.Body.KINEMATIC)
        self.screen = screen

        self.rect = (x, y, w, h)
        y_pm = utils.flipy(y)

        seg1 = pymunk.Segment(self.body, (0, 0), (0, -h), 10)
        seg2 = pymunk.Segment(self.body, (0, -h), (w, -h), 10)
        seg3 = pymunk.Segment(self.body, (w, 0), (w, -h), 10)

        self.segments = [seg1, seg2, seg3]

        space.add(self.body, *self.segments)

        self.color = (170, 92, 196)
        # self.balls = []
        self.body.velocity = pymunk.Vec2d(1, 0)
        self.body.position = pymunk.Vec2d(x, y_pm)
        self.body.position_func = Box.move

        imgPath = utils.getImgDir()
        self.img = utils.getImg(imgPath, 'lines_box.png')
        self.img = pygame.transform.scale(self.img, (w + 10, h + 10))

    def is_inside(self, ball) -> bool:
        ball_x = ball.body.position[0]
        ball_y = utils.flipy(ball.body.position[1])
        x, y, w, h = self.body.position.x, utils.flipy(
            self.body.position.y), 100, 50
        is_higher = ball_y + ball.radius < y
        is_lower = ball_y - ball.radius > y + h
        is_right = ball_x - ball.radius > x + w
        is_left = ball_x + ball.radius < x

        if is_higher or is_lower:
            return False
        if is_right or is_left:
            return False

        if ball in self.balls:
            return False

        self.balls.append(ball)
        self.color = (97, 201, 116)
        return True

    def draw(self) -> None:
        x, y, w, h = self.body.position.x, utils.flipy(
            self.body.position.y), 100, 50
        # pts = ((x, y), (x, y+h), (x+w, y+h), (x+w, y))
        # pygame.draw.lines(self.screen, self.color, False, pts, 3)
        # self.space.debug_draw(pymunk.pygame_util.DrawOptions(self.screen))
        self.screen.blit(self.img, (x - 5, y - 5))

    def move(body, dt):
        body.position += body.velocity
        if body.position.x <= 0 or body.position.x + 100 >= ConfigUtils().getScreenParams()[0]:
            body.velocity *= -1
            body.position += 2 * body.velocity
