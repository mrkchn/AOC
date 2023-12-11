import numpy as np

with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

convert = {
    'red': np.array([1, 0, 0]),
    'green': np.array([0, 1, 0]),
    'blue': np.array([0, 0, 1])
}

def convert_to_tuple(draw):
    temp = np.array([0, 0, 0])
    for color in draw:
        temp += int(color.split(" ")[0]) * convert[color.split(" ")[-1]]

    return temp

cum_sum = 0
pow_sum = 0
for line in raw_data:
    game = int(line.split(": ")[0].split(" ")[-1])
    draws = line.split(": ")[-1].split("; ")
    colors = [draw.split(", ") for draw in draws]
    tuples = [convert_to_tuple(x) for x in colors]
    any_greater = np.any([t > np.array([12, 13, 14]) for t in tuples])
    # print(any_greater)
    if not any_greater:
        cum_sum += game
    min_set = np.max(list(zip(*tuples)), axis=1)
    pow_sum += np.prod(min_set)

print(f"Part a: {cum_sum}")
print(f"Part b: {pow_sum}")

