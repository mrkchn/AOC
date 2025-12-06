import logging
from functools import lru_cache

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]


@lru_cache(maxsize=2**32)
def get_combinations(design, towels):
    logging.debug(f"design = {design}")
    if not design:
        logging.debug(f"found one!")
        return 1
    else:
        poss = 0
        for i in range(1, len(design)+1):
            t = design[:i]
            logging.debug(f"t = {t}")
            u = design[i:]
            if t in towels:
                poss += get_combinations(u, towels)
        logging.debug(f"end design = {design}")
        return poss


towels = tuple(raw_data[:raw_data.index('')][0].split(', '))
designs = raw_data[raw_data.index('')+1:]

combos = []
for i, d in enumerate(designs):
    logging.debug(f"looking at design #{i}")
    combos.append(get_combinations(d, towels))


print(f"Solution #1: {sum(1 for x in combos if x)}")
print(f"Solution #2: {sum(x for x in combos if x)}")