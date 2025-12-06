import itertools
import numpy as np
import networkx as nx


def add_tuple(p, q):
    return tuple(i+j for i, j in zip(p, q))


with open('input.txt') as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]


DIRS = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
MAZE = np.array(raw_data)
nodes = list(zip(*np.where(MAZE != '#')))

G = nx.DiGraph()
G.add_nodes_from(nodes)

for a in itertools.product(nodes, DIRS.keys()):
    neighbors = [(add_tuple(a[0], DIRS[a[1]]), a[1])] + [(a[0], d) for d in DIRS.keys() if d != a[1]]
    G.add_weighted_edges_from([(a, b, 1 if a[1] == b[1] else 1000) for b in neighbors])

start = list(zip(*np.where(MAZE == 'S')))[0]
end = list(zip(*np.where(MAZE == 'E')))[0]
paths = sorted(
    [nx.shortest_path(G, (start, ">"), (end, k), weight='weight') for k in [">", "^"]],
    key=lambda x: nx.path_weight(G, x, weight='weight')
)
all_paths = nx.all_shortest_paths(G, (start, ">"), (end, paths[0][-1][1]), weight='weight')
all_nodes_on_paths = set.union(*[set(list(zip(*path))[0]) for path in all_paths])
print(f"Solution #1: {nx.path_weight(G, paths[0], weight='weight')}")
print(f"Solution #2: {len(all_nodes_on_paths)}")

# %%
# for p, d in paths[0]:
#     MAZE[p] = d
# print(MAZE)
# %%
