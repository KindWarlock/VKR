import pygame
import sys
import win32gui
import win32con
from enum import Enum

from utils.config_utils import ConfigUtils

from menu.menu import Menu
from menu.menu_item import MenuItem
from calibration.surface import SurfaceCalibration
from calibration.cam import CameraCalibration
from calibration.color import ColorCalibration


class States(Enum):
    MENU = 0
    CALIBRATION = 1


def changeMenu(new_menu):
    global current_menu
    current_menu = new_menu


def findGameWindow():
    name = win32gui.FindWindow(None, 'Game')
    rect = win32gui.GetWindowRect(name)
    x = rect[0]
    y = rect[1]
    return x, y


def setGameWindowPos(pos):
    name = win32gui.FindWindow(None, 'Game')
    win32gui.SetWindowPos(
        name, 0, pos[0], pos[1], 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)


def quit():
    pos = findGameWindow()
    config.setScreenParams(None, None, pos)
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def createMenus():
    main_menu = Menu('Главное')
    game_menu = Menu('Игры', main_menu, changeMenu)
    calibration_menu = Menu('Калибровка', main_menu, changeMenu)
    settings_menu = Menu('Настройки', main_menu, changeMenu)

    main_menu.addItems([MenuItem('Играть', None, print, 'Играть'),
                        MenuItem('Калибровка', None,
                                 changeMenu, calibration_menu),
                        MenuItem('Настройки', None, changeMenu, settings_menu),
                        MenuItem('Выход', None, quit)])

    game_menu.addItems([MenuItem('Шарики',
                                 'Лопните как можно больше шариков, пока не кончилось время!', print, 'Шарики'),
                        MenuItem('Линии', 'Загоните мячик в корзину, используя маркерные рисунки.', print, 'Линии')])

    calibration_menu.addItems([MenuItem('Калибровка камеры',
                                        'Удаление искажений камеры при промощи паттерна шахматной доски', calibrate, screen, returnToMenu, 1),
                               MenuItem('Калибровка поверхности', 'Определение используемой поверхности',
                                        calibrate, screen, returnToMenu, 0),
                               MenuItem('Калибровка цвета', 'Устранение ошибок при считывании цветов с камеры', calibrate, screen, returnToMenu, 2)])

    return main_menu, game_menu, calibration_menu


def calibrate(screen, backFunc, calibration_mode):
    if calibration_mode == 0:
        calib = SurfaceCalibration(screen, backFunc)
    elif calibration_mode == 1:
        calib = CameraCalibration(screen, backFunc)
    else:
        calib = ColorCalibration(screen, backFunc)
    global state
    state = States.CALIBRATION

    return calib


def returnToMenu():
    global state, calibration
    state = States.MENU
    calibration = None


pygame.init()

config = ConfigUtils()
screenWidth, screenHeight, fps, pos = config.getScreenParams()

screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption('Game')
setGameWindowPos(pos)

clock = pygame.time.Clock()

main_menu, game_menu, calibration_menu = createMenus()
current_menu = main_menu
state = States.MENU

calibration = None

while True:
    result = None
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if state == States.MENU:
                if event.key == pygame.K_DOWN:
                    current_menu.chooseNext()
                if event.key == pygame.K_UP:
                    current_menu.choosePrevious()
                if event.key == pygame.K_RETURN:
                    result = current_menu.execute()
                if event.key == pygame.K_ESCAPE:
                    if current_menu.parent == None:
                        quit()
                    changeMenu(current_menu.parent)
            else:
                calibration.keypressed(event.key)
        elif event.type == pygame.VIDEORESIZE:
            config.setScreenParams(event.size[0], event.size[1])
        elif event.type == pygame.QUIT:
            quit()

    if state == States.MENU:
        screen.fill((255, 255, 255))
        current_menu.draw(screen)
    else:
        if calibration == None:
            calibration = result
        calibration.run()

    pygame.display.update()
    clock.tick(fps)
