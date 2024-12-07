import numpy as np

# %%
# given a grid, a point, and a direction, determine the new direction(s) of the beam:
dim2dir = {
    0: (0, 1),
    1: (0, -1),
    2: (1, 0),
    3: (-1, 0)
}

increment = {
    '.': {
        0: [0],
        1: [1],
        2: [2],
        3: [3],
    },
    '|': {
        0: [2, 3],
        1: [2, 3],
        2: [2],
        3: [3],
    },
    '-': {
        0: [0],
        1: [1],
        2: [0, 1],
        3: [0, 1],
    },
    '/': {
        0: [3],
        1: [2],
        2: [1],
        3: [0],
    },
    '\\': {
        0: [2],
        1: [3],
        2: [0],
        3: [1],
    },
}

# %%
# given a grid and energy_grid signature, return the energy_grid signature one step later
def step(grid, energy):
    lit_spots = list(zip(*np.where(energy > 0)))
    for (y, x, z) in lit_spots:
        for d in increment[grid[y, x]][z]:
            dy, dx = dim2dir[d]
            if (x+dx >= 0) and (x+dx < energy.shape[1]) and (y+dy >= 0) and (y+dy < energy.shape[0]):
                energy[y + dy, x + dx, d] = 1
    return energy


def get_energy(energy):
    proj = energy.sum(axis=2)
    return len(list(zip(*np.where(proj > 0))))


def find_steady_state(start=(0, 0, 0)):
    energy_grid = np.zeros(grid.shape + (4,))
    energy_grid[start] = 1
    flag = True
    while flag:
        proj = energy_grid.sum(axis=2)
        energy_grid = step(grid, energy_grid)
        new_proj = energy_grid.sum(axis=2)
        if np.all(proj == new_proj):
            flag = False
    return energy_grid

# %%

with open('input.txt') as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]

grid = np.array(raw_data)

# %%
# energy_grid represents all of the unique beams (and their directions)
# 0 is moving east
# 1 is moving west
# 2 is moving south
# 3 is moving north


print(f"Solution 1: {get_energy(find_steady_state(start=(0,0,0)))}")

# Now let's generate a set of entry points.
entry_points = [(i, 0, 0) for i in range(grid.shape[0])] + \
               [(i, grid.shape[1]-1, 1) for i in range(grid.shape[0])] + \
               [(0, i, 2) for i in range(grid.shape[1])] + \
               [(grid.shape[0]-1, i, 3) for i in range(grid.shape[1])]

max_energy = 0
while entry_points:
    p = entry_points[0]
    energy_grid = find_steady_state(start=p)
    energy = get_energy(energy_grid)
    if energy > max_energy:
        max_point = p
        max_energy = energy
    lit_spots = list(zip(*np.where(energy_grid > 0)))
    entry_points = list(set(entry_points) - set(lit_spots))
    # print(f"{len(entry_points)} left to consider")

print(f"Solution 2: {max_energy} at {max_point[:2]}")

