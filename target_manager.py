

import random
from os import spawnl

from playsound import playsound

from actions.actions import GameOver, UpdateScore
from application_path import get_app_path
from entities.target import Target
from utils.color import get_random_color
from utils.direction import Direction


class TargetType:
    def __init__(self, char, color):
        self.char = char
        self.color = color

class TargetSpawn:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


class TargetManager:
    def __init__(self, engine):

        self.engine = engine

        self.target_types = []
        self.target_types.append(TargetType('#', (255,0,0)))
        self.target_types.append(TargetType('@', (0,255,0)))
        self.target_types.append(TargetType('&', (0,0,255)))
        self.target_types.append(TargetType('!', (255,255,0)))

        self.target_spawns = []

        for i in range(0,4):
            self.target_spawns.append(TargetSpawn(0,4+i,Direction.RIGHT))
            self.target_spawns.append(TargetSpawn(17,4+i, Direction.LEFT))
            self.target_spawns.append(TargetSpawn(7+i,0, Direction.DOWN))
            self.target_spawns.append(TargetSpawn(7+i,11, Direction.UP))

    def get_random_target_type(self):
        return self.target_types[random.randrange(0, len(self.target_types))]

    def get_random_target_spawn(self):
        return self.target_spawns[random.randrange(0, len(self.target_spawns))]

    def spawn_target(self):
        type = self.get_random_target_type()
        spawn = self.get_random_target_spawn()

        if spawn.direction == Direction.UP:
            entities_to_move = []
            for entity in self.engine.entities:
                if isinstance(entity, Target):
                    for i in range(0,4):
                        if (entity.x == spawn.x and entity.y == spawn.y - i) and i == 3:
                            entities_to_move.append(entity)
                            GameOver(self.engine).perform()
                        elif entity.x == spawn.x and entity.y == spawn.y - i:
                            entities_to_move.append(entity)

            for entity in entities_to_move:
                entity.move(0,-1)

        elif spawn.direction == Direction.DOWN:
            entities_to_move = []
            for entity in self.engine.entities:
                if isinstance(entity, Target):
                    for i in range(0,4):
                        if (entity.x == spawn.x and entity.y == spawn.y + i) and i == 3:
                            entities_to_move.append(entity)
                            GameOver(self.engine).perform()
                        elif entity.x == spawn.x and entity.y == spawn.y + i:
                            entities_to_move.append(entity)

            for entity in entities_to_move:
                entity.move(0,1)

        elif spawn.direction == Direction.LEFT:
            entities_to_move = []
            for entity in self.engine.entities:
                if isinstance(entity, Target):
                    for i in range(0,7):
                        if (entity.x == spawn.x - i and entity.y == spawn.y) and i ==6:
                            entities_to_move.append(entity)
                            GameOver(self.engine).perform()
                        elif entity.x == spawn.x - i and entity.y == spawn.y:
                            entities_to_move.append(entity)

            for entity in entities_to_move:
                entity.move(-1,0)

        elif spawn.direction == Direction.RIGHT:
            entities_to_move = []
            for entity in self.engine.entities:
                if isinstance(entity, Target):
                    for i in range(0,7):
                        if (entity.x == spawn.x + i and entity.y == spawn.y) and i ==6:
                            entities_to_move.append(entity)
                            GameOver(self.engine).perform()
                        elif entity.x == spawn.x + i and entity.y == spawn.y:
                            entities_to_move.append(entity)

            for entity in entities_to_move:
                entity.move(1,0)

        playsound(get_app_path() + "/sounds/beep.wav", False)
        self.engine.entities.append(Target(self.engine, spawn.x, spawn.y, type.char, type.color))

    def place_target(self, color, point):
        char = '?'
        for type in  self.target_types:
            if color == type.color:
                char = type.char
                break

        self.engine.entities.append(Target(self.engine, point[0], point[1], char, color))

    def target_hit(self, point, direction, color):
        entities_to_remove = []
        chain_broken = False
        x_offset = point[0]
        y_offset = point[1]
        scoring_hit = True

        if direction == Direction.UP:
            while y_offset >= 0 and not chain_broken:
                for entity in self.engine.entities:
                    if isinstance(entity, Target):
                        if entity.x == point[0] and entity.y == y_offset:
                            if entity.color == color:
                                entities_to_remove.append(entity)
                            else:
                                if y_offset == point[1]:
                                    entities_to_remove.append(entity)
                                    scoring_hit = False
                                chain_broken = True
                y_offset -= 1

        elif direction == Direction.DOWN:
            while y_offset <= 11 and not chain_broken:
                for entity in self.engine.entities:
                    if isinstance(entity, Target):
                        if entity.x == point[0] and entity.y == y_offset:
                            if entity.color == color:
                                entities_to_remove.append(entity)
                            else:
                                if y_offset == point[1]:
                                    entities_to_remove.append(entity)
                                    scoring_hit = False
                                chain_broken = True
                y_offset += 1

        elif direction == Direction.LEFT:
            while x_offset >= 0 and not chain_broken:
                for entity in self.engine.entities:
                    if isinstance(entity, Target):
                        if entity.x == x_offset and entity.y == point[1]:
                            if entity.color == color:
                                entities_to_remove.append(entity)
                            else:
                                if x_offset == point[0]:
                                    entities_to_remove.append(entity)
                                    scoring_hit = False
                                chain_broken = True
                x_offset -= 1

        elif direction == Direction.RIGHT:
            while x_offset <= 17 and not chain_broken:
                for entity in self.engine.entities:
                    if isinstance(entity, Target):
                        if entity.x == x_offset and entity.y == point[1]:
                            if entity.color == color:
                                entities_to_remove.append(entity)
                            else:
                                if x_offset == point[0]:
                                    entities_to_remove.append(entity)
                                    scoring_hit = False
                                chain_broken = True
                x_offset += 1

        score = 0
        if scoring_hit:
            if len(entities_to_remove) == 1:
                score = 100
            if len(entities_to_remove) == 2:
                score = 500
            if len(entities_to_remove) == 3:
                score = 1000
            if len(entities_to_remove) == 4:
                score = 2000
            if len(entities_to_remove) == 5:
                score = 3000
            if len(entities_to_remove) == 6:
                score = 4000

        UpdateScore(self.engine, score).perform()

        for entity in entities_to_remove:
            self.engine.remove_entity(entity)

    def test_spawns(self):
        for spawn in self.target_spawns:
            self.engine.entities.append(Target(self.engine, spawn.x, spawn.y,'#', (255,0,0)))

    def setup_game(self):
        number_to_spawn = 6
        number_of_doubles = 2
        potential_spawns = [([0,4], Direction.LEFT),([0,5], Direction.LEFT),([0,6], Direction.LEFT),([0,7], Direction.LEFT),
                            ([17,4], Direction.RIGHT),([17,5], Direction.RIGHT),([17,6], Direction.RIGHT),([17,7], Direction.RIGHT),
                            ([7,0], Direction.DOWN),([8,0], Direction.DOWN),([9,0], Direction.DOWN),([10,0], Direction.DOWN),
                            ([7,11], Direction.UP),([8,11], Direction.UP),([9,11], Direction.UP),([10,11], Direction.UP)]
        while(number_to_spawn > 0):
            color = get_random_color()
            spawn = potential_spawns[random.randrange(0, len(potential_spawns))]
            if number_to_spawn <= number_of_doubles:
                self.place_target(color, spawn[0])  
                if spawn[1] == Direction.LEFT:
                    self.place_target(color, [spawn[0][0] + 1, spawn[0][1]])
                if spawn[1] == Direction.RIGHT:
                    self.place_target(color, [spawn[0][0] - 1, spawn[0][1]])
                if spawn[1] == Direction.DOWN:
                    self.place_target(color, [spawn[0][0], spawn[0][1] + 1])
                if spawn[1] == Direction.UP:
                    self.place_target(color, [spawn[0][0], spawn[0][1] - 1])
            else:
                self.place_target(color, spawn[0])

            potential_spawns.remove(spawn)
            number_to_spawn -= 1

