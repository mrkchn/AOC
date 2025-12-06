import numpy as np

with open('input.txt') as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]

city_map = np.array(raw_data)