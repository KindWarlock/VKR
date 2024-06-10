from enum import Enum
import pygame
import time

from utils.config_utils import ConfigUtils
import utils.utils as utils
from utils.menu_base import MenuBase, MenuItemBase


class ModalType(Enum):
    INFO = 0
    PROMPT = 1


class ModalWindow:
    PRINTABLE_SYMBOLS = set(
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%*+,-.:;<=>@^_~ йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ')
    MAX_LEN = 7

    PADDING = (50, 30)
    INPUT_GAP = 10
    MENU_GAP = 15

    class Menu(MenuBase):
        def __init__(self, title):
            super().__init__(title)

        def draw(self, surf):
            itemsX = self.alignAround(surf)
            for i, item in enumerate(self.items):
                x = itemsX[i]
                y = surf.get_height() - \
                    ModalWindow.PADDING[1] - item.getHeight()
                item.draw(surf, (x, y))

        def getHeight(self):
            return self.items[0].getHeight()

    class MenuItem(MenuItemBase):
        ...

    def __init__(self, text, type=ModalType.INFO, defaultText='', colorScheme='Shooter'):
        self.text = text
        self.type = type
        self.input = defaultText
        self.lastBlink = time.time()
        self.blink = True

        self.colors = ConfigUtils().getColorScheme(colorScheme)
        self._createMenu()

        self._loadFont()
        self._renderText()

        self._defineRect()
        self._centerText()

    def _loadFont(self):
        fontFamily, fontSize = ConfigUtils().getFont()
        self.font = pygame.font.Font(fontFamily, fontSize)

    def _defineRect(self):
        textWidth, textHeight = self.textR.get_size()
        rectWidth, rectHeight = textWidth + \
            ModalWindow.PADDING[0] * 2, textHeight + ModalWindow.PADDING[1] * \
            2 + self.menu.getHeight() + ModalWindow.MENU_GAP
        if self.type == ModalType.PROMPT:
            rectHeight += self.INPUT_GAP + textHeight

        self.surf = pygame.surface.Surface(
            (rectWidth, rectHeight), pygame.SRCALPHA)
        self.rect = pygame.Rect(0, 0, rectWidth, rectHeight)

        screenWidth, screenHeight = ConfigUtils().getScreenParams()[:2]
        self.rect.center = screenWidth // 2, screenHeight // 2

    def _renderText(self):
        # color = (60, 119, 141)
        color = self.colors['Text']['Dark']

        self.textR = self.font.render(self.text, True, color)
        self.textRect = self.textR.get_rect()

    def _createMenu(self):
        self.menu = ModalWindow.Menu('Buttons')
        colors = [self.colors['Text']['Dark'], self.colors['Text']['Light']]
        items = [ModalWindow.MenuItem('ОК', self.confirm, colors=colors)]
        if self.type == ModalType.PROMPT:
            items.append(ModalWindow.MenuItem(
                'Отмена', self.cancel, colors=colors))

        self.menu.addItems(items)

    def _centerText(self):
        self.textRect.topleft = (
            ModalWindow.PADDING[0], ModalWindow.PADDING[1])

    def draw(self, surf):
        alpha = 220
        # colorIn = (236, 242, 232, alpha)
        # colorOut = (150, 208, 219, alpha)

        colorIn = self.colors['Shadows']
        colorOut = self.colors['Accent']
        lIn = utils.calculateLuminance(colorIn)
        lOut = utils.calculateLuminance(colorOut)

        if lIn < lOut:
            colorOut = self.colors['Shadows']
            colorIn = self.colors['Accent']
        pygame.draw.rect(self.surf, colorIn + [alpha], self.surf.get_rect())
        pygame.draw.rect(self.surf, colorOut + [alpha],
                         self.surf.get_rect(), 2)

        self.menu.draw(self.surf)
        self.surf.blit(self.textR, self.textRect)

        if self.type == ModalType.PROMPT:
            self._drawInput(self.surf)

        surf.blit(self.surf, self.rect)

    def keypressed(self, key, unicode):
        back = False
        result = None

        if unicode in self.PRINTABLE_SYMBOLS and len(self.input) < self.MAX_LEN:
            self.input += unicode
        elif key == pygame.K_BACKSPACE and len(self.input) > 0:
            self.input = self.input[:-1]
        elif key == pygame.K_LEFT:
            self.menu.choosePrevious()
        elif key == pygame.K_RIGHT:
            self.menu.chooseNext()

        elif key == pygame.K_RETURN:
            back, result = self.menu.execute()
        elif key == pygame.K_ESCAPE:
            back, result = self.cancel()

        return back, result

    def confirm(self):
        return True, self.input

    def cancel(self):
        return True, None

    def _drawInput(self, surf):
        color = self.colors['Text']['Normal']
        inputR = self.font.render(self.input, True, color)

        # Определение положения текста
        inputRect = inputR.get_rect(center=surf.get_rect().center)
        inputRect.y = self.textRect.bottom + self.INPUT_GAP

        surf.blit(inputR, inputRect)

        # Отрисовка курсора
        if self.blink:
            cursor = self.font.render('_', True, color)
            surf.blit(cursor, (inputRect.right, inputRect.y))

        # Обновление курсора
        if time.time() - self.lastBlink >= 0.75:
            self.blink = not self.blink
            self.lastBlink = time.time()
