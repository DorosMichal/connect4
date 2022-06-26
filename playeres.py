from enum import Enum
from keras.models import load_model
import random
import numpy as np


class Player:
    """player MUST not modify the board, even though it can"""

    def make_move(self, board, legal_moves):
        pass

    def end(self, board, winner):
        pass

    @classmethod
    def creator(*args):
        pass


class RandomPlayer(Player):
    def make_move(self, state):
        move = random.choice(state.get_legal_moves())
        return move

    @classmethod
    def creator(cls):
        return lambda: RandomPlayer()


class ManualPlayer(Player):
    def __init__(self):
        self.board = None

    def make_move(self, state):
        self.board = state.board
        self.print_board()
        try:
            move = int(input())
        except ValueError:
            return self.make_move(state)
        if move not in state.get_legal_moves():
            print(f"nie mozesz zrobić ruchu {move}, jeszcze raz")
            return self.make_move(state)
        else:
            state.last_move = move
            return move

    @classmethod
    def creator(cls):
        return lambda: ManualPlayer()

    def end(self, board, winner):
        self.board = board
        self.print_board()
        print("game over")

    def print_board(self):
        def letter(i, j):
            if self.board[i, j] == 0:
                return "_"
            if self.board[i, j] == 1:
                return "x"
            return "o"

        for i in range(7):
            for j in range(7):
                print(letter(i, j), end=" ")
            print()


class Method(Enum):
    LABEL = 0
    MOVE = 1


class NetPlayer(Player):
    def __init__(self, method: Method):
        self.board = None
        self.method = method
        self.model = load_model("trained_model")

    def predict_state(self, state):
        b = state.board.reshape(49) + 1
        b = np.array([np.eye(3)[b].reshape((7, 7, 3))])
        c = state.ctr % 2
        c = np.array([np.eye(2)[c]])
        input = [b, c]
        pred = self.model.predict(input)  # 7 moves, 11 values
        moves = pred[0][0]
        labels = pred[1][0]
        return (moves, labels)

    def make_move(self, state):
        def labels_to_value(labels):
            i = np.argmax(labels)
            return -1 if i < 5 else 1 if i > 5 else 0

        def give_move(state, moves):
            mask = state.get_legal_moves_mask()
            moves[mask] += 10
            return np.argmax(moves)

        if self.method == Method.LABEL:
            pass

        if self.method == Method.MOVE:
            moves, labels = self.predict_state(state)
            return give_move(state, moves)

    @classmethod
    def creator(cls, method):
        return lambda: NetPlayer(method)


class NetValuePlayer(Player):
    def __init__(self):
        self.board = None
        self.model = load_model("trained_model_values")

    def process_state(self, state):
        b = state.board.reshape(49) + 1
        b = np.array([np.eye(3)[b].reshape((7, 7, 3))])
        c = state.ctr % 2
        c = np.array([np.eye(2)[c]])
        pred = self.model([b, c])[0].numpy()
        return (pred.argmax(), pred.max())

    # to działa tylko gdy grasz jako pierwszy
    def make_move(self, state):
        legal = state.get_legal_moves()
        states = [state.copy() for _ in legal]
        for m, s in zip(legal, states):
            s.update_board(m)
        val = [(i, self.process_state(s)) for i, s in enumerate(states)]
        print(val)
        best = max(val, key=lambda x: x[1][0] * 16 + x[1][1])
        return legal[best[0]]

    @classmethod
    def creator(cls):
        return lambda: NetValuePlayer()
