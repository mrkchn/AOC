from functools import lru_cache
import numpy as np
import itertools
import logging
import math
import re


# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("blah")


with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]


def is_valid(s, c):
    return c == tuple([len(x) for x in re.findall('#+', s)])

# %%

# This assumes s is composed of only '?' and '#'
@lru_cache(maxsize=2**31)
def get_all_defined(s, c):
    if not s.count('#'):
        return get_all_defined_from_unknowns(s, c)
    min_length = np.sum(c) + len(c) - 1
    if len(s) < min_length:
        return []
    elif s.count('#') > np.sum(c):
        return []
    elif not s.count('?'):
        return [s]

    summary = [(len(x), x[0]) for x in re.findall('\\?+|#+', s)]
    if summary[0][1] == '#':
        summary = [(0, '?')] + summary
    if summary[-1][1] == '#':
        summary = summary + [(0, '?')]

    seeds = tuple([k for k, v in summary if v == '#'])
    possible_clusters = [[i for i, x in enumerate(c) if x >= seed] for seed in seeds]
    seed_orderings = [tuple(k) for k in itertools.product(*possible_clusters) if all(x < y for x, y in zip(k, k[1:]))]
    perfect_summaries = []
    defined_springs = []
    for seed_order in seed_orderings:
        non_seed_clusters = [c[i+1:j] if c[i+1:j] else (0,) for i, j in zip([-1] + list(seed_order), list(seed_order) + [len(c)])]
        # if 0 in seed_order:
        #     non_seed_clusters = [(0,)] + non_seed_clusters
        # if len(c) - 1 in seed_order:
        #     non_seed_clusters = non_seed_clusters + [(0,)]
        temp = []
        for x, y, z, a in zip(*[summary[:-2:2], summary[1:-1:2], summary[2::2], seed_order]):
            # temp.append(complete_seed(x[0], y[0], z[0], c[a]))
            temp.append(complete_seed(x, y, z, c[a]))

        perfect_summaries.extend([list(itertools.chain.from_iterable([list(y[:2]) for y in x] + [[x[-1][2]]])) for x in itertools.product(*temp) if np.all([i[2] == j[0] for i, j in zip(x[:-1], x[1:])])])
        for summ in perfect_summaries:
            # for the unknowns, the first one cannot end on a '#', the last one cannot start on a '#' and the interior ones cannot have '#' on either side.
            unks = []
            for i, (x, y) in enumerate(zip(summ[::2], non_seed_clusters)):
                if (i == 0) and (x > 0):
                    unks.append([z + '.' for z in get_all_defined_from_unknowns('?' * (x - 1), y)])
                elif (i == (len(non_seed_clusters) - 1)) and (x > 0):
                    unks.append(['.' + z for z in get_all_defined_from_unknowns('?' * (x - 1), y)])
                elif (i > 0) and (i < len(non_seed_clusters) - 1) and (x > 2):
                    unks.append(['.' + z + '.' for z in get_all_defined_from_unknowns('?' * (x - 2), y)])
                else:
                    unks.append(get_all_defined_from_unknowns('?' * x, y))

            hashes = [[x * '#'] for x in summ[1::2]]
            interleave = unks + hashes
            interleave[::2] = unks
            interleave[1::2] = hashes
            summ_springs = list(itertools.product(*interleave))
            defined_springs.extend([''.join(x) for x in summ_springs])

    return defined_springs


# %%
@lru_cache(maxsize=2**31)
def complete_seed(x, y, z, a):
    temp = []
    x = x[0] if x[1] == '?' else 0
    y = y[0]
    z = z[0] if z[1] == '?' else 0
    for i in range(a-y+1):
        if (x >= i) and (a - y - i <= z):
            temp.append((x-i, a, z-(a-y-i)))
    return temp
# %%
@lru_cache(maxsize=2**31)
def complete_seed2(x, y, z, a):
    temp = []
    l = x[0] if x[1] == '?' else 0
    m = y[0]
    n = z[0] if z[1] == '?' else 0
    for i in range(a-y[0]+1):
        if (l >= i) and (a - m - i <= n):
            temp.append((((l - i, '?') if x[1] == '?' else x), (a, '#'), (n - (a - m - i), '?') if z[1] == '?' else z))
    return temp
# %%

# This assumes s is only '?'
@lru_cache(maxsize=2**31)
def get_all_defined_from_unknowns(s, c):
    Q = len(s)
    H = np.sum(c)
    N = len(c) + 1
    P = Q - H
    # if we want at least one unbroken spring in each interior bucket
    M = P - (N - 2)
    # if we will allow no unbroken springs in some buckets
    # M = P
    if (M >= 0) and (N > 0):
        temp = []
        hashes = ['#' * i for i in c]
        for x in partition(M, N):
            dots = ['.' * i for i in add_one_to_interior(x)]
            interleave = dots + hashes
            interleave[::2] = dots
            interleave[1::2] = hashes
            temp.append(''.join(interleave))

        return list(set(temp))
    else:
        return ['']
# %%

