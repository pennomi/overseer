"""A quick'n'dirty A* algorithm based off of Wikipedia's pseudocode."""

from collections import defaultdict

import math


def heuristic(a, b):
    """Manhattan distance (no diagonals)"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(world, start, goal):
    # The set of nodes already evaluated.
    closed_set = set()
    # The set of currently discovered nodes still to be evaluated.
    # Initially, only the start node is known.
    open_set = {start}
    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually
    # contain the most efficient previous step.
    came_from = dict()

    # For each node, the cost of getting from the start node to that node.
    g_score = defaultdict(lambda: math.inf)
    # The cost of going from start to start is zero.
    g_score[start] = 0
    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    f_scores = defaultdict(lambda: math.inf)
    # For the first node, that value is completely heuristic.
    f_scores[start] = heuristic(start, goal)

    while open_set:
        current = _get_lowest(open_set, f_scores)
        if current == goal:
            return _reconstruct_path(came_from, current)
        if not current:
            print("This probably shouldn't happen")
            return []

        open_set.remove(current)
        closed_set.add(current)
        for neighbor in world.neighbors(current):
            if neighbor in closed_set:
                continue  # Ignore the neighbor which is already evaluated.
            # The distance from start to a neighbor
            tentative_g_score = g_score[current] + world.cost(current, neighbor)
            if neighbor not in open_set:  # Discover a new node
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue  # This is not a better path.

            # This path is the best until now. Record it!
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_scores[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

    # We've failed. Return no path.
    return []


def _get_lowest(open_set, f_scores):
    lowest_value = math.inf
    lowest_point = None
    for p in open_set:
        value = f_scores[p]
        if value < lowest_value:
            lowest_value = value
            lowest_point = p
    return lowest_point


def _reconstruct_path(came_from: dict, current: (float, float)):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return list(reversed(total_path))
