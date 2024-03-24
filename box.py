import pygame as pg
import pymunk

from utils import flipy

class Box:
    def __init__(self, space, screen, x, y, w, h) -> None:
        self.body = pymunk.Body(0, 0, pymunk.Body.KINEMATIC)
        self.screen = screen

        self.rect = (x, y, w, h)
        y_pm = flipy(y)
        seg1 = pymunk.Segment(self.body, (x, y_pm), (x, y_pm-h), 3)
        seg2 = pymunk.Segment(self.body, (x, y_pm-h), (x+w, y_pm-h), 3)
        seg3 = pymunk.Segment(self.body, (x+w, y_pm), (x+w, y_pm-h), 3)
        self.segments = [seg1, seg2, seg3]

        space.add(self.body, *self.segments)

        self.color = (255, 0, 0)        
        self.balls = []

    def is_inside(self, ball) -> bool:
        ball_x = ball.body.position[0]
        ball_y = flipy(ball.body.position[1])
        is_higher = ball_y + ball.radius < self.rect[1]
        is_lower = ball_y - ball.radius > self.rect[1] + self.rect[3]
        is_right = ball_x - ball.radius > self.rect[0] + self.rect[2]
        is_left = ball_x + ball.radius < self.rect[0]

        if is_higher or is_lower:
            return False
        if is_right or is_left:
            return False
        
        if ball in self.balls:
            return False
        
        self.balls.append(ball)
        self.color = (0, 255, 0)
        return True


    def draw(self) -> None:
        x, y, w, h = self.rect
        pts = ((x, y), (x, y+h), (x+w, y+h), (x+w, y))
        pg.draw.lines(self.screen, self.color, False, pts, 3)
        