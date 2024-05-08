import pygame
import sys
import win32gui
import win32con
from enum import Enum

from utils.config_utils import ConfigUtils
import utils.utils as utils
from menu.menu import Menu
from menu.menu_item import MenuItem
from screen.screen_states import State


class MainMenu:
    def __init__(self, screen) -> None:
        self.screen = screen
        self._createMenus()
        self.current_menu = self.main_menu

    def changeMenu(self, new_menu):
        self.current_menu = new_menu

    def _createMenus(self):
        self.main_menu = Menu('Главное')
        self.game_menu = Menu('Игры', self.main_menu, self.changeMenu)
        self.calibration_menu = Menu(
            'Калибровка', self.main_menu, self.changeMenu)
        self.settings_menu = Menu('Настройки', self.main_menu, self.changeMenu)

        self.main_menu.addItems([MenuItem('Играть', None, self.changeMenu, self.game_menu),
                                 MenuItem('Калибровка', None,
                                          self.changeMenu, self.calibration_menu),
                                 MenuItem('Настройки', None,
                                          self.changeMenu, self.settings_menu),
                                 MenuItem('Выход', None, self.changeMenu, None)])

        self.game_menu.addItems([MenuItem('Шарики',
                                          'Лопните как можно больше шариков, пока не кончилось время!', utils.returnValue, State.GAME_SHOOTER),
                                 MenuItem('Линии', 'Загоните мячик в корзину, используя маркерные рисунки.', utils.returnValue, State.GAME_LINES)])

        self.calibration_menu.addItems([MenuItem('Калибровка камеры',
                                                 'Удаление искажений камеры при промощи паттерна шахматной доски', utils.returnValue, State.CAMERA_CALIBRATION),
                                        MenuItem(
                                            'Калибровка поверхности', 'Определение используемой поверхности', utils.returnValue, State.SURFACE_CALIBRATION),
                                        MenuItem('Калибровка цвета', 'Устранение ошибок при считывании цветов с камеры', utils.returnValue, State.COLOR_CALIBRATION)])

    def keypressed(self, key):
        if key == pygame.K_DOWN:
            self.current_menu.chooseNext()
        elif key == pygame.K_UP:
            self.current_menu.choosePrevious()
        elif key == pygame.K_RETURN:
            result = self.current_menu.execute()
            print(result)
            return result

        elif key == pygame.K_ESCAPE:
            # if self.current_menu.parent == None:
            #     quit()
            self.changeMenu(self.current_menu.parent)

    def run(self):
        self.screen.fill((255, 255, 255))

        if not self.current_menu:
            return True

        self.current_menu.draw(self.screen)
