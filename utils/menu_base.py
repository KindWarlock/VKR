from utils.config_utils import ConfigUtils
import pygame
import utils.utils as utils


class MenuItemBase(pygame.sprite.Sprite):
    def __init__(self, name, func, *args, colors=[(0, 0, 0), (100, 100, 100)]):
        super().__init__()
        self.chosen = False

        self.img = None
        self.imgOff = None

        self.color = colors[0]
        self.colorOff = colors[1]

        fontFamilyMain, fontSizeMain = ConfigUtils().getFont()
        self.font = pygame.font.Font(fontFamilyMain, fontSizeMain)

        self.name = name
        self._renderName()

        self.func = func
        self.args = args

    def execute(self):
        return self.func(*self.args)

    def draw(self, surf, pos, textCenter=None):
        if self.img == None:
            surf.blit(self.nameR, pos)
            return

        if not self.chosen:
            img = self.imgOff.copy()
        else:
            img = self.img.copy()

        if textCenter == None:
            center = utils.getCenter(img)
        else:
            center = textCenter
        textRect = self.nameR.get_rect(center=(center[0], center[1]))

        img.blit(self.nameR, textRect)
        if not self.chosen:
            img = self.lowerSaturation(img)
        surf.blit(img, pos)

    def toggleChosen(self):
        self.chosen = not self.chosen
        # if self.img == None:
        self._renderName()

    def _renderName(self):
        if self.chosen:
            self.nameR = self.font.render(self.name, True, self.color)
        else:
            self.nameR = self.font.render(self.name, True, self.colorOff)

    def lowerSaturation(self, img):
        surf = pygame.Surface(img.get_size()).convert_alpha()
        surf.fill((190, 190, 190))
        img.blit(surf, (0, 0), special_flags=pygame.BLEND_MULT)
        return img

    def getWidth(self):
        if self.img == None:
            return self.nameR.get_width()
        return self.img.get_width()

    def getHeight(self):
        if self.img == None:
            return self.nameR.get_height()
        return self.img.get_height()


class MenuBase:
    def __init__(self, title):
        self.title = title

        self.items = []
        self.chosenItem = 0

    def addItems(self, items):
        self.items += items
        if len(items) > self.chosenItem:
            items[self.chosenItem].toggleChosen()

    def draw(self):
        ...

    def _drawTitle(self):
        ...

    def _renderTitle(self):
        ...

    def chooseNext(self):
        if self.chosenItem < len(self.items) - 1:
            oldChosen = self.chosenItem
            self.chosenItem += 1
            self._changeItem(oldChosen, self.chosenItem)

    def choosePrevious(self):
        if self.chosenItem > 0:
            oldChosen = self.chosenItem
            self.chosenItem -= 1
            self._changeItem(oldChosen, self.chosenItem)

    def _changeItem(self, old, new):
        self.items[old].toggleChosen()
        self.items[new].toggleChosen()

    def execute(self):
        return self.items[self.chosenItem].execute()

    def alignAround(self, surf):
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
