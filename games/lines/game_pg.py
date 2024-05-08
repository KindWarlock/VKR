import pygame
import pymunk
from pymunk import Vec2d
import numpy as np

from utils.utils import flipy
from games.lines.objects.ball import Ball
from games.lines.objects.box import Box
from games.lines.objects.line import Line
from games.lines.objects.attractor import Attractor


from utils.config_utils import ConfigUtils

from enum import Enum

X, Y = 0, 1


class GameState(Enum):
    GAME = 0
    PAUSE = 1


class LinesGame:
    TIMER_EVENT = pygame.USEREVENT + 0
    BALL_SPAWN_EVENT = pygame.USEREVENT + 1

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = GameState.GAME

        self.space = pymunk.Space()
        self.space.gravity = 0.0, -10

        # Objects
        self.balls = []

        self.planets = []

        self.box = Box(self.space, self.screen, 50, ConfigUtils().getScreenParams()[0] - 100,
                       50, 100)

        self.fps = ConfigUtils.getScreenParams()[2]
        self.score = 0

        pygame.time.set_timer(self.BALL_SPAWN_EVENT, 5000)
        pygame.time.set_timer(self.TIMER_EVENT, 1000)

        self.background = pygame.image.load('bg1.jpg')

    def displayScore(self):
        font = pygame.font.Font(None, 16)
        text = f"""SCORE: {self.score}"""

        y = 5
        for line in text.splitlines():
            text = font.render(line, True, (128, 128, 128))
            self.screen.blit(text, (5, y))
            y += 10

    def run(self):
        p = pygame.mouse.get_pos()

        for ball in self.balls:
            for p in self.planets:
                v = p.position - ball.body.position
                v_norm = v.normalized()
                dt = 1.0 / 60.0

                pymunk.Body.update_velocity(
                    ball.body, p.get_force(ball) * v_norm + self.space.gravity, 0.99, dt)

        dt = 1.0 / 60.0
        self.space.step(dt)

        # DRAWING
        self.screen.fill(pygame.Color("white"))

        self.screen.blit(self.background, (0, 0))
        # for p in self.planets:
        # p.draw_shape(self.screen)

        for ball in self.balls:
            if ball.inBox(self.box, self.balls, ball):
                self.score += 1
            ball.draw()

        # for line in self.lines:
        #     line.draw()

        self.box.draw()

        self.displayScore()

        # Flip screen
        # pygame.display.flip()
        self.clock.tick(self.fps)
        # pygame.display.set_caption("fps: " + str(self.clock.get_fps()))
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

    def addContour(self, contour):
        # new_line = Line.line_from_contour(contour, self.screen, self.space)
        # self.lines.append(new_line)
        contour = np.squeeze(contour, axis=1)
        for p1, p2 in self.pairwise(contour):
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

    def addAttractor(self, p, r):
        p[1] = flipy(p[1])

        for planet in self.planets:
            if (planet.body.position - p).length < planet.radius:
                return
        # print(p, r)
        self.planets.append(Attractor(self.space, p, r + 5))

    def removePlanets(self, planets):
        for p in planets:
            p.delete()
            self.planets.remove(p)

    def handleEvent(self, event):
        if event.type == self.BALL_SPAWN_EVENT:
            self.balls.append(Ball.spawn(self.space, self.screen))
