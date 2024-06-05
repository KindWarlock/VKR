import win32gui
import win32con
import sys


import pygame

from games.shooter.game import Game as Shooter
from games.lines.game import Game as Lines
from utils.config_utils import ConfigUtils
from screen.main_menu import MainMenu
from calibration.surface import SurfaceCalibration
from calibration.cam import CameraCalibration
from calibration.color import ColorCalibration
from screen.screen_states import State


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


def createWindow():
    config = ConfigUtils()
    screenWidth, screenHeight, fps, pos = config.getScreenParams()

    screen = pygame.display.set_mode(
        (screenWidth, screenHeight), pygame.RESIZABLE)

    pygame.display.set_caption('Game')
    setGameWindowPos(pos)
    return screen, fps


def quit():
    pos = findGameWindow()
    config.setScreenParams(None, None, pos)
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def changeState(newState):
    global stateStack
    global state
    stateStack.append(state)

    state = None
    if newState == State.SURFACE_CALIBRATION:
        state = SurfaceCalibration(screen)
    elif newState == State.CAMERA_CALIBRATION:
        state = CameraCalibration(screen)
    elif newState == State.COLOR_CALIBRATION:
        state = ColorCalibration(screen)
    elif newState == State.GAME_SHOOTER:
        state = Shooter(screen)
    elif newState == State.GAME_LINES:
        state = Lines(screen)
    return state


def popState():
    global stateStack
    if len(stateStack) == 0:
        quit()
    return stateStack.pop()


pygame.init()
pygame.mixer.init()
screen, fps = createWindow()
clock = pygame.time.Clock()
config = ConfigUtils()

stateStack = []

state = MainMenu(screen)

while True:
    result = None
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            newState = state.keypressed(event.key, event.unicode)
            if newState:
                state = changeState(newState)
        elif event.type == pygame.VIDEORESIZE:
            config.setScreenParams(event.size[0], event.size[1])
        elif event.type == pygame.QUIT:
            quit()
        elif pygame.USEREVENT <= event.type < pygame.NUMEVENTS:
            state.handleEvent(event)

    back = state.run()
    if back:
        state = popState()

    pygame.display.update()
    clock.tick(fps)
