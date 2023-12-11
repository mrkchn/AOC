import re
from itertools import product
import numpy as np

with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

input = [int(x) for x in raw_data[0].split(": ")[-1].split(" ")]

maps = []
for line in raw_data[2:]+['']:
    if " map:" in line:
        map_name = line.split(" map:")[0]
        temp = []
    elif line != '':
        dest, source, length = [int(x) for x in line.split(" ")]
        temp.append([(source, source+length), dest-source])
    else:
        maps.append(temp)

intervals = [(input[i], input[i] + input[i+1]) for i in range(0, len(input), 2)]


def get_new_intervals(interval, imap):
    a, b = interval[0], interval[1]
    # print(f"a: {a}, b: {b}")
    for (c, d), adj in imap:
        # print(f"c: {c}, d: {d}")
        # print(sorted([a, b, c, d]))
        if sorted([a, b, c, d]) == [a, b, c, d]:
            pass
        elif sorted([a, b, c, d]) == [c, d, a, b]:
            pass
        elif sorted([a, b, c, d]) == [a, c, b, d]:
            return get_new_intervals((a, c), imap) + [(c+adj, b+adj)]
        elif sorted([a, b, c, d]) == [a, c, d, b]:
            return get_new_intervals((a, c), imap) + get_new_intervals((d, b), imap) + [(c+adj, d+adj)]
        elif sorted([a, b, c, d]) == [c, a, b, d]:
            return [(a+adj, b+adj)]
        elif sorted([a, b, c, d]) == [c, a, d, b]:
            return get_new_intervals((d, b), imap) + [(a+adj, d+adj)]
    return [(a, b)]


for imap in maps:
    new_intervals = []
    for interval in intervals:
        new_intervals.extend(get_new_intervals(interval, imap))
    intervals = new_intervals

while (0, 0) in intervals:
    intervals.remove((0, 0))

print(f"Solution b: {np.min(list(zip(*intervals))[0])}")






