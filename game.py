import numpy as np
BOARD_LENGTH = 7


class Game:
    def __init__(self, playerA, playerB, state):
        self.state = state
        self.players = [playerA, playerB]

    def play(self, track=True, end=False):
        moves = np.zeros(BOARD_LENGTH**2, dtype=int)

        while True:
            player = self.state.player
            move = self.players[player].make_move(self.state)
            if move not in self.state.get_legal_moves():
                raise ValueError(
                    f"move {move} made by player {self.players[player]} was not legal"
                )
            moves[self.state.ctr] = move
            self.state.update_board(move)

            if self.state.is_terminal():
                winner = self.state.result()

                if end:
                    for i in range(2):
                        self.players[i].end(self.state, winner)
                return winner
