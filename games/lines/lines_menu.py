from utils.config_utils import ConfigUtils
from utils import utils

from utils.menu_base import MenuItemBase, MenuBase
import pygame


class MenuItem(MenuItemBase):
    def __init__(self, name, func, *args):
        super().__init__(name, func, *args)
        imgPath = utils.getImgDir()
        self.img = utils.getImg(imgPath, 'lines_button.png')
        scaleFactor = 8
        self.img = pygame.transform.scale(self.img, (self.img.get_width(
        ) // scaleFactor, self.img.get_height() // scaleFactor))

        self.imgOff = utils.getImg(imgPath, 'lines_button_not.png')
        scaleFactor = 8
        self.imgOff = pygame.transform.scale(self.imgOff, (self.imgOff.get_width(
        ) // scaleFactor, self.imgOff.get_height() // scaleFactor))

        colorScheme = ConfigUtils().getColorScheme('Lines')
        self.color = colorScheme['Text']['Dark']

    def draw(self, surf, pos):
        if not self.chosen:
            img = self.imgOff.copy()
        else:
            img = self.img.copy()

        center = utils.getCenter(img)
        textRect = self.nameR.get_rect(center=(center[0] - 20, center[1]))

        img.blit(self.nameR, textRect)
        if not self.chosen:
            img = self.lowerSaturation(img)

        surf.blit(img, pos)

    def _renderName(self):
        self.nameR = self.font.render(self.name, True, self.color)


class Menu(MenuBase):
    def __init__(self, title, subtitle=None):
        super().__init__(title)
        self.subtitle = subtitle

        self.colorScheme = ConfigUtils().getColorScheme('Lines')

        self._renderTitle()
        self.chosenItem = 1

    def changeSubtitle(self, newSubtitle):
        self.subtitle = newSubtitle
        self._renderTitle()

    def _renderTitle(self):
        fontFamilyTitle, fontSizeTitle = ConfigUtils().getFont(type='title', size='l')
        fontTitle = pygame.font.Font(fontFamilyTitle, fontSizeTitle)

        shadow = fontTitle.render(
            self.title, True, self.colorScheme['Shadows'])
        main = fontTitle.render(self.title, True, self.colorScheme['Accent'])
        self.titleR = shadow
        self.titleR.blit(main, (3, 0))

        if self.subtitle != None:
            fontFamilySubtitle, fontSizeSubtitle = ConfigUtils().getFont(type='title', size='m')
            fontSubtitle = pygame.font.Font(
                fontFamilySubtitle, fontSizeSubtitle)
            self.subtitleR = fontSubtitle.render(
                self.subtitle, False, self.colorScheme['Text']['Normal'])

    def _drawTitle(self, surf):
        y = surf.get_height() / 4

        titleRect = self.titleR.get_rect(center=utils.getCenter(surf))
        titleRect.y = y
        surf.blit(self.titleR, titleRect)

        if self.subtitle != None:
            y += self.titleR.get_height() + 25
            subtitleRect = self.subtitleR.get_rect(
                center=utils.getCenter(surf, y=y))

            surf.blit(self.subtitleR, subtitleRect)

    def draw(self, surf):
        self._drawTitle(surf)
        itemsX = self._alignItems(surf)
        for i, item in enumerate(self.items):
            x = itemsX[i]
            y = surf.get_height() * 0.75  # Нижняя четверть
            item.draw(surf, (x, y))

    def _alignItems(self, surf):
        cnt = len(self.items) + 1
        textLen = 0
        for item in self.items:
            textLen += item.getWidth()

        spaces = surf.get_width() - textLen
        gap = spaces / cnt

        currX = gap
        itemsX = [gap]

        for item in self.items:
            currX += item.getWidth() + gap
            itemsX.append(currX)

        return itemsX
