import pygame
import pymunk
import pymunk.pygame_util
import numpy as np

import utils.utils as utils
from games.lines.objects.ball import Ball
from games.lines.objects.box import Box
from games.lines.objects.line import Line
from games.lines.objects.attractor import Attractor

from games.lines.states.base_state import BaseState
from games.lines.states.pause_state import PauseState
from utils.config_utils import ConfigUtils


class GameState(BaseState):
    timerEvent = pygame.USEREVENT + 0
    generationEvent = pygame.USEREVENT + 1

    STAMINA = 60
    TIME = 10

    def __init__(self, screen):
        self.screen = screen

        self.space = pymunk.Space()
        self.space.gravity = 0.0, -100

        pygame.time.set_timer(GameState.generationEvent, 1000)
        pygame.time.set_timer(GameState.timerEvent, 1000)

        imgDir = utils.getImgDir()
        self.background = utils.getImg(imgDir, 'bg_lines.jpg')
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size())

        self.scoreImg = utils.getImg(imgDir, 'lines_ball.png').convert_alpha()
        self.scoreImg = pygame.transform.scale(
            self.scoreImg, (30, 30))

        # Add collision handler
        collision_handler = self.space.add_collision_handler(2, 1)
        collision_handler.pre_solve = self.ball_attractor_collision
        self.start()

    def getContours(self):
        return self.contours

    def start(self):
        self.clock = pygame.time.Clock()

        self.score = 0
        self.timer = GameState.TIME
        self.timePassed = 0

        self.contours = []
        # Objects
        self.balls = []
        self.planets = []
        self.activeLines = []
        self.box = Box(self.space, self.screen, 50, ConfigUtils().getScreenParams()[1] - 110,
                       100, 70)

        return self

    def ball_attractor_collision(self, arbiter, space, data):
        ball, attractor = arbiter.shapes
        # Move the ball slightly outside the attractor radius to prevent sinking
        direction = ball.body.position - attractor.body.position
        direction = direction.normalized()
        ball.body.position = attractor.body.position + \
            direction * (attractor.radius + ball.radius)
        ball.body.velocity = pymunk.Vec2d(0, 0)  # Optionally adjust velocity

        return False  # Continue with default collision handling

    def _drawScore(self):
        # font = pygame.font.Font(None, 16)
        # text = f'''SCORE: {self.score}'''

        surf = pygame.surface.Surface(
            (self.scoreImg.get_width() + 30, self.scoreImg.get_height()), pygame.SRCALPHA).convert_alpha()
        surf.blit(self.scoreImg, (0, 0))

        fontFamily, fontSize = ConfigUtils().getFont()
        font = pygame.font.Font(fontFamily, fontSize)
        color = ConfigUtils().getColorScheme('Lines')['Text']['Light']
        textR = font.render(str(self.score), True, color)
        textRect = textR.get_rect(center=utils.getCenter(surf))
        textRect.x = self.scoreImg.get_width() + 10
        surf.blit(textR, textRect)

        # rect = surf.get_rect(center=utils.getCenter(self.screen))
        # rect.y = 20
        x = self.screen.get_width() - surf.get_width() - 30
        y = 30
        self.screen.blit(surf, (x, y))

    def _drawTime(self):
        pygame.draw.rect(
            self.screen, (255, 255, 255, 128), (0, 0, self.timeWidth, 10))

    def _writeTime(self):
        fontFamily, fontSize = ConfigUtils().getFont()
        myfont = pygame.font.Font(fontFamily, fontSize)

        label = myfont.render("Time left: " + str(self.timer), 1, (0, 0, 0))
        self.screen.blit(label, (self.screen.get_width() -
                         300, 10))

    def run(self):

        # for ball in self.balls:
        #     for p in self.planets:
        #         v = p.position - ball.body.position
        #         v_norm = v.normalized()
        #         dt = 1.0 / 60.0

        #         pymunk.Body.update_velocity(
        #             ball.body, p.getForce(ball) * v_norm + self.space.gravity, 0.99, dt)

        # dt = 1.0 / 60.0
        # self.space.step(dt)

        # DRAWING
        # self.screen.fill(pygame.Color("white"))

        # self.screen.blit(self.background, (0, 0))
        # for p in self.planets:
        # p.draw_shape(self.screen)

        # for ball in self.balls:
        #     if ball.inBox(self.box, self.balls, ball):
        #         self.score += 1
        #     ball.draw()

        # self.checkBalls()
        # for line in self.activeLines:
        #     line.draw()

        # self.box.draw()

        # self._writeScore()
        # self._writeTime()
        # self._drawTime()

        # Flip screen
        # pygame.display.flip()

        # pygame.display.set_caption("fps: " + str(self.clock.get_fps()))
        # for line in self.activeLines:
        #     line.delete()
        # self.activeLines = []
        # for p in self.planets:
        # p.delete()
        # self.planets = []

        self._updateGame()

        self._updateUi()
        self.draw()
        self._deleteObjects()

    def _deleteObjects(self):
        for line in self.activeLines:
            line.delete()
        self.activeLines = []

        self.checkBalls()

    def _updateGame(self):
        dt = 1.0 / 60.0

        # for ball in self.balls:
        #     for p in self.planets:
        #         v = p.position - ball.body.position
        #         v_norm = v.normalized()
        #         force = p.getForce(ball) * v_norm
        #         ball.body.apply_force_at_world_point(force, ball.body.position)
        #         # pymunk.Body.update_velocity(
        #         # ball.body, p.getForce(ball) * v_norm + self.space.gravity, 0.99, dt)
        #     ball.body.apply_force_at_world_point(
        #         self.space.gravity, self.space.gravity)

        for ball in self.balls:
            for p in self.planets:
                v = p.body.position - ball.body.position
                distance = v.length
                if distance == 0:
                    continue
                v_norm = v.normalized()
                force = p.getForce(ball) * v_norm
                ball.body.apply_force_at_world_point(force, ball.body.position)
        self.space.step(dt)

        for ball in self.balls:
            if ball.inBox(self.box, self.balls, ball):
                self.score += 1

        # self.checkBalls()
        # for line in self.activeLines:
        #     line.delete()
        # self.activeLines = []

    def _updateUi(self):
        dt = self.clock.get_time()
        self.timePassed += dt
        self.timeWidth = self.screen.get_width() - self.screen.get_width() * \
            self.timePassed / (GameState.TIME * 1000)

    def draw(self):
        self._drawBackground()
        for ball in self.balls:
            ball.draw()
        self.box.draw()

        self._drawScore()
        # self._writeTime()
        self._drawTime()

        for p in self.planets:
            p.draw(self.screen)
        self.clock.tick()

    def _drawBackground(self):
        self.screen.blit(self.background, (0, 0))

    def pairwise(iterable):
        a = iter(iterable)
        return zip(a, a)

    def getPlanets(self):
        return self.planets

    def addContour(self, contour):
        # new_line = Line.line_from_contour(contour, self.screen, self.space)
        # self.activeLines.append(new_line)
        contour = np.squeeze(contour, axis=1)
        for p1, p2 in GameState.pairwise(contour):
            # For text
            if p1[1] < 30 or p2[1] < 30:
                continue
            points = np.array([p1, p2])
            if np.linalg.norm(points[0] - [points[1]]) < 5:
                continue
            new_line = Line(points, self.screen, self.space)
            self.activeLines.append(new_line)

    def addAttractor(self, p, r):
        p[1] = utils.flipy(p[1])

        for planet in self.planets:
            if (planet.body.position - p).length < planet.radius:
                return
        # print(p, r)
        self.planets.append(Attractor(self.space, p, r+10))

    def removePlanets(self, planets):
        for p in planets:
            p.delete()
            self.planets.remove(p)

    def handleEvent(self, event):
        if event.type == GameState.generationEvent:
            self.balls.append(Ball.spawn(self.space, self.screen))
        elif event.type == GameState.timerEvent:
            self.timer -= 1
            if self.timer <= 0:
                return self.score

    def checkBalls(self):
        for ball in self.balls:
            if ball.isAbsent:
                ball.soundMissed.play()
                ball.delete(self.balls, ball)

    def keypressed(self, key, unicode):
        newState = self
        if key == pygame.K_ESCAPE:
            newState = PauseState(self.screen, self)

        return newState
