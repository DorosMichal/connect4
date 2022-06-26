import numpy as np

N = 20000

### data format 3 * 49 board places in one-hot + move_ctr(or player) + move in one hot(7) + final label


def generate_exp_res():
    with open("squashed", "r") as sq:
        data = np.fromfile(sq, sep=" ", dtype=int)
        data = data.reshape(-1, 3 * 49 + 1)
        boards = data[:, : 3 * 49]
        labels = data[:, -1]
        exp_res = dict(zip(map(tuple, boards), labels))
    return exp_res


m = {-1: "1 0 0", 0: "0 1 0", 1: "0 0 1"}
exp_res = generate_exp_res()


def to_input(board):
    seq = map(lambda x: m[x], board)
    return " ".join(seq)


def move_to_onehot(move, n):
    t = np.zeros(n, dtype=int)
    t[move] = 1
    return " ".join(map(str, t))


def change_to_boards(output, move_seq, label):
    ctr = np.zeros(7, dtype=int)
    board = np.zeros(49, dtype=int)
    global exp_res

    for i, move in enumerate(move_seq):
        board[ctr[move] * 7 + move] += -1 if i % 2 else 1
        ctr[move] += 1
        player = i % 2
        board_str = to_input(board)
        output.write(board_str)
        output.write(
            f" {(i+1) % 2} {i % 2} {move_to_onehot(move , 7)} {exp_res[tuple(map(int,board_str.split()))]}\n"
        )


if __name__ == "__main__":
    with open("boards1", "w") as boards:
        for i in range(N + 1):
            with open(f"games/game{i}", "r") as game:
                data = np.fromfile(game, dtype=int, sep=" ")
                label = data[-1]
                move_seq = data[:-1]
                change_to_boards(boards, move_seq, label)
