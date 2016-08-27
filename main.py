"""
OVERSEER: A "macromanagement" pyramid construction game. You never control
workers directly, but you can assign tasks and priorities.
"""


import pyglet

from camera import Camera
from generate_map import generate_simplex
from interface import INTERFACE_BATCH

from resources import ITEMS_BATCH
from tiles import UNACTIONABLE_TYPES, TERRAIN_BATCH
from workers import WORKERS_BATCH, Worker
from world import World

# Initialize window
window = pyglet.window.Window(vsync=True)
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
    for w in WORLD.workers:
        w.debug_draw()
    for t in WORLD.tiles.values():
        if t:
            t.draw_hp()
    INTERFACE_BATCH.draw()
    fps.draw()

    # Cleanup
    CAMERA.post_draw()


# noinspection PyUnusedLocal
@window.event
def on_mouse_press(x, y, button, modifiers):
    # TODO: Undo the camera transform
    point = CAMERA.untransform(x, y)
    if WORLD.tiles[point].type not in UNACTIONABLE_TYPES:
        WORLD.orders.add(point)


# noinspection PyUnusedLocal
@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y > 0:
        CAMERA.zoom *= 1.1
    elif scroll_y < 0:
        CAMERA.zoom *= 0.9


def update(dt):
    # Pan Camera
    scroll_speed = 16 * 10
    scroll_edges = 0.1
    x = window._mouse_x
    horizontal_hotspot = window.width * scroll_edges
    if x < horizontal_hotspot:
        CAMERA.x += scroll_speed * dt
    elif x > window.width - horizontal_hotspot:
        CAMERA.x -= scroll_speed * dt

    # Update world logic
    for w in WORLD.workers:
        w.update(dt)
    for t in WORLD.tiles.values():
        if t:
            t.update(dt)
pyglet.clock.schedule_interval(update, 0.1)


def main():
    # TODO: Some sort of random seeding
    generate_simplex('simplex.map', 30, 30)
    WORLD.load('simplex.map', WORLD)
    WORLD.calculate_revealed(WORLD.base.location)
    WORLD.workers.append(Worker(9, 8, WORLD))
    WORLD.workers.append(Worker(9, 9, WORLD))
    WORLD.workers.append(Worker(10, 8, WORLD))
    WORLD.workers.append(Worker(10, 9, WORLD))

    # Run the game
    pyglet.app.run()


if __name__ == "__main__":
    main()
