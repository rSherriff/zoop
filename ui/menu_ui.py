from ui.ui import UI
from ui.ui import Button

from actions.actions import CloseMenu, EscapeAction

import tcod.event

class MenuUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        bd = [4, 1,10,5] #Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=CloseMenu(self.section.engine), tiles=button_tiles )
        self.add_element(one_button)

        bd = [4, 6,10,5] #Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EscapeAction(self.section.engine), tiles=button_tiles )
        self.add_element(one_button)

    def keydown(self, event: tcod.event.KeyDown):
        super().keydown(event)
        key = event.sym
        if key == tcod.event.K_RETURN or key == tcod.event.K_ESCAPE or key == tcod.event.K_KP_ENTER:
            CloseMenu(self.section.engine).perform()