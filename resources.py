import enum

import pyglet

from media import get_tile

ITEMS_BATCH = pyglet.graphics.Batch()


class ResourceType(enum.Enum):
    WOOD = 0
    WATER = 1
    STONE = 2


RESOURCE_IMAGES = {
    ResourceType.WATER: get_tile(0, 4),
    ResourceType.STONE: get_tile(1, 2),
    ResourceType.WOOD: get_tile(2, 2),
}

RESOURCE_COLORS = {
    ResourceType.WATER: get_tile(10, 5),
    ResourceType.STONE: get_tile(8, 4),
    ResourceType.WOOD: get_tile(11, 7)
}


class Resource(pyglet.sprite.Sprite):

    def __init__(self, resource_type: ResourceType, x: int, y: int):
        self.type = resource_type
        img = RESOURCE_IMAGES[self.type]
        super().__init__(img, x=x * 16, y=y * 16, batch=ITEMS_BATCH)

    @property
    def location(self):
        return self.x // 16, self.y // 16
