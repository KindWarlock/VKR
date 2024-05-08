# from games.lines.game import Game, GameState
import cProfile
import pstats
import win32gui
import win32con
import sys

import numpy as np
import cv2

import pygame

from games.shooter.game import Game as Shooter
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
    # stateStack.append(state)
    return state


def popState():
    global stateStack
    if len(stateStack) == 0:
        quit()
    return stateStack.pop()


pygame.init()
screen, fps = createWindow()
clock = pygame.time.Clock()
config = ConfigUtils()

stateStack = []

state = MainMenu(screen)

while True:
    result = None
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            newState = state.keypressed(event.key)
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

    # state = State.MENU

    # def main():
    #     state = State.ARUCO
    #     aruco_utils, markers_image = game_cv.get_calibration_aruco()
    #     warp_matrix = []

    #     game = Game()

    #     cap = game_cv.open_cam()

    #     def get_hsv(event, x, y, flags, param):
    #         if event == cv2.EVENT_LBUTTONDOWN:
    #             hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #             print(hsv[y-5:y+5, x-5:x+5], x, y)

    #     cv2.setMouseCallback('Warped', get_hsv)

    #     while cap.isOpened():
    #         # Game stuff
    #         if game.state == GameState.PAUSE:
    #             return

    #         # CV stuff
    #         ret, frame = cap.read()
    #         if ret:
    #             # frame = cv2.undistort(frame, config.mtx, config.dist, None)

    #             if state == State.ARUCO:
    #                 cv2.imshow('Cam', frame)
    #                 warp_matrix = game_cv.get_warp_matrix(
    #                     aruco_utils, frame, markers_image)
    #                 if warp_matrix is not None:
    #                     state = State.GAME

    #             else:
    #                 cv2.imshow('Before color', frame)

    #                 frame = game_cv.colorCorrection(frame)
    #                 cv2.imshow('After color', frame)
    #                 frame, contours, planets = game_cv.process(frame, warp_matrix)
    #                 cv2.imshow('Before color', frame)

    #                 frame = game_cv.colorCorrection(frame)
    #                 cv2.imshow('After color', frame)
    #                 for c in contours:
    #                     game.add_contour(c)
    #                 # if planets is not None:
    #                 planets_to_remove = game_cv.check_planets(frame, game.planets)
    #                 game.remove_planets(planets_to_remove)
    #                 if planets is not None and len(planets) > len(game.planets):
    #                     for p in planets:
    #                         # print(p)
    #                         game.add_attractor([p[0], p[1]], p[2])

    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 break
    #         if state == State.GAME:
    #             game.run()
    #             cv2.imshow('Display', game_cv.pg_to_cv2(game.screen))

    # if __name__ == "__main__":
    #     doprof = 0
    #     if not doprof:
    #         main()
    #     else:
    #         prof = cProfile.run("main()", "profile.prof")
    #         stats = pstats.Stats("profile.prof")
    #         stats.strip_dirs()
    #         stats.sort_stats("cumulative", "time", "calls")
    #         stats.print_stats(30)
