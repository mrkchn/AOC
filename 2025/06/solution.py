# %%
import numpy as np

with open("input.txt") as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]

manifold = np.array(raw_data, dtype=object)
num_manifold = np.zeros_like(manifold)


def add_tuple(p, q):
    return tuple(i+j for i, j in zip(p, q))


def is_valid(p, size=manifold.shape):
    return all((i >= 0) and (i < j) for i, j in zip(p, size))


start = list(zip(*np.where(manifold == 'S')))[0]
splitters = list(zip(*np.where(manifold == '^')))
num_manifold[start] = 1
num_manifold[np.where(manifold == '.')] = 0

for row in range(manifold.shape[0]):
    to_explore = [b for b in list(zip(*np.where(num_manifold > 0))) if b[0] == row]
    for p in to_explore:
        q = add_tuple(p, (1, 0))
        if q in splitters:
            new_points = [add_tuple(q, (0, 1)), add_tuple(q, (0, -1))]
        else:
            new_points = [q]
        valid_points = [x for x in new_points if is_valid(x)]
        for v in valid_points:
            num_manifold[v] += num_manifold[p]

print(f"Solution #1: {len(set(zip(*np.where(num_manifold > 0))) & set([add_tuple(s, (-1, 0)) for s in splitters]))}")
print(f"Solution #2: {np.sum(num_manifold[-1,:])}")

