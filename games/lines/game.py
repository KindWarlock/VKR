import cv2

from games.lines.game_pg import LinesGame
import games.lines.game_cv as game_cv

import utils.cv_utils as cv_utils


class Game:
    def __init__(self, screen):
        self.game = LinesGame(screen)
        self.cap = cv_utils.openCam()
        # self.prevContours = []
        # self.subtractor = cv2.createBackgroundSubtractorMOG2(
        # history=1000, varThreshold=50, detectShadows=False)
        # game_cv.createTrackbar()

    def process(self, frame):
        blurred = game_cv.preprocess(frame)

        # Находим игровые объекты
        contours, planets = game_cv.findObjects(blurred)

        # newContours = game_cv.findNewLines(
        # frame, contours, self.game.delegateToState('getContours'))
        # newContours = game_cv.findNewLines(
        # frame, contours, self.prevContours)

        # self.prevContours = contours
        # Переводим найденные контуры в игровые сегменты
        for c in contours:
            self.game.delegateToState('addContour', c)

        # Проверяем старые планеты. Если их больше нет - удаляем
        planetsToRemove = game_cv.checkPlanets(
            frame, self.game.delegateToState('getPlanets'))
        self.game.delegateToState('removePlanets', planetsToRemove)

        # # Если есть новые планеты
        if planets is not None and len(planets) > len(self.game.delegateToState('getPlanets')):
            for p in planets:
                self.game.delegateToState('addAttractor', [p[0], p[1]], p[2])

        # game_cv.findNewLines(frame, self.subtractor)

    def run(self):
        back = self.game.run()
        if not self.game.isRunning:
            return back

        ret, frame = self.cap.read()
        if ret:
            frame = cv_utils.fixFrame(frame)
            frame = cv_utils.normalize(frame)
            self.process(frame)
            # cv2.imshow('Frame', frame)

        return back

    def keypressed(self, key, unicode):
        return self.game.keypressed(key, unicode)

    def handleEvent(self, event):
        self.game.handleEvent(event)
