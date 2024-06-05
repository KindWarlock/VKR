class BaseState:
    def __init__(self, screen):
        ...

    def run(self):
        ...

    def keypressed(self, key, unicode):
        ...

    def handleEvent(self, event):
        return
