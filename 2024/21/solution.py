import logging
import itertools
import numpy as np

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def add_tuple(p, q):
    return tuple(i+j for i, j in zip(p, q))


def mul_tuple(p, k):
    return tuple(i*k for i in p)


def get_move(p, q, keypad):
    row, col = add_tuple(q, mul_tuple(p, -1))

    if col >= 0:
        lr = ['>'] * col
    else:
        lr = ['<'] * abs(col)
    if row >= 0:
        ud = ['v'] * row
    else:
        ud = ['^'] * abs(row)

    if (keypad[add_tuple(p, (row, 0))] == 'X') or not lr:
        move = [lr + ud]
    elif (keypad[add_tuple(p, (0, col))] == 'X') or not ud:
        move = [ud + lr]
    else:
        move = [lr + ud, ud + lr]

    # logging.debug(f"({row}, {col}): {move}")
    return [m + ['A'] for m in move]


def get_sequences(code, keypad):
    output = []
    curr = list(zip(*np.where(keypad == 'A')))[0]
    for c in code:
        next = list(zip(*np.where(keypad == c)))[0]
        output.append(get_move(curr, next, keypad))
        curr = next
    return [list(itertools.chain.from_iterable(x)) for x in list(itertools.product(*output))]


# %%

with open('input.txt') as f:
    raw_data = [list(x.strip('\n')) for x in f.readlines()]


DIRS = {(0, 1): '>', (1, 0): 'v', (0, -1): '<', (-1, 0): '^'}

NUMERIC_KEYPAD = np.array([
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['X', '0', 'A'],
])

DIRECTIONAL_KEYPAD = np.array([
    ['X', '^', 'A'],
    ['<', 'v', '>'],
])


def get_complexity(directional_keypad_count):
    complexity = []
    for code in raw_data:
        logging.debug(f"code: {code}")
        num_seq = get_sequences(code, NUMERIC_KEYPAD)
        dir_seq = list(itertools.chain.from_iterable([get_sequences(s, DIRECTIONAL_KEYPAD) for s in num_seq]))
        for i in range(directional_keypad_count - 1):
            logging.debug(f"{len(dir_seq)}")
            dir_seq = list(itertools.chain.from_iterable([get_sequences(s, DIRECTIONAL_KEYPAD) for s in dir_seq]))
        complexity.append(min([len(s) for s in dir_seq]) * int(''.join(code[:-1])))
        logging.debug(f"{min([len(s) for s in dir_seq])} * {int(''.join(code[:-1]))}")
    return complexity

print(f"Solution #1: {sum(get_complexity(2))}")

print(f"Solution #2: {sum(get_complexity(3))}")