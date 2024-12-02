import numpy as np
import itertools

with open('input.txt') as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]

galaxy = np.array(raw_data)
galaxy[galaxy == '#'] = 1
galaxy[galaxy == '.'] = 0
galaxy = galaxy.astype(int)

empty_cols = np.where(np.sum(galaxy, axis=0) == 0)[0]
empty_rows = np.where(np.sum(galaxy, axis=1) == 0)[0]

dist_a = np.ones(galaxy.shape)
dist_a[:, empty_cols] += 1
dist_a[empty_rows, :] += 1

dist_b = np.ones(galaxy.shape)
dist_b[:, empty_cols] += 1e6 - 1
dist_b[empty_rows, :] += 1e6 - 1

locations = list(zip(*np.where(galaxy == 1)))
location_pairs = set(list(itertools.combinations(locations, 2)))


def taxi_cab(a, b, d):
    min_y = np.min([a[0], b[0]])
    max_y = np.max([a[0], b[0]])
    min_x = np.min([a[1], b[1]])
    max_x = np.max([a[1], b[1]])
    return np.sum(d[min_y, min_x:max_x]) + np.sum(d[min_y:max_y, min_x])


shortest_dists_a = list(map(lambda x: taxi_cab(x[0], x[1], dist_a), location_pairs))
shortest_dists_b = list(map(lambda x: taxi_cab(x[0], x[1], dist_b), location_pairs))

print(f"Solution a: {int(np.sum(shortest_dists_a))}")
print(f"Solution b: {int(np.sum(shortest_dists_b))}")
