import re
import numpy as np

with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

times = [int(x) for x in raw_data[0].split(" ")[1:] if x!='']
distances = [int(x) for x in raw_data[1].split(" ")[1:] if x!='']

long_time = int(''.join([x for x in raw_data[0].split(" ")[1:] if x!='']))
long_dist = int(''.join([x for x in raw_data[1].split(" ")[1:] if x!='']))

wins = []
for t, d in zip(times, distances):
    wins.append(len([s for s in range(t) if (t - s) * s > d]))

print(f"Solution a: {np.product(wins)}")
print(f"Solution b: {len([s for s in range(long_time) if (long_time - s) * s > long_dist])}")