import numpy as np

with open('input.txt') as f:
    raw_data = [[int(y) for y in x.strip('\n').split(" ")] for x in f.readlines()]

next_num = []
first_num = []
for seq in raw_data:
    sub_seqs = [seq]
    while not np.all(sub_seqs[-1] == 0):
        sub_seqs.append(np.diff(sub_seqs[-1]))
    next_num.append(np.sum(list(reversed([x[-1] for x in sub_seqs]))))
    temp = [0]
    for i in range(len(sub_seqs)):
        temp.append(-temp[-1] + sub_seqs[len(sub_seqs)- 1 - i][0])
    first_num.append(temp[-1])

print(f"Solution a: {np.sum(next_num)}")
print(f"Solution b: {np.sum(first_num)}")