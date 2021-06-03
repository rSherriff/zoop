from __future__ import annotations
from entities.temptity import Temptity

import time
from enum import Enum, auto
from threading import Timer
from typing import TYPE_CHECKING

import numpy as np
import tcod
from playsound import playsound
from tcod.console import Console

import tile_types
from application_path import get_app_path
from effects.melt_effect import MeltWipeEffect, MeltWipeEffectType
from entities.player import Player
from entities.temptity import Temptity
from input_handlers import EventHandler, MainGameEventHandler
from sections.menu import Menu
from sections.pitch import Pitch
from target_manager import TargetManager
from utils.delta_time import DeltaTime


class GameState(Enum):
    MENU = auto()
    IN_GAME = auto()
    GAME_OVER = auto()
    COMPLETE = auto()


class Engine:
    def __init__(self, teminal_width: int, terminal_height: int):

        self.screen_width = teminal_width
        self.screen_height = terminal_height
        self.delta_time = DeltaTime()

       
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.mouse_location = (0, 0)

        self.target_manager = TargetManager(self)

        self.setup_effects()
        self.setup_sections()
        self.setup_game()

        self.state = GameState.IN_GAME
        

    def render(self, root_console: Console) -> None:
        """ Renders the game to console """
        for section_key, section_value in self.get_active_sections():
            if section_key not in self.disabled_sections:
                section_value.render(root_console)

        if self.state == GameState.IN_GAME or self.state == GameState.GAME_OVER:
            for entity in self.entities:
                root_console.print(entity.x, entity.y, entity.char, fg=entity.color)

        if self.state == GameState.IN_GAME or self.state == GameState.GAME_OVER:
            root_console.print(0, 0, str(self.score).zfill(6)[0:6], (255,255,255))
            if self.last_score != 0:
                root_console.print(2, 1, str(self.last_score).zfill(4), (255,255,255))

        if self.full_screen_effect.in_effect == True:
            self.full_screen_effect.render(root_console)
        else:
            self.full_screen_effect.set_tiles(root_console.tiles_rgb)

    def update(self):
        """ Engine update tick """
        for _, section in self.get_active_sections():
            section.update()

        self.delta_time.update_delta_time()

        self.time_since_last_tick += self.get_delta_time()

        if self.time_since_last_tick > self.tick_length and self.state == GameState.IN_GAME:
            self.target_manager.spawn_target()
            self.time_since_last_tick = 0

        for entity in self.entities:
            entity.update()

    def handle_events(self, context: tcod.context.Context):
        self.event_handler.handle_events(
            context, discard_events=self.full_screen_effect.in_effect or self.state == GameState.GAME_OVER)

    def setup_game(self):
        self.player = Player(self, 7,4)
        self.entities = []
        self.entities.append(self.player)

        self.tick_length = 1
        self.time_since_last_tick = -2
        self.score = 0
        self.last_score = 0
        self.target_manager.setup_game()

       

    def setup_effects(self): 
        self.full_screen_effect = MeltWipeEffect(self, 0, 0, self.screen_width, self.screen_height, MeltWipeEffectType.RANDOM, 100)

    def setup_sections(self):
        self.menu_sections = {}
        self.menu_sections["Menu"] = Menu(self, 0, 0, self.screen_width, self.screen_height)

        self.game_sections = {}
        self.game_sections["Pitch"] = Pitch(self,0, 0, self.screen_width, self.screen_height)

        self.completion_sections = {}

        self.disabled_sections = []

    def get_active_sections(self):
        if self.state == GameState.MENU:
            return self.menu_sections.items()
        elif self.state == GameState.IN_GAME or self.state == GameState.GAME_OVER:
            return self.game_sections.items()
        elif self.state == GameState.COMPLETE:
            return self.completion_sections.items()

    def close_menu(self):
        print("Closing menu!")
        self.state = GameState.IN_GAME
        self.setup_game()
        self.full_screen_effect.start()

    def open_menu(self):
        self.state = GameState.MENU
        self.full_screen_effect.start()

    def game_over(self):
        self.state = GameState.GAME_OVER
        Timer(3,self.open_menu).start()

    def complete_game(self):
        self.state = GameState.COMPLETE
        self.full_screen_effect.start()

    def show_tooltip(self, key):
        self.tooltips[key].invisible = False

    def hide_tooltip(self, key):
        self.tooltips[key].invisible = True

    def get_delta_time(self):
        return self.delta_time.get_delta_time()

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def update_score(self, score_diff):
        self.score += score_diff
        self.last_score = score_diff

    def spawn_temp_entity(self, point, char, colour, lifespan):
        self.entities.append(Temptity(self, point[0], point[1], char, colour, lifespan))


