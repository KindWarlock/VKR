import pygame as pg
import pymunk
import numpy as np

import config
from utils.utils import flipy


class Line:
    def __init__(self, pts, screen, space):
        self.pts = pts
        pts[:, 1] = np.fromiter((flipy(y) for y in pts[:, 1]), np.float64)

        pts = list(map(tuple, pts))
        self.shape = pymunk.Segment(
            space.static_body, pts[0], pts[1], 3.0
        )
        # pts[:, 1] = np.fromiter((flipy(y) for y in pts[:, 1]), np.float64)
        # self.shape = pymunk.Poly(space.static_body, pts)
        self.shape.friction = 0.99
        space.add(self.shape)
        self.screen = screen
        self.space = space
        # self.bbox = bbox
        # self.buffer = np.empty((config.SCREEN_HEIGHT, config.SCREEN_WIDTH))

    def is_same(self, frame):
        pass

    def is_line(frame, bbox):
        pass

    def draw(self):
        body = self.shape.body
        pv1 = body.position + self.shape.a.rotated(body.angle)
        pv2 = body.position + self.shape.b.rotated(body.angle)
        p1 = int(pv1.x), int(flipy(pv1.y))
        p2 = int(pv2.x), int(flipy(pv2.y))
        pg.draw.lines(self.screen, pg.Color("lightgray"), False, [p1, p2])

    def line_from_contour(contour, screen, space):
        return Line(np.squeeze(contour, axis=1), screen, space)

    def delete(self):
        self.space.remove(self.shape)
