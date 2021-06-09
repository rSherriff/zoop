from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from entities.entity import Entity

if TYPE_CHECKING:
    from engine import Engine


class Action:
    def __init__(self, engine) -> None:
        super().__init__()
        self.engine = engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        self.engine.quit()
        
class CloseMenu(Action):
    def perform(self) -> None:
        self.engine.close_menu()

class OpenMenu(Action):
    def perform(self) -> None:
        self.engine.open_menu()

class ShowTooltip(Action):
    def __init__(self, engine, tooltip_key: str) -> None:
        super().__init__(engine)
        self.tooltip_key = tooltip_key

    def perform(self):
        self.engine.show_tooltip(self.tooltip_key)

class HideTooltip(Action):
    def __init__(self, engine, tooltip_key: str) -> None:
        super().__init__(engine)
        self.tooltip_key = tooltip_key

    def perform(self):
        self.engine.hide_tooltip(self.tooltip_key)

class HitTarget(Action):
    def __init__(self, engine, point, player_color, target, player_direction) -> None:
        super().__init__(engine)
        self.point = point
        self.player_color = player_color
        self.target = target
        self.player_direction = player_direction

    def perform(self):
        self.engine.target_manager.target_hit(self.point, self.player_direction, self.player_color)
        if self.player_color != self.target.color:
            self.engine.player.color = self.target.color
            self.engine.target_manager.place_target(self.player_color, self.point)

class UpdateScore(Action):
    def __init__(self, engine, score_diff) -> None:
        super().__init__(engine)
        self.score_diff = score_diff

    def perform(self):
        self.engine.update_score(self.score_diff)

class GameOver(Action):
    def perform(self) -> None:
        self.engine.game_over()

class SpawnTempEntity(Action):
    def __init__(self, engine, point, char, color, lifespan):
        super().__init__(engine)
        self.point = point
        self.char = char
        self.color = color
        self.lifespan = lifespan

    def perform(self) -> None:
        self.engine.spawn_temp_entity(self.point, self.char, self.color, self.lifespan)

class DeleteEntity(Action):
    def __init__(self, engine, entity):
        super().__init__(engine)
        self.entity = entity

    def perform(self):
        self.engine.remove_entity(self.entity)