from games.lines.game_pg import LinesGame
import games.lines.game_cv as game_cv

import utils.cv_utils as cv_utils


class Game:
    def __init__(self, screen):
        self.game = LinesGame(screen)
        self.cap = game_cv.open_cam()

    def handleEvent(self, event):
        self.game.handleEvent(event)

    def process(self, frame):
        blurred = game_cv.preprocess(frame)

        # Находим игровые объекты
        contours, planets = game_cv.findObjects(blurred)

        # Переводим найденные контуры в игровые сегменты
        for c in contours:
            self.game.add_contour(c)

        # Проверяем старые планеты. Если их больше нет - удаляем
        planetsToRemove = game_cv.checkPlanets(
            frame, self.game.planets)
        self.game.removePlanets(planetsToRemove)

        # Если есть новые планеты
        if planets is not None and len(planets) > len(self.game.planets):
            for p in planets:
                self.game.addAttractor([p[0], p[1]], p[2])

    def run(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv_utils.fixFrame(frame)
            frame = cv_utils.normalize(frame)
            self.process(frame)

    def keypressed(self):
        ...

    # def _getHsv(self, x, y):
        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # print(hsv[y-5:y+5, x-5:x+5], x, y)

        # cv2.setMouseCallback('Warped', get_hsv)
