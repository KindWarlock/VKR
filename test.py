import pygame as pg
import numpy as np

from enum import Enum

from line import LinePh
from ball import BallPh
import config

import math

class State(Enum):
    ARUCO = 0
    RUNNING = 1
    PAUSE = 2

def create_box():
    return LinePh([[0, 0], [config.SCREEN_WIDTH, 0], [config.SCREEN_WIDTH, config.SCREEN_HEIGHT], [0, config.SCREEN_HEIGHT], [0, 0]])


def circle_line_dist(c, l):
    return np.linalg.norm(np.cross(l[1]-l[0], l[0]-c.position)) / np.linalg.norm(l[1]-l[0]) 

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


pg.init()
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pg.time.Clock()

gravity = np.array([0.0, -config.GRAVITY])

## Balls
balls = []
state = State.RUNNING
prev_t = 0

lines = []
lines.append(create_box())

while state != State.PAUSE:
    for event in pg.event.get():
        if (event.type == pg.QUIT) or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            state = State.PAUSE
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos[0], event.pos[1]
            balls.append(BallPh(x, y))

    ### Draw stuff
    screen.fill(pg.Color("white"))

    t = pg.time.get_ticks()
    dt = (t - prev_t) / 1000

    for ball in balls:
        collided = False
        ball.apply_force(gravity)
        ball.update(dt)

        for line in lines:
            for line_part in line.to_lines():
                dist = circle_line_dist(ball, line_part) - ball.radius
                if dist < 0:         
                    if ball.velocity[0] == 0:
                        angle = math.pi / 2
                    else:
                        angle = math.atan(ball.velocity[1] / ball.velocity[0])
                    x = math.cos(angle) * dist
                    y = math.sin(angle) * dist
                    ball.position[0] += x
                    ball.position[1] += y
                    collided = True

                    # ball.apply_force(-gravity * 20)


        ball.draw(screen)

    for line in lines:
        line.draw(screen)
        
    prev_t = t
    clock.tick(50)

    pg.display.flip()
    pg.display.set_caption("fps: " + str(clock.get_fps()))

