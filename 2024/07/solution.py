import itertools
from functools import partial

with open('input.txt') as f:
    raw_data = [x.strip('\n').split(": ") for x in f.readlines()]


def evaluate(input, value, ops):
    if all(len(i) > 1 for i in input):
        new_inputs = []
        for i in input:
            for op in ops:
                ni = eval(i[0] + op + i[1])
                if ni <= int(value):
                    new_inputs.append([str(ni)] + i[2:])
        if new_inputs:
            return evaluate(new_inputs, value, ops)
        else:
            return 0
    else:
        return int(value) if any(i[0] == value for i in input) else 0


test_values, inputs = list(zip(*raw_data))
inputs = [[x.split(' ')] for x in inputs]

print(f"Solution #1: {sum(list(map(partial(evaluate, ops=['+', '*']), inputs, test_values)))}")
print(f"Solution #2: {sum(list(map(partial(evaluate, ops=['+', '*', '']), inputs, test_values)))}")
