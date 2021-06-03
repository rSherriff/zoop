#!/usr/bin/env python3
import copy
import time

import tcod

from engine import Engine
from tcod.sdl import Window

from application_path import get_app_path


def main() -> None:
    screen_width = 18
    screen_height = 12

    terminal_height = screen_height  * 2
    terminal_width = screen_width * 2

    tileset = tcod.tileset.load_tilesheet(
        get_app_path() + "/polyducks_12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    with tcod.context.new_terminal(
        terminal_width,
        terminal_height,
        tileset=tileset,
        title="Zoop",
        vsync=True,
        #sdl_window_flags = tcod.context.SDL_WINDOW_BORDERLESS
    ) as root_context:

        root_console = tcod.Console(screen_width, screen_height, order="F")
        engine = Engine(screen_width, screen_height)

        cycle = 0
        while True:
            root_console.clear()

            engine.event_handler.on_render(root_console=root_console)

            root_context.present(root_console)

            engine.handle_events(root_context)

            cycle += 1
            if cycle % 2 == 0:
                engine.update()


if __name__ == "__main__":
    main()
