import math
import weakref

import pyglet

from media import get_tile
from pathfinding import find_path
from resources import Resource
from tiles import DIGGABLE_TYPES, TileType, TILE_COSTS

WORKERS_BATCH = pyglet.graphics.Batch()

WORKER_IMAGE = get_tile(14, 0)


class Worker(pyglet.sprite.Sprite):
    speed = 32

    def __init__(self, x, y, world):
        super().__init__(WORKER_IMAGE, x=x*16, y=y*16, batch=WORKERS_BATCH)
        self.path = []
        self.orders = None
        self.inventory = None
        self._world = weakref.proxy(world)

    @property
    def current_location(self):
        return (self.x+8) // 16, (self.y+8) // 16

    def update(self, dt):
        tile = self._world.tiles[self.current_location]
        if self.current_location == self.orders:
            done = True
            if tile.type in DIGGABLE_TYPES:
                done = tile.work_on(dt, TileType.GROUND)
            elif tile.type == TileType.GROUND:
                done = tile.work_on(dt, TileType.ROAD)
            elif tile.type == TileType.WATER:
                done = tile.work_on(dt, TileType.WATER)

            if done:
                self.orders = None
            return

        # If we're tracking a resource, try to pick it up
        elif isinstance(self.orders, Resource) and self.current_location == self.orders.location and not self.inventory:
            self._world.resources.remove(self.orders)
            self.inventory = self.orders
            self.path = find_path(self._world, self.current_location, self._world.base.location)
            if not self.path:
                self.orders = None
                self.inventory = None
                print("We lost a resource forever")
            return

        # Deposit items into the base
        elif self.inventory and self.current_location == self._world.base.location:
            self._world.base.add_item(self.inventory)
            self.inventory = None
            self.orders = None
            return

        # If idle, look for something to do
        if not self.path and not self.orders:
            if self._world.orders:
                # TODO: Prioritize orders by proximity and priority level
                tile = self._world.orders.pop()
                self.path = find_path(self._world, self.current_location, tile)
                if not self.path:
                    self._world.orders.add(tile)
                else:
                    self.orders = tile
            # Try to get a resource
            elif self._world.resources:
                other_orders = {w.orders for w in self._world.workers if w is not self}
                targets = [w for w in self._world.resources if w not in other_orders]
                if targets:
                    res = targets[0]
                    self.path = find_path(
                        self._world, self.current_location, (res.x//16, res.y//16))
                    self.orders = res
            return
        elif not self.path and self.orders:
            print("Uh oh, orders were", self.orders)
            self.orders = None
            return

        # Otherwise, just follow the path
        dx = self.path[0][0] * 16 - self.x
        dy = self.path[0][1] * 16 - self.y
        speed = self.speed / TILE_COSTS[tile.type]
        if self.current_location == self.path[0]:
            self.path.pop(0)
            self.update(dt)  # recurse
            return
        # Movement
        elif abs(dx) >= 1 and abs(dx) > abs(dy):
            self.x += speed * math.copysign(1, dx) * dt
        elif abs(dy) >= 1 and abs(dy) > abs(dx):
            self.y += speed * math.copysign(1, dy) * dt

        # If there's an inventory, move it too
        if self.inventory:
            self.inventory.x = self.x
            self.inventory.y = self.y

    def debug_draw(self):
        flat_list = []
        for p in self.path:
            flat_list.append(p[0] * 16 + 8)
            flat_list.append(p[1] * 16 + 8)
        pyglet.gl.glLineWidth(2.0)
        pyglet.graphics.draw(
            len(flat_list) // 2,
            pyglet.gl.GL_LINE_STRIP,
            ("v2f", flat_list)
        )
