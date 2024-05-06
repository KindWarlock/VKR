import pygame
from enum import Enum
import numpy as np
import cv2
import json

import utils.utils as utils
from utils.config_utils import ConfigUtils


class CalibrationWindow:

    class State(Enum):
        WAITING = 0
        RUNNING = 1
        END = 2

        def next(self):
            if self.value == 2:
                return
            value = self.value + 1
            return CalibrationWindow.State(value)

        def prev(self):
            if self.value == 0:
                return
            value = self.value - 1
            return CalibrationWindow.State(value)

    def __init__(self, surface, backFunc):
        self.state = self.State.WAITING
        self.surf = surface
        self.back = backFunc

        self.config = ConfigUtils()
        self.cap = None

    def _renderTitle(self, text):
        fontFamily = self.config.getFonts()[0]
        font = pygame.font.Font(fontFamily, 32)
        title = font.render(text, True, (57, 41, 92))
        y = self.surf.get_size()[1] // 2 - 60
        line_rect = title.get_rect(
            center=utils.getCenter(self.surf, y=y))
        self.surf.blit(title, line_rect)

    def _displayText(self, text):
        fontFamily = self.config.getFonts()[1]
        font = pygame.font.Font(fontFamily, 24)

        textLines = utils.textToLines(text, font, 400)
        lines = utils.renderMultiline(textLines, font, (57, 41, 92))

        y = self.surf.get_size()[1] // 2
        for line in lines:
            line_rect = line.get_rect(
                center=utils.getCenter(self.surf, y=y))
            y += line_rect.height
            self.surf.blit(line, line_rect)

    def _displayTemplate(self, title, text):
        self.surf.fill((255, 255, 255))
        self._renderTitle(title)
        self._displayText(text)

    def _displayWaiting(self):
        ...

    def _displayRunning(self):
        ...

    def _displayEnd(self):
        ...

    def _displayRunningCv(self):
        ...

    def _displayEndCv(self):
        ...

    def _calibToConfig(self):
        ...

    def keypressed(self, key):
        if key == pygame.K_RETURN:
            if self.state == self.State.RUNNING:
                return
            self.state = self.state.next()
        elif key == pygame.K_r and self.state == self.State.END:
            self.state = self.state.prev()
        elif key == pygame.K_ESCAPE and self.state != self.State.END:
            self.state = self.state.prev()

    def run(self):
        if self.state == self.State.WAITING:
            self._displayWaiting()
        elif self.state == self.State.RUNNING:
            self._displayRunning()
            self._displayRunningCv()
        else:
            self._displayEnd()
            self._displayEndCv()
