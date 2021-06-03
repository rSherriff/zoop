from sections.section import Section

import numpy as np
import xp_loader
import gzip
import tile_types
import os.path
from application_path import get_app_path
from ui.menu_ui import MenuUI

class Pitch(Section):
    def __init__(self, engine, x, y, width, height):
        super().__init__(engine, x, y, width, height)
        self.tiles = np.full((self.width, self.height),fill_value=tile_types.background_tile, order="F")

        x = 7
        y = 4
        width, height = 4, 4
        for i in range(x, x+ width):
            for j in range(y, y + height):
                self.tiles[i,j] = tile_types.playground_tile
               
        #self.ui = MenuUI(self, x, y, self.tiles["graphic"])