from math import lcm

with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

directions = raw_data[0]
nodes = {}
for line in raw_data[2:]:
    input = line.split(" = ")[0]
    left, right = line.split(" = ")[1].split(",")
    nodes.update({input: {"L": left[1:], "R": right[1:-1]}})

currents = [x for x in nodes.keys() if x[-1] == 'A']
all_steps = []
for current in currents:
    steps = 0
    while current[-1] != "Z":
        d = directions[steps % len(directions)]
        steps += 1
        current = nodes[current][d]
    all_steps.append(steps)

print(f"Solution b: {lcm(*all_steps)}")