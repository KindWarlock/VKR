import pygame as pg
import numpy as np

from enum import Enum

from objects.line import LinePh
from objects.ball import BallPh
import config

import math


class State(Enum):
    ARUCO = 0
    RUNNING = 1
    PAUSE = 2


def create_box():
    return LinePh([[0, 0], [config.SCREEN_WIDTH, 0], [config.SCREEN_WIDTH, config.SCREEN_HEIGHT - 100], [0, config.SCREEN_HEIGHT], [0, 0]])


def circle_line_dist(c, l):
    return np.linalg.norm(np.cross(l[1]-l[0], l[0]-c.position)) / np.linalg.norm(l[1]-l[0])


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def perpendicular(line):
    perpendicular = np.empty_like(line)
    perpendicular[0] = -line[1]
    perpendicular[1] = line[0]
    perpendicular -= perpendicular[0]
    return perpendicular


def sign(num):
    return np.sign(num) if num != 0 else 1.0


def resolve_collision(ball, line, dist):
    perp = perpendicular(normalize(line))[1]

    # if perp[0] == 0:
    #    angle = 0
    # else:
    #    angle = math.atan(perp[1] / perp[0])

    # x_ns = math.sin(angle) * abs(dist)
    # y_ns = math.cos(angle) * abs(dist)
    # x = math.sin(angle) * abs(dist) * sign_x
    # y = math.cos(angle) * abs(dist) * sign_y
#
    # ball.position[0] -= x
    # ball.position[1] -= y

    sign_x = 1 if sign(perp[0]) == sign(ball.velocity[0]) else -1
    sign_y = 1 if sign(perp[1]) == sign(ball.velocity[1]) else -1
    print(ball.velocity)
    ball.position -= normalize(perp) * abs(dist) * [sign_x, sign_y]


def find_intersection(line1, line2):
    s = np.vstack([line1[0], line1[1], line2[0], line2[1]]
                  )        # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)


pg.init()
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pg.time.Clock()

gravity = np.array([0.0, -config.GRAVITY])

# Balls
balls = []
state = State.RUNNING
prev_t = 0

lines = []
lines.append(create_box())
collided = False
intersection = None

while state != State.PAUSE:
    for event in pg.event.get():
        if (event.type == pg.QUIT) or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            state = State.PAUSE
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos[0], event.pos[1]
            balls.append(BallPh(x, y))

    # Draw stuff
    screen.fill(pg.Color("white"))

    t = pg.time.get_ticks()
    dt = (t - prev_t) / 1000
    prev_t = t

    for ball in balls:
        ball.apply_force(gravity)
        ball.update(dt)

        for line in lines:
            for line_part in line.to_lines():
                dist = circle_line_dist(ball, line_part) - ball.radius
                if dist < 0:

                    # intersection = find_intersection(
                    #     line_part, [ball.position_old, ball.position])
                    #
                    # so = normalize(
                    #     ball.position - intersection) * ball.radius
                    # ball.position_old = so + intersection

                    intersection = find_intersection(
                        line_part, [ball.position, [ball.position[0], 0]])

                    # ball.position_old[1] = intersection[1] - ball.radius

                    # intersection = ball.position_old
                    resolve_collision(ball, line_part, dist)

                    collided = True
        # if collided:
        #     ball.update_old_pos()
        pg.draw.circle(screen, (0, 255, 0), ball.position, 2)

        ball.draw(screen)

    for line in lines:
        line.draw(screen)

    prev_t = t
    clock.tick(50)
    if collided:
        pg.draw.circle(screen, (255, 0, 0), intersection, 2)
    pg.display.flip()
    pg.display.set_caption("fps: " + str(clock.get_fps()))