@lru_cache(maxsize=2**31)
def partition(items, bins):
    if items == 0:
        return [(0,) * bins]
    else:
        temp = list(set(partition(items - 1, bins)))
        p = []
        for i in temp:
            for j in [tuple(x) for x in np.identity(bins, dtype=int)]:
                p.append(elem_sum(i, j))
        return list(set(p))

# %%

def elem_sum(i, j):
    return tuple(x+y for x, y in zip(i, j))


def add_one_to_interior(i):
    return elem_sum(i, (0,) + (len(i) - 2) * (1,) + (0, ))


# %%
# @lru_cache(maxsize=2**31)
# def count_ways(s, c):
#     if len(s) < (np.sum(c) + len(c) - 1):
#         return 0
#     # print(s, c)
#     if not s.count('?'):
#         return int(is_valid(s, c))
#     if s.count('.'):
#         sub_s = [x for x in s.split('.') if x]
#         # partitions = [list(x) for x in itertools.combinations(list(range(len(c) + 1)), len(sub_s) - 1)]
#         count = 0
#         for p in partitions:
#             sub_c = []
#             for i, j in zip([0] + p, p + [len(c)]):
#                 sub_c.append(c[i: j])
#             count += np.product([count_ways(new_s, new_c) for new_s, new_c in zip(sub_s, sub_c)])
#         return count
#
#     return np.sum([count_ways(new_s, c) for new_s in get_all_defined(s, c)])

# %%

@lru_cache(maxsize=2**31)
def count_ways(s, c):
    if len(s) < (np.sum(c) + len(c) - 1):
        return 0
    # print(s, c)
    if not s.count('?'):
        return int(is_valid(s, c))
    if s.count('.'):
        sub_s = [x for x in s.split('.') if x]
        summary = [(len(x), x[0]) for x in re.findall('\\?+|#+|\\.+', s)]

        seeds = tuple([k for k, v in summary if v == '#'])
        seed_idxs = [i for i, (k, v) in enumerate(summary) if v == '#']
        possible_clusters = [[i for i, x in enumerate(c) if x >= seed] for seed in seeds]
        seed_orderings = [tuple(k) for k in itertools.product(*possible_clusters) if all(x < y for x, y in zip(k, k[1:]))]
        perfect_summaries = []
        defined_springs = []
        for seed_order in seed_orderings:
            non_seed_clusters = [c[i+1:j] if c[i+1:j] else (0,) for i, j in zip([-1] + list(seed_order), list(seed_order) + [len(c)])]
            temp = []
            for i, x in enumerate(summary):
                if i in seed_idxs:
                    temp.append(complete_seed2(summary[i-1] if i > 0 else (0, '.'), summary[i], summary[i+1] if (i+1) < len(summary) else (0, '.'), c[seed_order[seed_idxs.index(i)]]))
                elif (i-1 not in seed_idxs) and (i not in seed_idxs) and (i+1 not in seed_idxs):
                    temp.append([x])

            all_summaries = list(itertools.product(*temp))
            # START HERE
            perfect_summaries.extend([list(itertools.chain.from_iterable([list(y[:2]) for y in x] + [[x[-1][2]]])) for x in itertools.product(*temp) if np.all([i[2] == j[0] for i, j in zip(x[:-1], x[1:])])])
            for summ in perfect_summaries:
                # for the unknowns, the first one cannot end on a '#', the last one cannot start on a '#' and the interior ones cannot have '#' on either side.
                unks = []
                for i, (x, y) in enumerate(zip(summ[::2], non_seed_clusters)):
                    if (i == 0) and (x > 0):
                        unks.append([z + '.' for z in get_all_defined_from_unknowns('?' * (x - 1), y)])
                    elif (i == (len(non_seed_clusters) - 1)) and (x > 0):
                        unks.append(['.' + z for z in get_all_defined_from_unknowns('?' * (x - 1), y)])
                    elif (i > 0) and (i < len(non_seed_clusters) - 1) and (x > 2):
                        unks.append(['.' + z + '.' for z in get_all_defined_from_unknowns('?' * (x - 2), y)])
                    else:
                        unks.append(get_all_defined_from_unknowns('?' * x, y))

                hashes = [[x * '#'] for x in summ[1::2]]
                interleave = unks + hashes
                interleave[::2] = unks
                interleave[1::2] = hashes
                summ_springs = list(itertools.product(*interleave))
                defined_springs.extend([''.join(x) for x in summ_springs])


        return count

    return np.sum([count_ways(new_s, c) for new_s in get_all_defined(s, c)])


# %%

import time
springs = [line.split(" ")[0] for line in raw_data]
clusters = [[int(x) for x in line.split(" ")[1].split(",")] for line in raw_data]
springs = [''.join((list(x) + ['?']) * 4 + list(x)) for x in springs]
clusters = [tuple(x * 5) for x in clusters]

# %%
# print(f"Solution a: {np.sum(counts)}")
counts = []
i = 1
s = springs[i]
c = clusters[i]
start = time.time()
counts.append(count_ways(s, c))
end = time.time()
print(f"Solved {i} in {end-start:0.2f} seconds: {counts[-1]} ")

print(np.sum(counts))