import pygame as pg
import pymunk 
from pymunk import Vec2d

import config
from ball import Ball
from box import Box
from utils import flipy

import cProfile
import pstats
from enum import Enum

X, Y = 0, 1
### Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1
COLLTYPE_BALL = 2

class State(Enum):
    ARUCO = 0
    RUNNING = 1
    PAUSE = 2


def check_coll(obj1, obj2):
    pass


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
        text = font.render(line, True, pg.Color("black"))
        screen.blit(text, (5, y))
        y += 10


def main():
    pg.init()
    screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pg.time.Clock()
    state = State.state

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = 0.0, config.GRAVITY

    ## Balls
    balls = []
    
    ### Static line
    prev_point = None
    static_lines = []

    box = Box(space, screen, 400, 400, 100, 50)

    score = 0
    while state != State.PAUSE:
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                state = State.PAUSE
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos[X], flipy(event.pos[Y])
                balls.append(Ball(x, y, space).shape)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                    prev_point = None

        if pg.mouse.get_pressed()[2]:
            new_point = Vec2d(event.pos[X], flipy(event.pos[Y]))
            if prev_point is not None:
                line = add_line(prev_point, new_point, space)
                static_lines.append(line)
            prev_point = new_point
        p = pg.mouse.get_pos()

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Draw stuff
        screen.fill(pg.Color("white"))

        # Display some text
        display_text(screen, score)
        

        for ball in balls:
            r = ball.radius 
            v = ball.body.position
            rot = ball.body.rotation_vector
            p = int(v.x), int(flipy(v.y))
            p2 = p + Vec2d(rot.x, -rot.y) * r * 0.9
            p2 = int(p2.x), int(p2.y)
            pg.draw.circle(screen, pg.Color("blue"), p, int(r), 2)
            pg.draw.line(screen, pg.Color("red"), p, p2)

            if box.is_inside(ball):
                score += 1

        for line in static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = int(pv1.x), int(flipy(pv1.y))
            p2 = int(pv2.x), int(flipy(pv2.y))
            pg.draw.lines(screen, pg.Color("lightgray"), False, [p1, p2])

        box.draw()
        ### Flip screen
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