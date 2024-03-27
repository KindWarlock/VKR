import pygame as pg
import numpy as np
import config

class Line:
    def __init__(self, pts, bbox):
        self.pts = pts
        self.bbox = bbox
        self.buffer = np.empty((config.SCREEN_HEIGHT, config.SCREEN_WIDTH))

    def is_same(self, frame):
        pass

    def is_line(frame, bbox):
        pass

class LinePh:
    def __init__(self, pts):
        self.pts = pts

    def draw(self, screen):
        pg.draw.lines(screen, (0, 0, 0), False, self.pts)

    def to_lines(self):
        res = np.array(list(zip(self.pts, self.pts[1:])))
        return res