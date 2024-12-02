import numpy as np
import logging
import re
from functools import lru_cache

log = logging.getLogger("blah")
log.setLevel(level=logging.NOTSET)
# log.setLevel(level=logging.ERROR)


with open('input.txt') as f:
    raw_data = f.read()

patterns = [np.array([list(y) for y in x.split('\n')]) for x in raw_data.split('\n\n')]

# %%

def is_symmetric(p, axis=0, smudges=0):
    if (p.shape[0] <= 1) or (p.shape[1] <= 1) or (p.shape[axis] % 2):
        return False
    else:
        hashes = (p == "#") * 1
        dots = (p == ".") * 1
        sym_hashes = np.abs(np.sum((hashes * np.flip(hashes, axis=axis)) - hashes)) == smudges
        sym_dots = np.abs(np.sum((dots * np.flip(dots, axis=axis)) - dots)) == smudges
        return sym_hashes and sym_dots

# %%
def summarize(patterns, smudges=0):
    total = []
    for i, p in enumerate(patterns):
        # print(f"pattern {i}")
        # iterate through all rows, looking for horizontally symmetric
        for j in range(p.shape[0]):
            if is_symmetric(p[j:, :], axis=0, smudges=smudges):
                # print(f"symmetric after row {j}")
                total.append((j + (p.shape[0] - j) / 2) * 100)
            if is_symmetric(p[:j, :], axis=0, smudges=smudges):
                # print(f"symmetric before row {j}")
                total.append((j / 2) * 100)

        # iterate through all columns, looking for vertically symmetric
        for k in range(p.shape[1]):
            if is_symmetric(p[:, k:], axis=1, smudges=smudges):
                # print(f"symmetric after column {k}")
                total.append((k + (p.shape[1] - k) / 2))
            if is_symmetric(p[:, :k], axis=1, smudges=smudges):
                # print(f"symmetric before column {k}")
                total.append(k / 2)
    return np.sum(total)

print(f"Solution 1: {summarize(patterns, smudges=0)}")
print(f"Solution 2: {summarize(patterns, smudges=1)}")