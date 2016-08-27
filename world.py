from collections import defaultdict

from pyramid import Pyramid
from tiles import TileType, TILE_COSTS, WALKABLE_TYPES, DIGGABLE_TYPES, Tile


class World:
    tiles = defaultdict(lambda: None)
    orders = set()
    resources = set()
    base = Pyramid(9, 9)
    workers = []

    def load(self, filename, world):
        for y, line in enumerate(open(filename, 'r')):
            for x, column in enumerate(line):
                if column not in TileType.__dict__:
                    continue
                t = Tile(getattr(TileType, column), world, x=x, y=y)
                self.tiles[(x, y)] = t

    def neighbors_los(self, p):
        potential_points = [
            (p[0] + 1, p[1]),
            (p[0], p[1] + 1),
            (p[0] - 1, p[1]),
            (p[0], p[1] - 1),
            (p[0] + 1, p[1] + 1),
            (p[0] - 1, p[1] + 1),
            (p[0] - 1, p[1] - 1),
            (p[0] + 1, p[1] - 1),
        ]
        points = []
        for p in potential_points:
            tile = self.tiles[p]
            if not tile:
                continue
            points.append(p)
        return points

    def neighbors(self, p):
        potential_points = [
            (p[0] + 1, p[1]),
            (p[0], p[1] + 1),
            (p[0] - 1, p[1]),
            (p[0], p[1] - 1),
        ]
        points = []
        for p2 in potential_points:
            old_tile = self.tiles[p]
            if old_tile.type in DIGGABLE_TYPES:
                continue
            tile = self.tiles[p2]
            if not tile:
                continue
            if tile.type in WALKABLE_TYPES + DIGGABLE_TYPES:
                points.append(p2)
        return points

    def cost(self, p1, p2):
        t1, t2 = self.tiles[p1], self.tiles[p2]
        return (TILE_COSTS[t1.type] + TILE_COSTS[t2.type]) / 2
