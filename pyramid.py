import pyglet
from media import get_tile
from resources import ResourceType, ITEMS_BATCH


class Pyramid(pyglet.sprite.Sprite):
    inventory = {
        ResourceType.WOOD: 0,
        ResourceType.WATER: 0,
        ResourceType.STONE: 0,
    }

    def __init__(self, x, y):
        # TODO: Build a big, multi-tile pyramid that changes by completion
        image = get_tile(0, 1)
        super().__init__(image, x=x * 16, y=y * 16, batch=ITEMS_BATCH)

    @property
    def location(self):
        return self.x // 16, self.y // 16

    def add_item(self, item):
        self.inventory[item.type] += 1
        # if item.type == ResourceType.STONE:
        #     STONE_PROGRESS.text = "STONE: {}".format(self.inventory[item.type])
        # elif item.type == ResourceType.WOOD:
        #     WOOD_PROGRESS.text = "WOOD: {}".format(self.inventory[item.type])
        # elif item.type == ResourceType.WATER:
        #     WATER_PROGRESS.text = "WATER: {}".format(self.inventory[item.type])

    def get_inventory(self):
        return inventory
