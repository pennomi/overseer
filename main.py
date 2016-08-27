"""
OVERSEER: A "macromanagement" pyramid construction game. You never control
workers directly, but you can assign tasks and priorities.
"""


import pyglet

from generate_map import generate_simplex
from interface import INTERFACE_BATCH

from resources import ITEMS_BATCH
from tiles import UNACTIONABLE_TYPES, TERRAIN_BATCH
from workers import WORKERS_BATCH, Worker
from world import World

# Initialize window
window = pyglet.window.Window(vsync=True)
fps = pyglet.clock.ClockDisplay()


WORLD = World()


@window.event
def on_draw():
    window.clear()
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


# noinspection PyUnusedLocal
@window.event
def on_mouse_press(x, y, button, modifiers):
    point = (x//16, y//16)
    if WORLD.tiles[point].type not in UNACTIONABLE_TYPES:
        WORLD.orders.add(point)


def update(dt):
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
