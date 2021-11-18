import numpy as np
from collections import Counter, defaultdict


with open('boards', 'r') as file:
    data = np.fromfile(file, dtype=np.int32, sep=' ')

data = data.reshape(-1,49*3+9)
boards = data[:,:-9]
print(len(boards[0]))
labels = data[:,-1]

res = defaultdict(Counter)
d = defaultdict(list)
c = Counter()
for i,board in enumerate(boards):
    b = tuple(board)
    d[b].append(i)
    c[b] += 1


for b in c.most_common():
    b = b[0]
    for i in d[b]:
        lab = labels[i]
        res[b][lab] += 1



with open('squashed', 'w') as file:
    for key, val in res.items():
        # print(len(key))
        s = val[-1] + val[0] + val[1]
        r = f" {val[-1]/s:.2} {val[0]/s:.2} {val[1]/s:.2}\n"
        file.write(" ".join(map(str,key)) + r)