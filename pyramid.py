from interface import stone_gauge, wood_gauge, water_gauge
from media import get_tile
from resources import ResourceType, ITEMS_BATCH
from sprite import BetterSprite


class Pyramid(BetterSprite):
    inventory = {
        ResourceType.WOOD: 0,
        ResourceType.WATER: 0,
        ResourceType.STONE: 0,
    }

    def __init__(self, x, y):
        # TODO: Build a big, multi-tile pyramid that changes by completion
        image = get_tile(0, 1)
        super().__init__(image, x, y, ITEMS_BATCH)

    @property
    def location(self):
        return self.x // 16, self.y // 16

    def add_item(self, item):
        self.inventory[item.type] += 1
        if item.type == ResourceType.STONE:
            stone_gauge.text = "STONE: {}".format(self.inventory[item.type])
        elif item.type == ResourceType.WOOD:
            wood_gauge.text = "WOOD: {}".format(self.inventory[item.type])
        elif item.type == ResourceType.WATER:
            water_gauge.text = "WATER: {}".format(self.inventory[item.type])
