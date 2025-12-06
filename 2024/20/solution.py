import copy
import logging
import itertools
import numpy as np
import networkx as nx
from collections import Counter

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def add_tuple(p, q):
    return tuple(i+j for i, j in zip(p, q))


def mul_tuple(p, k):
    return tuple(i*k for i in p)


def is_valid(p):
    return all((x > 0) and (x <= MAZE.shape[i]) for i, x in enumerate(p))


def taxi(p, q):
    return sum([abs(i-j) for i, j in zip(p, q)])


def get_ball(p, r):
    if r == 1:
        return set([add_tuple(p, d) for d in DIRS])
    else:
        se = [(r-i, i) for i in range(r+1)]
        ne = [(i-r, i) for i in range(r+1)]
        sw = [(r-i, -i) for i in range(r+1)]
        nw = [(i-r, -i) for i in range(r+1)]
        return set([add_tuple(p, x) for x in (se + ne + sw + nw)]) | get_ball(p, r-1)


with open('input.txt') as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]


MAZE = np.array(raw_data)
all_points = set(itertools.product(*[range(i) for i in MAZE.shape]))
walls = set(zip(*np.where(MAZE == '#')))
start = list(zip(*np.where(MAZE == 'S')))[0]
end = list(zip(*np.where(MAZE == 'E')))[0]

G = nx.DiGraph()
vertices = all_points - walls
for u in vertices:
    valid_neighbors = [add_tuple(u, d) for d in DIRS if add_tuple(u, d) in vertices]
    G.add_edges_from([(u, v) for v in valid_neighbors])

shortest = nx.shortest_path(G, start, end)


def count_cheats(shortest, r, hurdle):
    over_hurdle = 0
    # This algorithm assumes that the cheats are all along the shortest path
    # Look at every point on the shortest path
    for i in range(len(shortest)-1):
        # logging.debug(f"{i}/{len(shortest)}")
        u = shortest[i]
        # Get a ball of radius r around your point, and see if that intersects with the shortest path again
        for v in get_ball(u, r) & set(shortest[i+hurdle:]):
            j = shortest.index(v)
            k = taxi(u, v)
            # if it does, your "savings" is simply the difference in indices of your two points along the shortest path
            # minus the distance between those two points!
            if (j - i - k) >= hurdle:
                over_hurdle += 1
    return over_hurdle


# logging.debug(Counter(saved))
# print(f"Solution #1: {len([x for x in saved if x >= 100])}")
print(f"Solution #1: {count_cheats(shortest, 2, 100)}")
print(f"Solution #2: {count_cheats(shortest, 20, 100)}")

# %% Display
# idx = saved.index(81)
# display = np.full_like(MAZE, ".")
# display[start] = 'S'
# display[end] = 'E'
# display[tuple(zip(*(walls)))] = '#'
# display[tuple(zip(*(cheats[idx])))] = 'X'
# logging.debug(display)
#
