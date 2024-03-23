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