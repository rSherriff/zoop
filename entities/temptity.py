from entities.entity import Entity
from typing import Tuple
from actions.actions import DeleteEntity
import tcod.event

class Temptity(Entity):
    def __init__(self, engine, x: int, y: int, char, color, lifespan):
        super().__init__(engine, x, y, char, color)
        self.lifespan = lifespan
        self.time_alive = 0

    def update(self):
        self.time_alive += self.engine.get_delta_time()

        if self.time_alive > self.lifespan:
            DeleteEntity(self.engine, self).perform()
