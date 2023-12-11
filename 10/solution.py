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