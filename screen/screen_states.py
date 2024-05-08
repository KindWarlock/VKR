from enum import Enum


class State(Enum):
    MENU = 0
    CAMERA_CALIBRATION = 1
    SURFACE_CALIBRATION = 2
    COLOR_CALIBRATION = 3
    GAME_SHOOTER = 4
    GAME_LINES = 5
