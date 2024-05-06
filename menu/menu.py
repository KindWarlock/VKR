from menu.menu_item import MenuItem


class Menu:
    def __init__(self, name, parent=None, menuChangeFunc=None, pos=None):
        self.name = name
        self.parent = parent

        if pos == None:
            self.pos = (30, 100)
        else:
            self.pos = pos

        self.items = []
        self.chosenItem = 0
        if parent != None:
            self._addBackButton(menuChangeFunc)

    def addItems(self, items):
        # Чтобы кнопка "Назад" всегда была в конце
        if self.parent != None and len(self.items) > 0:
            self.items = self.items[:-1] + items + self.items[-1:]
            return
        self.items += items

    def _addBackButton(self, menuChangeFunc):
        self.addItems([MenuItem('Назад', None, menuChangeFunc, self.parent)])

    def draw(self, surf):
        offsetY = 0
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
