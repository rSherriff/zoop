from ui.ui import UI
from ui.ui import CheckedInput, HoverTrigger

from actions.actions import OpenMenu

import tcod.event


class GeneralUI(UI):
    def __init__(self, section, x, y):
        super().__init__(section, x, y)
        self.elements = list()

    def keydown(self, event: tcod.event.KeyDown):
        super().keydown(event)
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            OpenMenu(self.section.engine).perform()
