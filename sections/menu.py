from sections.section import Section

import numpy as np
import xp_loader
import gzip
import tile_types
import os.path
from application_path import get_app_path
from ui.menu_ui import MenuUI

xp_filepath = get_app_path() + '/images/menu.xp'


class Menu(Section):
    def __init__(self, engine, x, y, width, height):
        super().__init__(engine, x, y, width, height)

        xp_file = gzip.open(xp_filepath)
        raw_data = xp_file.read()
        xp_file.close()

        xp_data = xp_loader.load_xp_string(raw_data)

        self.tiles = np.full((self.width, self.height),fill_value=tile_types.background_tile, order="F")

        for h in range(0, self.height):
            for w in range(0, self.width):
                self.tiles[w, h]['graphic'] = xp_data['layer_data'][0]['cells'][w][h]

        self.ui = MenuUI(self, x, y, self.tiles["graphic"])