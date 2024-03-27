import pygame as pg
import pymunk
from pymunk import Vec2d
import numpy as np

import config
from objects.ball import Ball
from objects.box import Box
from utils import flipy, normalize
from objects.attractor import Attractor

import cProfile
import pstats
from enum import Enum

X, Y = 0, 1
# Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1
COLLTYPE_BALL = 2


class State(Enum):
    ARUCO = 0
    state = 1
    PAUSE = 2


def add_line(p1, p2, space):
    line = pymunk.Segment(
        space.static_body, p1, p2, 0.0
    )
    line.friction = 0.99
    space.add(line)
    return line


def display_text(screen, score):
    font = pg.font.Font(None, 16)
    text = f"""LMB: Create ball
    LMB + Shift: Create many balls
    RMB: Drag to create wall, release to finish
    Space: Pause physics simulation

    SCORE: {score}"""

    y = 5
    for line in text.splitlines():
        text = font.render(line, True, (128, 128, 128))
        screen.blit(text, (5, y))
        y += 10


def main():
    pg.init()
    screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pg.time.Clock()
    state = State.state

    # Physics stuff
    space = pymunk.Space()
    space.gravity = 0.0, config.GRAVITY

    # Balls
    balls = []

    planet = Attractor(space)
    planet1 = Attractor(space, (500, 600))

    planets = [planet]
    prev_point = None
    static_lines = []

    box = Box(space, screen, 400, 400, config.BOX_WIDTH, config.BOX_HEIGHT)

    score = 0

    BALL_SPAWN = pg.USEREVENT + 1
    pg.time.set_timer(BALL_SPAWN, 5000)
    while state != State.PAUSE:
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                state = State.PAUSE
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos[X], flipy(event.pos[Y])
                balls.append(Ball(x, y, space, screen))
            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                prev_point = None

            if event.type == BALL_SPAWN:
                balls.append(Ball.spawn(space, screen))

        if pg.mouse.get_pressed()[2]:
            new_point = Vec2d(event.pos[X], flipy(event.pos[Y]))
            if prev_point is not None:
                line = add_line(prev_point, new_point, space)
                static_lines.append(line)
            prev_point = new_point
        p = pg.mouse.get_pos()

        for ball in balls:
            for p in planets:

                v = p.position - ball.body.position
                v_norm = v.normalized()
                dt = 1.0 / 60.0

                pymunk.Body.update_velocity(
                    ball.body, p.get_force(ball) * v_norm + space.gravity, 0.99, dt)

        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        # DRAWING
        screen.fill(pg.Color("white"))

        for p in planets:
            p.draw_shape(screen)

        for ball in balls:
            if ball.in_box(box, balls, ball):
                score += 1
            ball.draw()

        for line in static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = int(pv1.x), int(flipy(pv1.y))
            p2 = int(pv2.x), int(flipy(pv2.y))
            pg.draw.lines(screen, pg.Color("lightgray"), False, [p1, p2])

        box.draw()

        display_text(screen, score)

        # Flip screen
        pg.display.flip()
        clock.tick(50)
        pg.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    doprof = 0
    if not doprof:
        main()
    else:
        prof = cProfile.run("main()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats("cumulative", "time", "calls")
        stats.print_stats(30)
