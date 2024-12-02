
with open('input.txt') as f:
    left, right = zip(*[[int(y) for y in x.strip('\n').split(" ") if y != ''] for x in f.readlines()])

print(f"Solution 1: {sum([abs(l-r) for l,r in zip(*[sorted(left), sorted(right)])])}")
print(f"Solution 2: {sum([l * right.count(l) for l in left])}")
