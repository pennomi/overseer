import pyglet
from pyglet.text import Label

INTERFACE_BATCH = pyglet.graphics.Batch()

STONE_PROGRESS = Label('STONE: 0', x=0, y=0, batch=INTERFACE_BATCH)
WOOD_PROGRESS = Label('WOOD: 0', x=0, y=20, batch=INTERFACE_BATCH)
WATER_PROGRESS = Label('WATER: 0', x=0, y=40, batch=INTERFACE_BATCH)
