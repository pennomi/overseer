import pyglet
from media import get_tile
from pyglet.text import Label
from resources import ResourceType, RESOURCE_IMAGES, RESOURCE_COLORS

stone_gauge = pyglet.image.load('stone_gauge.png')
water_gauge = pyglet.image.load('water_gauge.png')
wood_gauge = pyglet.image.load('wood_gauge.png')

INTERFACE_BATCH = pyglet.graphics.Batch()
INTERFACE_BATCH2 = pyglet.graphics.Batch()


RESOURCE_GAUGES = {
    ResourceType.WOOD: pyglet.sprite.Sprite(wood_gauge, x=0, y=0, batch=INTERFACE_BATCH),
    ResourceType.STONE: pyglet.sprite.Sprite(stone_gauge, x=0, y=40, batch=INTERFACE_BATCH),
    ResourceType.WATER: pyglet.sprite.Sprite(water_gauge, x=0, y=80, batch=INTERFACE_BATCH)
}


class Gauge:

    def __init__(self, resource_type: ResourceType, y: int):
        self.type = resource_type
        self.tile = RESOURCE_COLORS[self.type]
        self.colored_blocks = []
        self.y = y + 8

    def draw(self, amount):
        for i in range(amount):
            if i % 5 == 0:
                self.colored_blocks.append(pyglet.sprite.Sprite(
                    self.tile, x=i / 5 * 16 + 25, y=self.y, batch=INTERFACE_BATCH2))
