import itertools
import numpy as np
from functools import lru_cache
from queue import PriorityQueue

with open('input.txt') as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]

grid = np.array(raw_data, dtype=int)

# %%

# let's keep track of our position p=(row, col)
# the direction we are moving in d=(row, col)
# and the number of blocks we have already moved in that direction, n=1 to 3
# then we can return a set of possible nodes
points = list(itertools.product(range(grid.shape[0]), range(grid.shape[1])))
dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

@lru_cache(maxsize=2**24)
def get_neighbors_ultra(p, d, n):
    blocked = []
    if n < 4:
        blocked += list(set(dirs) - set([d]))
    elif n >= 10:
        blocked += [d]
    new_ds = set(dirs) - set([(-d[0], -d[1])] + blocked)
    next_moves = []
    for nd in new_ds:
        new_p = (p[0] + nd[0], p[1] + nd[1])
        if ((new_p[0] >= 0) and (new_p[0] < grid.shape[0])) and ((new_p[1] >= 0) and (new_p[1] < grid.shape[1])):
            next_moves.append((new_p, nd, n+1 if d == nd else 1))
    return next_moves

@lru_cache(maxsize=2**24)
def get_neighbors(p, d, n):
    # Cannot continue in the same direction if we've already gone 3 blocks this way
    blocked = ([] if n < 3 else [d])
    # Get all the possible new directions
    new_ds = set(dirs) - set([(-d[0], -d[1])] + blocked)
    next_moves = []
    for nd in new_ds:
        new_p = (p[0] + nd[0], p[1] + nd[1])
        if ((new_p[0] >= 0) and (new_p[0] < grid.shape[0])) and ((new_p[1] >= 0) and (new_p[1] < grid.shape[1])):
            next_moves.append((new_p, nd, n+1 if d == nd else 1))

    return next_moves

vertices = list(itertools.product(points, dirs, range(1, 11)))
dist = {}
prev = {}
Q = []
for v in vertices:
    dist[v] = np.infty
    prev[v] = np.NaN
    Q += [v]
dist[((0, 0), (0, 1), 1)] = 0
dist[((0, 0), (1, 0), 1)] = 0

# %%
min_result = np.infty
while Q:
    u = min(Q, key=lambda x: dist[x])
    Q.remove(u)

    for v in set(Q) & set(get_neighbors_ultra(*u)):
        alt = dist[u] + grid[v[0]]
        if alt < dist[v]:
            dist[v] = alt
            prev[v] = u

    new_result = min([dist[v] for v in vertices if v[0] == (grid.shape[0]-1, grid.shape[1]-1)])
    if new_result < min_result:
        min_result = new_result
        print(new_result)

print(f"Solution 1: {min_result}")

