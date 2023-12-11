from functools import cmp_to_key
import numpy as np

with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

directions = raw_data[0]
nodes = {}
for line in raw_data[2:]:
    input = line.split(" = ")[0]
    left, right = line.split(" = ")[1].split(",")
    nodes.update({input: {"L": left[1:], "R": right[1:-1]}})

current = "AAA"
steps = 0
while current != "ZZZ":
    d = directions[steps % len(directions)]
    steps += 1
    current = nodes[current][d]

print(f"Solution a: {steps}")