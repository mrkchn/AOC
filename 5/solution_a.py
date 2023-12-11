import re
from itertools import product
import numpy as np

with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

input = [int(x) for x in raw_data[0].split(": ")[-1].split(" ")]

# input_b = []
# for i in range(0, len(input), 2):
#     input_b.extend(list(range(input[i], input[i] + input[i+1])))
# input = input_b

maps = {}
for line in raw_data[2:]+['']:
    if " map:" in line:
        map_name = line.split(" map: ")[0]
        temp_map = []
    elif line != '':
        dest, source, length = [int(x) for x in line.split(" ")]
        temp_map.append([dest, source, length])
    else:
        # temp_map = [list(x) for x in zip(*temp_map)]
        maps.update({map_name: np.array(temp_map)})

for map_name, temp_map in maps.items():
    new_input = []
    for i in input:
        idx = np.where((i >= temp_map[:, 1]) & (i < temp_map[:, 1] + temp_map[:, 2]))
        if len(idx[0]) < 1:
            new_input.append(i)
        else:
            new_input.append(i - temp_map[idx[0][0], 1] + temp_map[idx[0][0], 0])
    input = new_input

print(f"Solution a: {np.min(input)}")


