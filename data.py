import numpy as np
N = 14961

### data format 3 * 49 board places in one-hot + move_ctr + move in one hot(7) + final label

m = {-1: "1 0 0", 0: "0 1 0", 1: "0 0 1"}

def to_input(board):
    seq = map(lambda x: m[x], board)
    return " ".join(seq)

def move_to_onehot(move):
    t = np.zeros(7, dtype=int)
    t[move] = 1
    return " ".join(map(str, t))

def change_to_boards(output, move_seq, label):
    ctr = np.zeros(7, dtype=int)
    board = np.zeros(49, dtype=int)

    for i, move in enumerate(move_seq):
        board[ctr[move] * 7 + move] += -1 if i % 2 else 1
        ctr[move] += 1
        if i % 2 == 0: # record only from first player perspective
            output.write(to_input(board))
            output.write(f" {i} {move_to_onehot(move)} {label}\n")

with open("boards", 'w') as boards:
    for i in range(N + 1):
        with open(f"games/game{i}", 'r') as game:
            data = np.fromfile(game, dtype=int, sep=" ")
            label = data[-1]
            move_seq = data[:-1]
            change_to_boards(boards, move_seq, label)


with open("boards", 'r') as boards, open("boards_squashed", 'w') as squashed:
    data = np.fromfile(boards, dtype=np.int32, sep=' ')