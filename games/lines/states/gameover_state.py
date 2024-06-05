import pygame

import utils.utils as utils
from utils.database import SqliteDB
from utils.config_utils import ConfigUtils

from games.lines.states.base_state import BaseState
from games.lines.lines_menu import Menu, MenuItem
from games.lines.states.menu_state import MenuState
from games.lines.states.scores_state import ScoresState


class GameoverState(BaseState):
    def __init__(self, screen, score):
        self.screen = screen

        self.score = score
        self.player = ConfigUtils().getPlayer(game=1)

        self._scoreToFile()

        self._createMenu()

        imgDir = utils.getImgDir()
        self.background = utils.getImg(imgDir, 'bg_lines.jpg')
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size())
        utils.darken(self.background, 30)
        

    def run(self):
        self.screen.blit(self.background, (0, 0))
        self.menu.draw(self.screen)

    def keypressed(self, key, unicode):
        newState = self
        if key == pygame.K_LEFT:
            self.menu.choosePrevious()
        elif key == pygame.K_RIGHT:
            self.menu.chooseNext()
        elif key == pygame.K_RETURN:
            newState = self.menu.execute()
        return newState

    def _scoreToFile(self):
        db = SqliteDB('Lines')
        db.insertScore(self.player, self.score)

    def _createMenu(self):
        self.menu = Menu('Игра окончена!', f'Ваш счет: {self.score}')
        self.menu.addItems([MenuItem('Рекорды', ScoresState, self.screen, self),
                            MenuItem('В меню', MenuState,
                                     self.screen),
                            MenuItem('Выход', utils.returnValue, None)])
