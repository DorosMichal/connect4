from typing import List, NewType
import numpy as np
from config import BOARD_X, BOARD_Y, BOARD_SIZE, CONNECT_N

Move = NewType("Move", int)


def _generate_all_connectN(x: int, y: int, n: int):
    """
    for every index on board X x Y
    generate all n-tuples of indexes that form winning configuration and contain this index.
    To make working with numpy easier, single winning configuration is of the form
    ((x1,x2,...,xn), (y1,y2,...,yn))
    and for every (i, j) theres a list of such configurations
    """
    # vertical
    v = [
        tuple((i, j) for i in range(k, k + n))
        for j in range(x)
        for k in range(y - n + 1)
    ]
    # horizontal
    h = [
        tuple((i, j) for j in range(k, k + n))
        for i in range(y)
        for k in range(x - n + 1)
    ]
    # diagonal right up
    d1 = [
        tuple((i - k, j + k) for k in range(n))
        for i in range(n - 1, y)
        for j in range(x - n + 1)
    ]
    # diagonal left up
    d2 = [
        tuple((i - k, j - k) for k in range(n))
        for i in range(n - 1, y)
        for j in range(n - 1, x)
    ]
    t = h + v + d1 + d2
    # make (x, x, x, x) (y, y, y, y) instead of (x,y)
    return {
        (i, j): [tuple(zip(*scheme)) for scheme in t if (i, j) in scheme]
        for i in range(y)
        for j in range(x)
    }


class GameState:
    @property
    def current_player(self) -> int:
        pass

    def get_legal_moves(self) -> List[Move]:
        pass

    def update_board(self, move: int) -> None:
        pass

    def is_terminal(self) -> bool:
        pass

    def result(self) -> int:
        pass


class ConnectNState(GameState):
    score_map = {-1: 0, 0: -1, 1: 1}

    scores = [np.zeros(CONNECT_N, dtype=int) - 1, np.zeros(CONNECT_N, dtype=int) + 1]
    winning_schemas = _generate_all_connectN(BOARD_X, BOARD_Y, CONNECT_N)

    def __init__(self, ctr: int = 0, last_move: Move = None):
        self.ctr = 0
        self.board = np.zeros((BOARD_Y, BOARD_X), dtype=int)
        self._board_ctr = np.zeros(BOARD_X, dtype=int) + (BOARD_Y - 1)
        self.last_move = None

    @property
    def current_player(self) -> int:
        return self.ctr % 2

    def get_legal_moves(self) -> List[Move]:
        return [i for i in range(BOARD_X) if self._board_ctr[i] >= 0]

    def _scheme_wins(
        self, scheme: "ConnectNState", player_no: int
    ) -> int:  # player_no is 0 or 1
        if all(self.board[scheme] == ConnectNState.scores[player_no]):
            return player_no
        return -1

    def _someone_wins(self, move: Move, player_no: int) -> int:
        for scheme in ConnectNState.winning_schemas[(self._board_ctr[move] + 1, move)]:
            res = self._scheme_wins(scheme, player_no)
            if res > -1:
                return res
        return -1

    def update_board(self, move: Move) -> None:
        self.board[self._board_ctr[move], move] = ConnectNState.score_map[
            self.current_player
        ]
        self._board_ctr[move] -= 1
        self.ctr += 1
        self.last_move = move

    def copy(self) -> "ConnectNState":
        new = ConnectNState()
        new.board = self.board.copy()
        new._board_ctr = self._board_ctr.copy()
        new.ctr = self.ctr
        return new

    def is_terminal(self) -> bool:
        move = self.last_move
        player = (
            self.current_player ^ 1
        )  # we want player that made last move, not current player to play
        if move is None:
            return 0
        return self._someone_wins(move, player) > -1 or self.ctr == BOARD_SIZE

    def result(self) -> int:
        move = self.last_move
        player = self.current_player ^ 1
        if move is None:
            return 0
        res = self._someone_wins(move, player)
        if res > -1 or self.ctr == BOARD_SIZE:
            return ConnectNState.score_map[res]
        return ConnectNState.score_map[-1]

    def print_board(self) -> None:
        def letter(i, j):
            if self.board[i, j] == 0:
                return "_"
            if self.board[i, j] == 1:
                return "x"
            return "o"

        for i in range(BOARD_Y):
            for j in range(BOARD_X):
                print(letter(i, j), end=" ")
            print()
