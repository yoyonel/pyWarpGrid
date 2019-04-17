"""

"""
# import _pickle as pickle
import logging

import pyglet
import pymunk

from warp_grid.game_window import GameWindow
from warp_grid.warp_map_renderer import WarpMapRenderer


def main():
    space = pymunk.Space()

    # TODO: Find a way to test if multisample (AA) is available
    config = pyglet.gl.Config(
        sample_buffers=0,
        samples=0,
        double_buffer=True
    )

    window = GameWindow(
        WarpMapRenderer(space, 13, 11),
        1. / 60.,
        space,
        config=config,
        caption='Fire - WarpMap',
        resizable=False, fullscreen=False, vsync=False,
        record_simu=False,
    )

    # No limitation on display framerate
    pyglet.clock.schedule_interval_soft(window.update, -1)
    pyglet.clock.set_fps_limit(None)

    pyglet.app.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(module)s - %(levelname)s - %(message)s'
    )
    main()
