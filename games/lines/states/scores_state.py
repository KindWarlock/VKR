import pygame

from games.shooter.states.base_state import BaseState
from utils.config_utils import ConfigUtils
from utils.database import SqliteDB
import utils.utils as utils


class ScoresState(BaseState):
    def __init__(self, screen, retState):
        self.screen = screen
        self.player = ConfigUtils().getPlayer(game=1)
        self.retState = retState

        self._renderTitle()

        self._loadItems()
        self._renderItems()

        self._renderBack()

        imgDir = utils.getImgDir()
        self.background = utils.getImg(imgDir, 'bg_lines.jpg')
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size())
        utils.darken(self.background, 30)

    def run(self):
        self.screen.blit(self.background, (0, 0))
        self._drawTitle()
        self._drawItems()
        self._drawBack()

    def keypressed(self, key, unicode):
        newState = self
        if key == pygame.K_ESCAPE:
            newState = self.retState
        return newState

    def _renderTitle(self):
        fontFamily, fontSize = ConfigUtils().getFont('title')
        font = pygame.font.Font(fontFamily, fontSize)
        self.titleR = font.render('Рекорды', True, (0, 0, 0))

    def _renderItems(self):
        fontFamily, fontSize = ConfigUtils().getFont()
        font = pygame.font.Font(fontFamily, fontSize)

        self.itemsR = []

        playerInTop = False
        for item in self.items:
            idx = item[0] + 1
            name = item[1][0]
            score = item[1][1]
            if name == self.player and idx < len(self.items) - 1:
                playerInTop = True
            elif name == self.player and playerInTop:
                break
            text = f'{idx}.{name} : {score}'
            itemR = font.render(text, True, (0, 0, 0))
            self.itemsR.append(itemR)

        if not playerInTop:
            dots = font.render('...', True, (0, 0, 0))
            self.itemsR.insert(-1, dots)

    def _renderBack(self):
        fontFamily, fontSize = ConfigUtils().getFont()
        font = pygame.font.Font(fontFamily, fontSize)

        self.backR = font.render('Назад', True, (0, 0, 0))

    def _loadItems(self):
        self.items = SqliteDB('Lines').retrieveScore(self.player, limit=3)
        print(self.items)

    def _drawItems(self):
        margin = 10
        y = self.screen.get_height() // 4 + self.titleR.get_height() + margin

        for item in self.itemsR:
            itemRect = item.get_rect(center=utils.getCenter(self.screen, y=y))
            self.screen.blit(item, itemRect)
            y += item.get_height() + 5

    def _drawTitle(self):
        y = self.screen.get_height() // 4
        titleRect = self.titleR.get_rect(
            center=utils.getCenter(self.screen, y=y))
        self.screen.blit(self.titleR, titleRect)

    def _drawBack(self):
        y = self.screen.get_height() * 0.9
        x = self.screen.get_height() * 0.1

        self.screen.blit(self.backR, (x, y))
