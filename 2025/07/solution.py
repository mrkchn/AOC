# %%
import numpy as np
import itertools

with open("input.txt") as f:
    raw_data = [x.strip('\n') for x in f.readlines()]

numbers = np.array(list(zip(*itertools.zip_longest(*[list(x) for x in raw_data], fillvalue=''))))
sep_cols = [-1] + [idx for idx, col in enumerate((numbers == ' ').T) if all(col)] + [len(numbers[0])]
problems = [numbers[:, sep_cols[i]+1:sep_cols[i+1]] for i in range(len(sep_cols)-1)]

sols = []
sols_transpose = []
for p in problems:
    op = "".join(p[-1]).strip(" ")
    sols.append(eval(op.join(["".join(l) for l in p[:-1]])))
    sols_transpose.append(eval(op.join(["".join(l) for l in p[:-1].T])))

print(f"Solution #1: {sum(sols)}")
print(f"Solution #1: {sum(sols_transpose)}")