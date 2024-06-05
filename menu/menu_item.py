import pygame as pg

from utils.config_utils import ConfigUtils
from utils.text_animation import TextAnimation
from utils.mutliline_text import MultilineText

from enum import Enum


class MenuItem:
    class ItemState(Enum):
        APPEAR = 0
        EXIST = 1
        DISAPPEAR = 2

        def next(self):
            if self.value == 2:
                MenuItem.ItemState(0)
            value = self.value + 1
            return MenuItem.ItemState(value)

        def prev(self):
            if self.value == 0:
                return
            value = self.value - 1
            return MenuItem.ItemState(value)

    def __init__(self, name, desc, func, *args):
        fontFamilyDesc, fontSizeDesc = ConfigUtils().getFont(size='s')
        self.colorScheme = ConfigUtils().getColorScheme('Menu')
        self.name = '- ' + name
        if desc != None:
            self.desc = MultilineText(desc, pg.font.Font(
                fontFamilyDesc, fontSizeDesc), self.colorScheme['Text']['Normal'], 300, TextAnimation.AnimtaionType.OPENING)
        else:
            self.desc = None

        fontFamilyMain, fontSizeMain = ConfigUtils().getFont()
        self.font = pg.font.Font(fontFamilyMain, fontSizeMain)

        self._renderName()

        self.func = func
        self.args = args

        dotWidth = self.font.render(
            '- ', True, self.colorScheme['Text']['Normal']).get_width()
        self.animations = []
        self.animation = TextAnimation(
            0.17, TextAnimation.AnimtaionType.DEFAULT, (0, 0), (dotWidth, 0))

        self.state = self.ItemState.APPEAR

    def execute(self):
        return self.func(*self.args)

    def draw(self, surf, x, y, chosen=False):
        text = self.font.render(
            self.name, True, self.colorScheme['Text']['Normal'])
        dotWidth = self.font.render(
            '- ', True, (255, 255, 255)).get_width()
        offset = dotWidth

        if chosen:
            if self.animation.state == TextAnimation.AnimationState.NONE:
                self.animation.start()
                if self.desc != None:
                    self.desc.animation.start()

            elif self.animation.isReturning():
                self.animation.reverse()
                if self.desc != None:
                    self.desc.animation.reverse()
        else:
            if self.animation.state != TextAnimation.AnimationState.NONE and not self.animation.isReturning():
                self.animation.reverse()
                if self.desc != None:
                    self.desc.animation.reverse()

        if self.animation.state != TextAnimation.AnimationState.NONE:
            offset = self._playAnimation(x, y, offset)

        area = (x - offset, 0, text.get_width() + offset, text.get_height())
        surf.blit(text, (x, y), area)
        if self.desc != None:
            self.desc.draw(surf, x+dotWidth, y+text.get_height()+2)

    def _playAnimation(self, x, y, offset):
        if self.animation.isReturning():
            offset += self.animation.getNextPos()[0]
        else:
            offset += self.animation.getNextPos()[0]

        return offset

    def getHeight(self, chosen=False):
        height = self.nameR.get_height()
        if self.desc != None:
            height += self.desc.getDrawnHeight()
        return height

    def _renderName(self, chosen=False):
        if chosen:
            self.nameR = self.font.render(
                self.name, True, self.colorScheme['Text']['Normal'])
        else:
            self.nameR = self.font.render(
                self.name, True, self.colorScheme['Text']['Dark'])

    # def _renderDescription(self):
    #     font = pg.font.Font(None, 17)
    #     lines = utils.textToLines(self.desc, font, 350)
    #     self.descR = utils.renderMultiline(lines, font, (57, 41, 92))

    # def _drawDescription(self, surf, x, y):
    #     lineHeight = self.descR[0].get_height()
    #     for idx, line in enumerate(self.descR):
    #         offsetY = (lineHeight) * idx
    #         surf.blit(line, (x, y + offsetY))
