import numpy as np
import networkx as nx
import itertools
# Change this for the real problem!
# MAX_SIZE = 6
# FALLING_BYTES = 12
MAX_SIZE = 70
FALLING_BYTES = 1024
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def add_tuple(p, q):
    return tuple(i+j for i, j in zip(p, q))


def is_valid(p):
    return all((i > 0) and (i <= MAX_SIZE) for i in p)


with open('input.txt') as f:
    raw_data = [tuple(int(i) for i in x.strip('\n').split(',')) for x in f.readlines()]


falling_bytes = raw_data[:FALLING_BYTES]
G = nx.Graph()
vertices = set(itertools.product(*[range(MAX_SIZE + 1)] * 2)) - set(falling_bytes)
for u in vertices:
    valid_neighbors = [add_tuple(u, d) for d in DIRS if add_tuple(u, d) in vertices]
    G.add_edges_from([(u, v) for v in valid_neighbors])

path = nx.shortest_path(G, (0, 0), (MAX_SIZE, MAX_SIZE))
print(f"Solution #1: {len(path) - 1}")

# %%

for i in range(FALLING_BYTES + 1, len(raw_data)):
    falling_bytes = raw_data[:i]
    G = nx.Graph()
    vertices = set(itertools.product(*[range(MAX_SIZE + 1)] * 2)) - set(falling_bytes)
    for u in vertices:
        valid_neighbors = [add_tuple(u, d) for d in DIRS if add_tuple(u, d) in vertices]
        G.add_edges_from([(u, v) for v in valid_neighbors])
    try:
        path = nx.shortest_path(G, (0, 0), (MAX_SIZE, MAX_SIZE))
    except:
        break

print(f"Solution #2: {raw_data[i-1]}")

# %%
memory_space = np.full((MAX_SIZE+1, MAX_SIZE+1), '.')
memory_space[tuple(zip(*falling_bytes))] = '#'
memory_space[tuple(zip(*path))] = 'O'
memory_space = memory_space.transpose()