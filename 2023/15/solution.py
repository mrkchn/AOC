import numpy as np

with open('input.txt') as f:
    raw_data = f.read().split(",")

def hash(clear):
    ascii_vals = [ord(x) for x in clear]
    current_value = 0
    for val in ascii_vals:
        current_value = ((current_value + val) * 17) % 256
    return current_value

def hash_map(inst, hmap):
    if '-' in inst:
        label = inst[:-1]
        box = hash(label)
        new_contents = []
        for (l, f) in hmap[box]:
            if label != l:
                new_contents.append((l, f))
        hmap[box] = new_contents
    else:
        label, focal_length = inst.split('=')
        box = hash(label)
        new_contents = []
        found = False
        for l, f in hmap[box]:
            if label == l:
                found = True
                new_contents.append((l, focal_length))
            else:
                new_contents.append((l, f))
        if not found:
            new_contents.append((label, focal_length))
        hmap[box] = new_contents
    return hmap

# %%

print(f"Solution 1: {np.sum([hash(x) for x in raw_data])}")

hmap = {i: [] for i in range(256)}
for inst in raw_data:
    hmap = hash_map(inst, hmap)

focusing_power = np.sum([np.sum([(1 + num) * (i + 1) * int(f) for i, (l, f) in enumerate(box)]) for num, box in hmap.items()])
print(f"Solution 2: {int(focusing_power)}")
