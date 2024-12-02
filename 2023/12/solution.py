import numpy as np
import logging
import re
from functools import lru_cache

log = logging.getLogger("blah")
# log.setLevel(level=logging.WARNING)
log.setLevel(level=logging.ERROR)


with open('input.txt') as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

springs = [line.split(" ")[0] for line in raw_data]
clusters = [tuple([int(x) for x in line.split(" ")[1].split(",")]) for line in raw_data]
springs = [x + '?' + x + '?' + x + '?' + x + '?' + x for x in springs]
clusters = [x * 5 for x in clusters]


def count_clusters(spring):
    return [len(x) for x in re.findall('#+', ''.join(spring))]

@lru_cache(maxsize=2**30)
def ways_to_arrange(spring, sub_spring, orig_cluster, sub_cluster, clust_count=0):
    current_clust = 0 if len(sub_cluster) == 0 else sub_cluster[0]
    # log.warning(f"checking: {''.join(spring), cluster}")
    if len(sub_spring) < (np.sum(sub_cluster) + len(sub_cluster) - 1):
        log.info(f"spring too short to have requisite clusters!")
        return 0
    elif len([x for x in sub_spring if x in ['?', '#']]) < sum(sub_cluster):
        log.info(f"not enough broken springs!")
        return 0
    elif len([x for x in sub_spring if x in ['?', '.']]) < len(sub_spring) - sum(sub_cluster):
        log.info(f"not enough fixed springs!")
        return 0

    diff = len(spring) - len(sub_spring)
    for i, s in enumerate(sub_spring):
        if s == "#":
            clust_count += 1
            if clust_count < current_clust:
                log.info(f"at {i} you have #, incrementing the cluster count.")
            elif (clust_count == current_clust) and ((i == len(sub_spring) - 1) or sub_spring[i + 1] in [".", "?"]):
                log.info(f"at {i} is the last # in the cluster")
                sub_cluster = sub_cluster[1:]
                current_clust = 0 if len(sub_cluster) == 0 else sub_cluster[0]
                clust_count = 0
                if i < (len(sub_spring) - 1):
                    sub_spring = sub_spring[:(i+1)] + '.' + sub_spring[(i+2):]
                    spring = spring[:(i+diff+1)] + '.' + spring[(i+diff+2):]
                    # sub_spring[i + 1] = '.'
                    # spring[i + diff + 1] = '.'
                else:
                    if not sub_cluster:
                        log.warning(f"{sub_cluster}")
                        log.warning(f"if you make it to the end of the string on a #, that's one way! {''.join(spring)}")
                        return 1
            elif (clust_count == current_clust) and (sub_spring[i + 1] == '#'):
                log.info(f"at {i+1} your cluster of {clust_count + 1} is too big")
                return 0
            else:
                log.info(f"at {i} your cluster of {clust_count} is too big.")
                return 0
        elif s == ".":
            if (clust_count > 0) and (clust_count != current_clust):
                log.info(f"at {i} you have too many/few in a cluster!")
                return 0
            elif (clust_count > 0) and (clust_count == current_clust):
                log.info(f"at {i-1} is the last # in the cluster")
                sub_cluster = sub_cluster[1:]
                current_clust = 0 if len(sub_cluster) == 0 else sub_cluster[0]
                clust_count = 0
            else:
                log.info(f"at {i} cluster count remains a zero")
        elif s == "?":
            if (clust_count > 0) and (clust_count > current_clust):
                log.info(f"at {i} you have too many in a cluster!")
                return 0
            elif (clust_count > 0) and (clust_count <= (current_clust - 1)):
                log.info(f"at {i} this ? needs to be #")
                # spring[i + diff] = '#'
                spring = spring[:(i+diff)] + '#' + spring[(i+diff+1):]
                clust_count += 1
            elif (clust_count > 0) and (clust_count == (current_clust - 1)):
                log.info(f"at {i} this ? needs to be the last #")
                # spring[i + diff] = '#'
                spring = spring[:(i+diff)] + '#' + spring[(i+diff+1):]
                sub_cluster = sub_cluster[1:]
                current_clust = 0 if len(sub_cluster) == 0 else sub_cluster[0]
                clust_count = 0
            elif (clust_count > 0) and (clust_count == current_clust):
                log.info(f"at {i} this ? needs to be the first .")
                # spring[i + diff] = '.'
                spring = spring[:(i+diff)] + '.' + spring[(i+diff+1):]
                sub_cluster = sub_cluster[1:]
                current_clust = 0 if len(sub_cluster) == 0 else sub_cluster[0]
                clust_count = 0
            elif (clust_count == 0) and ((i > 0) and sub_spring[i - 1] == "#"):
                log.info(f"at {i} cluster count is zero, this must be first .")
                # spring[i + diff] = '.'
                spring = spring[:(i+diff)] + '.' + spring[(i+diff+1):]
            else:
                log.info(f"at {i} cluster count is zero, this could be either")
                return (
                    ways_to_arrange(
                        spring[:(i+diff)] + "#" + spring[(i+diff+1):],
                        "#" + sub_spring[(i+1):],
                        orig_cluster,
                        sub_cluster
                    ) +
                    ways_to_arrange(
                        spring[:(i+diff)] + "." + spring[(i+diff+1):],
                        "." + sub_spring[(i+1):],
                        orig_cluster,
                        sub_cluster
                    )
                )

    return 1 if count_clusters(spring) == orig_cluster else 0


# %%
import time
poss_counts = []
for s, c in zip(springs, clusters):
    start = time.time()
    poss_counts.append(ways_to_arrange(s, s, c, c))
    end = time.time()
    print(f"took {end-start} seconds to do #{len(poss_counts)}")

print(f"Solution b: {np.sum(poss_counts)}")


# %%
#
# diffs = [x-y for x, y in zip(poss_counts, counts)]
# idx = diffs.index(1)
# print(''.join(springs[idx]), clusters[idx])
# print(ways_to_arrange(springs[idx], springs[idx], clusters[idx], clusters[idx]))





