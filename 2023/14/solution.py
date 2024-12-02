import numpy as np

with open('input.txt') as f:
    raw_data = f.read()

panel = np.array([list(y) for y in raw_data.split('\n')])

def tilt_col(column):
    str_col = "".join(column)
    new_col = "#".join(["".join((['O'] * x.count('O') + ['.'] * x.count('.'))) for x in str_col.split("#")])
    return np.array(list(new_col))
def tilt_panel(panel, direction="north"):
    if direction == "north":
        panel = panel
    elif direction == "south":
        panel = np.flip(panel, axis=0)
    elif direction == "west":
        panel = np.transpose(panel)
    elif direction == "east":
        panel = np.flip(np.transpose(panel), axis=0)
    new_panel = np.apply_along_axis(tilt_col, axis=0, arr=panel)

    if direction == "north":
        new_panel = new_panel
    elif direction == "south":
        new_panel = np.flip(new_panel, axis=0)
    elif direction == "west":
        new_panel = np.transpose(new_panel)
    elif direction == "east":
        new_panel = np.flip(np.transpose(new_panel), axis=0)

    return new_panel

def calc_load(panel):
    total = 0
    for i in range(panel.shape[0]):
        total += np.sum(panel[i, :] == 'O') * (panel.shape[0] - i)
    return total

def cycle(panel, n=1):
    panels = []
    for i in range(n):
        panel = np.flip(np.flip(tilt_panel(tilt_panel(tilt_panel(tilt_panel(panel, "north"), "west"), "south"), "east"), axis=0), axis=1)
        panels.append(panel)
        # keep track of positions we've been in so far. When you hit a loop, you can use modular arithmetic.
        flag = np.where([np.all(panels[-1] == p) for p in panels[:-1]])[0]
        if flag.size:
            return panels[flag[0] + (n - flag[0]) % (i - flag[0]) - 1]
    return panel

new_panel = tilt_panel(panel, 'north')
print(f"Solution 1: {calc_load(tilt_panel(panel, 'north'))}")
print(f"Solution 2: {calc_load(cycle(panel, n=int(1e9)))}")

