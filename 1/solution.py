import re
import numpy as np
with open('input.txt') as f:
    raw_data = f.readlines()

convert = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

numeric_data_a = [re.findall(r"(?=([0-9]))", d) for d in raw_data]
two_digits_a = [int(x[0]) * 10 + int(x[-1]) for x in numeric_data_a]

numeric_data_b = [re.findall(r"(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))", d) for d in raw_data]
two_digits_b = [(convert[x[0]] if x[0] in convert.keys() else int(x[0])) * 10 + (convert[x[-1]] if x[-1] in convert.keys() else int(x[-1])) for x in numeric_data_b]

print(f"Part a: {np.sum(two_digits_a)}")
print(f"Part b: {np.sum(two_digits_b)}")


