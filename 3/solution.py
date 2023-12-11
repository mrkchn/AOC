import re
from itertools import product
import numpy as np

with open('input.txt') as f:
    raw_data = f.readlines()

num_chars = [str(x) for x in range(0, 10)]
parsed_data = np.vstack([np.array(list(x.strip('\n'))) for x in raw_data])
symbols = set(parsed_data.flatten()) - set(num_chars + ['.'])
symbol_grid = np.isin(parsed_data, list(symbols))
symbol_locations = list(zip(*np.where(symbol_grid)))

part_numbers = []
gear_ratios = []
for (x, y) in symbol_locations:
    parts_per_symbol = []
    seed_locations = [(x + i, y + j) for i, j in set(product(*[[-1, 0, 1], [-1, 0, 1]])) - set([(0, 0)]) if parsed_data[(x + i, y + j)] in num_chars]
    while seed_locations:
        (i, j) = seed_locations.pop()
        end = j
        while (end < parsed_data.shape[1]) and (parsed_data[(i, end)] in num_chars):
            if (i, end) in seed_locations:
                seed_locations.remove((i, end))
            end += 1

        start = j
        while (start >= 0) and (parsed_data[(i, start)] in num_chars):
            if (i, start) in seed_locations:
                seed_locations.remove((i, start))
            start -= 1

        parts_per_symbol.append(int("".join(parsed_data[i, (start+1):end])))
    if (parsed_data[(x, y)] == "*") and (len(parts_per_symbol) == 2):
        gear_ratios.append(np.multiply(*parts_per_symbol))
    part_numbers.extend(parts_per_symbol)

print(f"Solution a: {np.sum(part_numbers)}")
print(f"Solution b: {np.sum(gear_ratios)}")
