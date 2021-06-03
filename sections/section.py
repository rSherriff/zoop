import numpy as np
import tile_types

class Section:
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        self.engine = engine

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.tiles =  np.full((width, height), fill_value=tile_types.background_tile, order="F")
        self.ui = None

        self.invisible = False

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

            if self.ui is not None:
                self.ui.render(console)

    def update(self):
        pass