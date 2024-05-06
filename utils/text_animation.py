import pygame
from enum import Enum
import numpy as np
import time

import utils.utils as utils


class TextAnimation:

    class AnimtaionType(Enum):
        DEFAULT = 0
        OPENING = 1

    class Direction(Enum):
        LEFT = 0
        RIGHT = 1
        UP = 2
        DOWN = 3

    class AnimationState(Enum):
        NONE = 0
        STARTED = 1
        MIDDLE = 2
        REVERSED = 3
        ENDED = 4

    def __init__(self, duration, animation_type, startPos, endPos):
        self.type = animation_type
        self.fullDuration = duration
        self.duration = duration

        self.startPos = np.array(startPos)
        self.endPos = np.array(endPos)
        self.pos = np.array(startPos)

        self.velocity = (self.endPos - self.startPos) / \
            self.duration / utils.getScreenParams()[2]
        self.state = self.AnimationState.NONE

    def start(self):
        self.startTime = time.time()
        self.state = self.AnimationState.STARTED

    def getNextPos(self):
        if self.state == TextAnimation.AnimationState.NONE:
            return
        if not self.isChanging():
            return self.endPos
        if time.time() - self.startTime >= self.duration:
            if self.state == TextAnimation.AnimationState.STARTED:
                self.state = TextAnimation.AnimationState.MIDDLE
            else:
                self.state = TextAnimation.AnimationState.ENDED
            self.pos = self.endPos
            return self.pos

        pos = self.pos
        self.pos = self.pos + self.velocity
        return pos.astype('int32')

    def reverse(self):
        self.velocity *= -1

        tempPos = self.endPos
        self.endPos = self.startPos
        self.startPos = tempPos
        if self.isReturning():
            self.state = self.AnimationState.STARTED
        else:
            self.state = self.AnimationState.REVERSED

        if time.time() - self.startTime < self.duration:
            self.duration = time.time() - self.startTime
        else:
            self.duration = self.fullDuration
        self.startTime = time.time()

    def isChanging(self):
        return self.state == self.AnimationState.REVERSED or self.state == self.AnimationState.STARTED

    def isReturning(self):
        return self.state == self.AnimationState.REVERSED or self.state == self.AnimationState.ENDED
