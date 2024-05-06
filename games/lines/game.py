import pygame as pg
import pymunk
from pymunk import Vec2d
import numpy as np

from utils.utils import flipy
from games.lines.objects.ball import Ball
from games.lines.objects.box import Box
from games.lines.objects.line import Line
from games.lines.objects.attractor import Attractor

from enum import Enum

X, Y = 0, 1


class GameState(Enum):
    GAME = 0
    PAUSE = 1


class Game:
    BALL_SPAWN_EVENT = pg.USEREVENT + 1

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.state = GameState.GAME

        self.space = pymunk.Space()
        self.space.gravity = 0.0, config.GRAVITY

        # Objects
        self.balls = []

        # planet = Attractor(self.space)
        # planet1 = Attractor(self.space, (500, 600))

        self.planets = []
        self.prev_point = None
        self.lines = []

        self.box = Box(self.space, self.screen, 50, config.SCREEN_HEIGHT - 100,
                       config.BOX_WIDTH, config.BOX_HEIGHT)

        self.score = 0

        pg.time.set_timer(self.BALL_SPAWN_EVENT, 5000)
        self.background = pg.image.load('bg1.jpg')

    def display_score(self):
        font = pg.font.Font(None, 16)
        text = f"""SCORE: {self.score}"""

        y = 5
        for line in text.splitlines():
            text = font.render(line, True, (128, 128, 128))
            self.screen.blit(text, (5, y))
            y += 10

    def run(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.state = GameState.PAUSE
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos[X], flipy(event.pos[Y])
                self.balls.append(Ball(x, y, self.space, self.screen))
            # elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                # self.prev_point = None

            if event.type == self.BALL_SPAWN_EVENT:
                self.balls.append(Ball.spawn(self.space, self.screen))

        # if pg.mouse.get_pressed()[2]:
            # new_point = Vec2d(pg.mouse.get_pos()[
                #   0], flipy(pg.mouse.get_pos()[1]))
            # if self.prev_point is not None:
                # line = Line(self.prev_point, new_point,
                # self.screen, self.space)
                # self.lines.append(line)
            # self.prev_point = new_point
        p = pg.mouse.get_pos()

        for ball in self.balls:
            for p in self.planets:
                v = p.position - ball.body.position
                v_norm = v.normalized()
                dt = 1.0 / 60.0

                pymunk.Body.update_velocity(
                    ball.body, p.get_force(ball) * v_norm + self.space.gravity, 0.99, dt)

        dt = 1.0 / 60.0
        for x in range(1):
            self.space.step(dt)

        # DRAWING
        self.screen.fill(pg.Color("white"))

        self.screen.blit(self.background, (0, 0))
        # for p in self.planets:
        # p.draw_shape(self.screen)

        for ball in self.balls:
            if ball.in_box(self.box, self.balls, ball):
                self.score += 1
            ball.draw()

        # for line in self.lines:
        #     line.draw()

        self.box.draw()

        self.display_score()

        # Flip screen
        pg.display.flip()
        self.clock.tick(50)
        pg.display.set_caption("fps: " + str(self.clock.get_fps()))
        for line in self.lines:
            line.delete()
        self.lines = []
        # for p in self.planets:
        # p.delete()
        # self.planets = []
        # for p in self.planets:
        # print(p.body.position, p.radius)

    def pairwise(iterable):
        a = iter(iterable)
        return zip(a, a)

    def add_contour(self, contour):
        # new_line = Line.line_from_contour(contour, self.screen, self.space)
        # self.lines.append(new_line)
        contour = np.squeeze(contour, axis=1)
        for p1, p2 in Game.pairwise(contour):
            # For text
            if p1[1] < 30 or p2[1] < 30:
                continue
            # for b in self.balls:
                # f_p1 = Vec2d(p1[0], p1[1])
                # f_p2 = Vec2d(p2[0], p2[1])
                # print((b.body.position - f_p1).length)
                # if (b.body.position - f_p1).length + 2 <= b.radius or (b.body.position - f_p2).length + 2 <= b.radius:
                # print('!')
                # return
            points = np.array([p1, p2])
            # print(np.linalg.norm(points[0] - [points[1]]))
            # if np.linalg.norm(points[0] - [points[1]]) < 2:
            # continue
            new_line = Line(points, self.screen, self.space)
            self.lines.append(new_line)

    def add_attractor(self, p, r):
        p[1] = flipy(p[1])

        for planet in self.planets:
            if (planet.body.position - p).length < planet.radius:
                return
        # print(p, r)
        self.planets.append(Attractor(self.space, p, r + 5))

    def remove_planets(self, planets):
        for p in planets:
            p.delete()
            self.planets.remove(p)
