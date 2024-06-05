import pygame

from utils.config_utils import ConfigUtils
import utils.utils as utils

from games.lines.lines_menu import Menu, MenuItem
from utils.modal_window import ModalWindow, ModalType
from games.lines.states.base_state import BaseState
from games.lines.states.game_state import GameState
from games.lines.states.scores_state import ScoresState


class MenuState(BaseState):
    def __init__(self, screen):
        self.screen = screen
        self.modal = None
        self.player = ConfigUtils().getPlayer(game=1)

        self._createMenu()

        imgDir = utils.getImgDir()
        self.background = utils.getImg(imgDir, 'bg_lines.jpg')
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size())
        utils.darken(self.background, 100)

    def _createMenu(self):
        self.menu = Menu('Спасение хомячков', f'Игрок: {self.player}')
        self.menu.addItems([MenuItem('Рекорды', ScoresState, self.screen, self),
                            MenuItem('Играть', GameState, self.screen),
                            MenuItem('Выход', utils.returnValue, None)])

    def run(self):
        self.screen.blit(self.background, (0, 0))
        self.menu.draw(self.screen)
        if self.modal != None:
            self.modal.draw(self.screen)

    def keypressed(self, key, unicode):
        newState = self
        if self.modal != None:
            back, result = self.modal.keypressed(key, unicode)
            if back:
                self.modal = None
                if result != None:
                    self.player = result
                    self.menu.changeSubtitle(f'Игрок: {self.player}')
                    ConfigUtils().setPlayer(self.player, game=1)
        else:
            if key == pygame.K_ESCAPE:
                newState = None
            elif key == pygame.K_LEFT:
                self.menu.choosePrevious()
            elif key == pygame.K_RIGHT:
                self.menu.chooseNext()
            elif key == pygame.K_RETURN:
                return self.menu.execute()
            elif key == pygame.K_UP:
                self.modal = ModalWindow(
                    'Введите имя:', ModalType.PROMPT, self.player, 'Lines')
        return newState
