import pygame as pg
import pymunk

from utils.utils import flipy
import config


class Box:
    def __init__(self, space, screen, x, y, w, h) -> None:
        self.body = pymunk.Body(0, 0, pymunk.Body.KINEMATIC)
        self.screen = screen

        self.rect = (x, y, w, h)
        y_pm = flipy(y)
        # seg1 = pymunk.Segment(self.body, (x, y_pm), (x, y_pm-h), 3)
        # seg2 = pymunk.Segment(self.body, (x, y_pm-h), (x+w, y_pm-h), 3)
        # seg3 = pymunk.Segment(self.body, (x+w, y_pm), (x+w, y_pm-h), 3)
        seg1 = pymunk.Segment(self.body, (0, 0), (0, -h), 3)
        seg2 = pymunk.Segment(self.body, (0, -h), (w, -h), 3)
        seg3 = pymunk.Segment(self.body, (w, 0), (w, -h), 3)

        self.segments = [seg1, seg2, seg3]

        space.add(self.body, *self.segments)

        self.color = (170, 92, 196)
        # self.balls = []
        self.body.velocity = pymunk.Vec2d(1, 0)
        self.body.position = pymunk.Vec2d(x, y_pm)
        self.body.position_func = Box.move
        # self.body.velocity_func = Box.move

    def is_inside(self, ball) -> bool:
        ball_x = ball.body.position[0]
        ball_y = flipy(ball.body.position[1])
        x, y, w, h = self.body.position.x, flipy(
            self.body.position.y), config.BOX_WIDTH, config.BOX_HEIGHT
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
        x, y, w, h = self.body.position.x, flipy(
            self.body.position.y), config.BOX_WIDTH, config.BOX_HEIGHT
        pts = ((x, y), (x, y+h), (x+w, y+h), (x+w, y))
        pg.draw.lines(self.screen, self.color, False, pts, 3)

    def move(body, dt):
        body.position += body.velocity
        if body.position.x <= 0 or body.position.x + config.BOX_WIDTH >= config.SCREEN_WIDTH:
            body.velocity *= -1
            body.position += 2 * body.velocity
