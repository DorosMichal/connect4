import numpy as np
from collections import Counter, defaultdict


def boards_squash():
    with open("boards", "r") as file:
        data = np.fromfile(file, dtype=np.int32, sep=" ")

    data = data.reshape(-1, 49 * 3 + 10)
    boards = data[:, :-10]
    labels = data[:, -1]

    res = defaultdict(Counter)
    d = defaultdict(list)
    c = Counter()
    for i, board in enumerate(boards):
        b = tuple(board)
        d[b].append(i)
        c[b] += 1

    for b in c.most_common():
        b = b[0]
        for i in d[b]:
            lab = labels[i]
            res[b][lab] += 1

    def categorize(wins, loses, draws):
        s = wins + loses + draws
        return round(((wins - loses) / s + 1) * 5)

    with open("squashed", "w") as file:
        for key, val in res.items():
            r = f" {categorize(val[-1], val[1], val[0])}\n"
            # board (49*3) + position_value(1)
            file.write(" ".join(map(str, key)) + r)


boards_squash()
