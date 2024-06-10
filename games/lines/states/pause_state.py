import pygame

import utils.utils as utils

from games.shooter.states.base_state import BaseState
from games.lines.lines_menu import Menu, MenuItem


class PauseState(BaseState):
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self._createMenu()

    def run(self):
        self.game.draw()
        utils.darken(self.screen)
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

    def _createMenu(self):
        from games.lines.states.menu_state import MenuState

        self.menu = Menu('Пауза')
        self.menu.addItems([MenuItem('Заново', self.game.start),
                            MenuItem('Продолжить', utils.returnValue,
                                     self.game),
                            MenuItem('Выход', MenuState, self.screen)])
