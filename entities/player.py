
from typing import Tuple

import tcod.event
from actions.actions import HitTarget, SpawnTempEntity
from utils.direction import Direction
from utils.color import get_random_color

from entities.entity import Entity
from entities.target import Target


class Player(Entity):
    def __init__(self, engine, x: int, y: int):
        self.direction = Direction.LEFT
        super().__init__(engine, x, y, chr(250), get_random_color())
        self.update_direction_char()
        

    def keydown(self, key):  
        dx,dy = 0,0 

        if key == tcod.event.K_UP or key == tcod.event.K_DOWN or key == tcod.event.K_LEFT or key == tcod.event.K_RIGHT:
            if key == tcod.event.K_UP:
                dx=0
                dy=-1
                self.direction = Direction.UP
            elif key == tcod.event.K_DOWN:
                dx=0
                dy=1
                self.direction = Direction.DOWN
            elif key == tcod.event.K_LEFT:
                dx=-1
                dy=0
                self.direction = Direction.LEFT
            elif key == tcod.event.K_RIGHT:
                dx=1
                dy=0
                self.direction = Direction.RIGHT

            dest_x = self.x + dx
            dest_y = self.y + dy

            for _, section in self.engine.get_active_sections():
                if section.tiles["walkable"][dest_x, dest_y]:
                    self.move(dx, dy)

        
        self.update_direction_char()

        if key == tcod.event.K_SPACE:
            shot_travel_points = []
            target = False
            if self.direction == Direction.UP:
                offset = self.y - 1
                target_found = False
                while not target_found and offset >= 0:
                    for entity in self.engine.entities:
                        if isinstance(entity, Target):
                            shot_travel_points.append([self.x, offset])
                            if (entity.x == self.x and entity.y == offset):
                                target_found = True
                                target = entity
                                break    
                    offset -= 1
            elif self.direction == Direction.DOWN:
                offset = self.y + 1
                target_found = False
                while not target_found and offset <= 11:
                    for entity in self.engine.entities:
                        if isinstance(entity, Target):
                            shot_travel_points.append([self.x, offset])
                            if (entity.x == self.x and entity.y == offset):
                                target_found = True
                                target = entity
                                break    
                    offset += 1
            elif self.direction == Direction.LEFT:
                offset = self.x - 1
                target_found = False
                while not target_found and offset >= 0:
                    for entity in self.engine.entities:
                        if isinstance(entity, Target):
                            shot_travel_points.append([offset, self.y])
                            if (entity.x == offset and entity.y == self.y):
                                target_found = True
                                target = entity
                                break    
                    offset -=1 
            elif self.direction == Direction.RIGHT:
                offset = self.x + 1
                target_found = False
                while not target_found and offset <= 17:
                    for entity in self.engine.entities:
                        if isinstance(entity, Target):
                            shot_travel_points.append([offset, self.y])
                            if (entity.x == offset and entity.y == self.y):
                                target_found = True
                                target = entity
                                break    
                    offset += 1

            if target:
                shot_char = "-"
                if self.direction == Direction.UP:
                    shot_char = '|'
                elif self.direction == Direction.DOWN:
                    shot_char = '|'
                elif self.direction == Direction.LEFT:
                    shot_char = "-"
                elif self.direction == Direction.RIGHT:
                    shot_char = "-"

                for point in shot_travel_points:
                    SpawnTempEntity(self.engine, point, shot_char, self.color, 0.1).perform()

                HitTarget(self.engine, [entity.x, entity.y], self.color, target, self.direction).perform()


    def update_direction_char(self):
        if self.direction == Direction.UP:
            self.char = chr(250)
        elif self.direction == Direction.DOWN:
            self.char = chr(237)
        elif self.direction == Direction.LEFT:
            self.char = chr(243)
        elif self.direction == Direction.RIGHT:
            self.char = chr(225)
