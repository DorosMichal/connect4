import numpy as np


def generate_all_connect4():
    # horizontal
    h = [tuple((i,j) for i in range(k, k+4)) for j in range(7) for k in range(4)]
    # vertical
    v = [tuple((i,j) for j in range(k, k+4)) for i in range(7) for k in range(4)]
    # diagonal right up
    d1 = [tuple((i-k,j+k) for k in range(4)) for i in range(3,7) for j in range(4)]
    # diagonal left up
    d2 = [tuple((i-k,j-k) for k in range(4)) for i in range(3,7) for j in range(3,7)]
    t = h + v + d1 + d2
    # make (x, x, x, x) (y, y, y, y) instead of (x,y)
    return {(i,j) : [tuple(zip(*scheme)) for scheme in t if (i,j) in scheme] for i in range(7) for j in range(7)}


class Connect4State():
    score_map = {-1: 0, 0: -1, 1: 1}

    scores = [np.zeros(4, dtype=int) + 1, np.zeros(4, dtype=int) - 1]
    winning_schemas = generate_all_connect4()

    def __init__(self):
        self.ctr = 0
        self.board = np.zeros((7,7), dtype=int)
        self._board_ctr = np.zeros(7, dtype=int) + 6
        self.last_move = None

    def get_legal_moves(self):
        return [i for i in range(7) if self._board_ctr[i] >= 0]

    def scheme_wins(self, scheme, player_no): #player_no is 0 or 1
        if all(self.board[scheme] == Connect4State.scores[player_no]): return player_no
        return -1

    def someone_wins(self, move, player_no):
        for scheme in Connect4State.winning_schemas[(self._board_ctr[move] + 1, move)]:
            if (res:= self.scheme_wins(scheme, player_no)) > -1:
                return res
        return -1

    def update_board(self, move, player_no):
        self.board[self._board_ctr[move], move] = 1 if player_no == 0 else -1
        self._board_ctr[move] -= 1
        self.ctr += 1
    
    def copy(self):
        new = Connect4State()
        new.board = self.board.copy()
        new._board_ctr = self._board_ctr.copy()
        return new

    def is_terminal(self):
        move = self.last_move
        player_no = self.ctr % 2
        if (res:=self.someone_wins(move, player_no)) > -1 or self.ctr == 49:
            return Connect4State.score_map[res]
        return Connect4State.score_map[-1]
