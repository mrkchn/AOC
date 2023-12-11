import re
from itertools import product
import numpy as np

with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

game = [int(x.split(":")[0].split(" ")[-1]) for x in raw_data]
winning_numbers = [set([int(y) for y in re.findall(r"[0-9]+", x.split(": ")[-1].split(" | ")[0])]) for x in raw_data]
card_numbers = [set([int(y) for y in re.findall(r"[0-9]+", x.split(": ")[-1].split(" | ")[-1])]) for x in raw_data]
cards = list(zip(card_numbers, winning_numbers))
matches = [len(w & c) for w, c in cards]
points = [2**(x-1) if x>0 else 0 for x in matches]

instance_count = np.ones(len(cards))
for i, c in enumerate(cards):
    m = len(c[0] & c[1])
    instance_count[(i+1):(i+m+1)] = instance_count[(i+1):(i+m+1)] + [instance_count[i]] * len(instance_count[(i+1):(i+m+1)])
    print(instance_count)

print(f"Solution a: {np.sum(points)}")
print(f"Solution b: {np.sum(instance_count)}")

