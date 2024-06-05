import pygame

from utils.config_utils import ConfigUtils
from games.lines.states.menu_state import MenuState
from games.lines.states.game_state import GameState
from games.lines.states.gameover_state import GameoverState
from games.lines.states.pause_state import PauseState


class LinesGame:
    FPS = ConfigUtils().getScreenParams()[2]

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.state = MenuState(self.screen)

    @property
    def isRunning(self):
        return isinstance(self.state, GameState)

    @property
    def isMenu(self):
        return isinstance(self.state, MenuState) or isinstance(self.state, GameoverState) or isinstance(self.state, PauseState)

    def run(self):
        if self.state == None:
            pygame.time.set_timer(GameState.timerEvent, 0)
            pygame.time.set_timer(GameState.generationEvent, 0)
            return True
        self.screen.fill((255, 255, 255))
        self.state.run()

        self.clock.tick(self.FPS)

    def handleEvent(self, event):
        result = self.state.handleEvent(event)

        # Вышло время
        if self.isRunning and result != None:
            self.state = GameoverState(self.screen, result)

    def keypressed(self, key, unicode):
        result = self.state.keypressed(key, unicode)
        self.state = result

    def delegateToState(self, func, *args):
        method = getattr(self.state, func)
        return method(*args)
