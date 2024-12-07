import re
from itertools import chain

with open('input.txt') as f:
    raw_data = f.read()


def mul(x,y):
    return x*y

def get_muls(input):
    return re.findall('mul\([\d]{1,3},[\d]{1,3}\)', input)

do_matches = re.findall("do\(\).*?don't\(\)", "do()"+raw_data+"don't()", flags=re.DOTALL)

print(f"Solution 1: {sum(list(map(eval, get_muls(raw_data))))}")
print(f"Solution 1: {sum(list(map(eval, list(chain.from_iterable(map(get_muls, do_matches))))))}")