from menu.menu_item import MenuItem
from utils.config_utils import ConfigUtils
import pygame


class Menu:
    def __init__(self, name, parent=None, menuChangeFunc=None, pos=None):
        self.colorScheme = ConfigUtils().getColorScheme('Menu')
        self.name = name
        self.parent = parent
        self._renderTitle()
        if pos == None:
            self.pos = (30, 50)
        else:
            self.pos = pos

        self.items = []
        self.chosenItem = 0
        if parent != None:
            self._addBackButton(menuChangeFunc)

    def _renderTitle(self):
        fontFamily, fontSize = ConfigUtils().getFont('title', size='l')
        font = pygame.font.Font(fontFamily, fontSize)
        self.nameR = font.render(self.name, True, self.colorScheme['Accent'])

    def addItems(self, items):
        # Чтобы кнопка "Назад" всегда была в конце
        if self.parent != None and len(self.items) > 0:
            self.items = self.items[:-1] + items + self.items[-1:]
            return
        self.items += items

    def _addBackButton(self, menuChangeFunc):
        self.addItems([MenuItem('Назад', None, menuChangeFunc, self.parent)])

    def draw(self, surf):
        self._drawTitle(surf)
        self._drawItems(surf)

    def _drawTitle(self, surf):
        surf.blit(self.nameR, self.pos)

    def _drawItems(self, surf):
        offsetY = self.nameR.get_height() + 20
        for idx, item in enumerate(self.items):
            item.draw(surf, self.pos[0], self.pos[1] +
                      offsetY, self.chosenItem == idx)
            offsetY += item.getHeight(self.chosenItem == idx) + 15

    def chooseNext(self):
        if self.chosenItem < len(self.items) - 1:
            self.chosenItem += 1

    def choosePrevious(self):
        if self.chosenItem > 0:
            self.chosenItem -= 1

    def execute(self):
        return self.items[self.chosenItem].execute()
