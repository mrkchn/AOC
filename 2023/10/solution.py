import copy

import numpy as np

with open('input.txt') as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]

directions = {
    "|": {"n": "n", "s": "s"},
    "-": {"e": "e", "w": "w"},
    "L": {"n": "w", "e": "s"},
    "J": {"n": "e", "w": "s"},
    "7": {"s": "e", "w": "n"},
    "F": {"e": "n", "s": "w"},
    ".": {},
}

moves = {
    "s": [-1, 0],
    "w": [0, 1],
    "n": [1, 0],
    "e": [0, -1]
}

def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])

diagram = np.array(raw_data)
start_dirs = ["n", "e", "s", "w"]
dist = np.ones(diagram.shape) * 1e10
s = tuple(np.argwhere(diagram == 'S')[0])
dist[s] = 0
for d in start_dirs:
    flag = True
    c = s
    steps = 0
    # print(f"starting from {d}")
    while flag:
        c = add_tuples(c, moves[d])
        # print(c)
        if (c == s) or (d not in directions[diagram[c]].keys()):
            # print("end of the road")
            flag = False
        else:
            d = directions[diagram[c]][d]
            # print(f"coming from {d}")
            steps += 1
            dist[c] = np.min([dist[c], steps])

dist[np.where(dist == 1e10)] = 0

print(f"Solution a: {int(np.max(dist))}")
# %%
# My hypothesis is that a region is "in the loop" if it has an odd number of boundaries on every side
borders = copy.deepcopy(dist)

horizontals = (np.abs(np.diff(dist, axis=1)) == 1) * 1
borders_above = (np.cumsum(horizontals, axis=0) % 2) == 1
borders_below = (np.flip(np.cumsum(np.flip(horizontals, axis=0), axis=0), axis=0) % 2) == 1
borders_horiz = (borders_above & borders_below) * 1
borders_horiz = np.hstack((borders_horiz, np.zeros((borders_horiz.shape[0], 1))))

verticals = (np.abs(np.diff(dist, axis=0)) == 1) * 1
borders_left = (np.cumsum(verticals, axis=1) % 2) == 1
borders_right = (np.flip(np.cumsum(np.flip(verticals, axis=1), axis=1), axis=1) % 2) == 1
borders_vert = (borders_left & borders_right) * 1
borders_vert = np.vstack((borders_vert, np.zeros((1, borders_vert.shape[1]))))

borders = (borders > 0) * 1
borders[s] = 1
interior = borders_vert * borders_horiz * (1 - borders)
print(f"Solution b: {int(np.sum(interior))}")

