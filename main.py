"""
OVERSEER: A "macromanagement" pyramid construction game. You never control
workers directly, but you can assign tasks and priorities.
"""
import random

import pyglet

from camera import Camera
from generate_map import generate_simplex
from interface import INTERFACE_BATCH

from resources import ITEMS_BATCH
from tiles import UNACTIONABLE_TYPES, TERRAIN_BATCH
from workers import WORKERS_BATCH, Worker
from world import World

# Initialize window
window = pyglet.window.Window(vsync=True, resizable=True)
fps = pyglet.clock.ClockDisplay()


CAMERA = Camera()
WORLD = World()


@window.event
def on_draw():
    # Setup
    window.clear()
    CAMERA.pre_draw()  # TODO: Implement as a context manager

    # Draw
    TERRAIN_BATCH.draw()
    ITEMS_BATCH.draw()
    WORKERS_BATCH.draw()
    # for w in WORLD.workers:
    #     w.debug_draw()
    for t in WORLD.tiles.values():
        if t:
            t.draw_hp()

    # Cleanup
    CAMERA.post_draw()

    # Draw interface (non-transforming) widgets
    INTERFACE_BATCH.draw()
    fps.draw()


# noinspection PyUnusedLocal
@window.event
def on_mouse_press(x, y, button, modifiers):
    # TODO: Undo the camera transform
    point = CAMERA.untransform_mouse(x, y)
    if WORLD.tiles[point].type not in UNACTIONABLE_TYPES:
        WORLD.orders.add(point)


def update(dt):
    # Pan Camera
    scroll_speed = 16 * 10
    scroll_edge_size = 20
    x, y = window._mouse_x, window._mouse_y
    if 0 < x < scroll_edge_size:
        CAMERA.x += scroll_speed * dt
    elif window.width > x > window.width - scroll_edge_size:
        CAMERA.x -= scroll_speed * dt
    if 0 < y < scroll_edge_size:
        CAMERA.y += scroll_speed * dt
    elif window.height > y > window.height - scroll_edge_size:
        CAMERA.y -= scroll_speed * dt

    # Update world logic
    for w in WORLD.workers:
        w.update(dt)
    for t in WORLD.tiles.values():
        if t:
            t.update(dt)
pyglet.clock.schedule_interval(update, 0.1)


def main():
    size = 100
    generate_simplex('simplex.map', size, seed=random.randint(0, 1000000))
    WORLD.load('simplex.map', WORLD)
    WORLD.workers.append(Worker(size // 2 + 4, size // 2, WORLD))
    WORLD.workers.append(Worker(size // 2 + 4, size // 2 + 1, WORLD))
    WORLD.workers.append(Worker(size // 2 - 3, size // 2, WORLD))
    WORLD.workers.append(Worker(size // 2 - 3, size // 2 + 1, WORLD))

    # Run the game
    pyglet.app.run()


if __name__ == "__main__":
    main()
