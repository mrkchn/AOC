import numpy as np
import logging
import re

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("blah")


with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

springs = [line.split(" ")[0] for line in raw_data]
clusters = [[int(x) for x in line.split(" ")[1].split(",")] for line in raw_data]

# wild_count = [s.count("?") for s in springs]
# print(np.sum([2**x for x in wild_count]))


def get_all_springs(spring):
    if spring[0] in ['#', '.']:
        results = [spring[0]]
    elif spring[0] == '?':
        results = ['#', '.']

    for s in spring[1:]:
        if s in ['#', '.']:
            results = [x + s for x in results]
        elif s == '?':
            results = [x + '.' for x in results] + [x + '#' for x in results]
    return results


def count_clusters(spring):
    return [len(x) for x in re.findall('#+', spring)]


def get_possible(springs, cluster):
    results = list(map(count_clusters, springs))
    possible = list(map(lambda x: x == cluster, results))
    return np.sum(possible)


counts = []
for s, c in zip(springs, clusters):
    x = get_all_springs(s)
    counts.append(get_possible(x, c))

print(f"Solution a: {np.sum(counts)}")

