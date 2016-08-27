import enum

import math
import weakref

import pyglet
from pyglet.gl import gl

from media import get_tile
from resources import ResourceType, Resource


TERRAIN_BATCH = pyglet.graphics.Batch()


class TileType(enum.Enum):
    R = ROAD = 0
    G = GROUND = 1
    W = WATER = 2
    T = TREE = 3
    S = STONE = 4
    B = BEDROCK = 5


TILE_COSTS = {
    TileType.ROAD: 0.5,
    TileType.GROUND: 1.0,
    TileType.WATER: 3.0,
    TileType.TREE: 2,
    TileType.STONE: 4,
    TileType.BEDROCK: math.inf,
}


TILE_IMAGES = {
    TileType.ROAD: get_tile(1, 5),
    TileType.GROUND: get_tile(1, 6),
    TileType.WATER: get_tile(0, 5),
    TileType.TREE: get_tile(10, 6),
    TileType.STONE: get_tile(8, 4),
    TileType.BEDROCK: get_tile(9, 4),
}


class Tile(pyglet.sprite.Sprite):

    def __init__(self, tile_type: TileType, world, x=0, y=0):
        self.type = tile_type
        self.hp = TILE_COSTS[self.type]
        img = TILE_IMAGES[self.type]
        super().__init__(img, x=x * 16, y=y * 16, batch=TERRAIN_BATCH)
        self.opacity = 0.0
        self._world = weakref.proxy(world)

    def update(self, dt):
        this_tile = (self.x // 16, self.y // 16)
        if this_tile in self._world.orders:
            self.color = (255, 0, 0)
        elif this_tile in [w.orders for w in self._world.workers]:
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)

    def draw_hp(self):
        full_hp = TILE_COSTS[self.type]
        if full_hp == math.inf:
            return
        percent = int((full_hp - self.hp) / full_hp * 4)
        if 0 < percent < 4:
            # TODO: Move this to the main function
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            get_tile(percent, 3).blit(self.x, self.y)

    def work_on(self, dt: float, new_type: TileType) -> bool:
        """Returns if the job is done."""
        self.hp -= dt
        if self.hp <= 0:
            # Spawn resources
            if self.type == TileType.WATER:
                self._world.resources.add(
                    Resource(ResourceType.WATER, self.x // 16, self.y // 16))
            elif self.type == TileType.TREE:
                self._world.resources.add(
                    Resource(ResourceType.WOOD, self.x // 16, self.y // 16))
            elif self.type == TileType.STONE:
                self._world.resources.add(
                    Resource(ResourceType.STONE, self.x // 16, self.y // 16))
            # Switch to a new type
            self.type = new_type
            self.hp = TILE_COSTS[self.type]
            self.image = TILE_IMAGES[self.type]
            # Update the map's visibility
            self._world.calculate_revealed(self._world.base.location)
            return True
        return False


WALKABLE_TYPES = [TileType.ROAD, TileType.GROUND, TileType.WATER]
DIGGABLE_TYPES = [TileType.TREE, TileType.STONE]
UNACTIONABLE_TYPES = [TileType.ROAD, TileType.BEDROCK]
VISIBLE_TYPES = [TileType.GROUND, TileType.WATER, TileType.ROAD]
