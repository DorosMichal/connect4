import numpy as np
from state import Connect4State

games_played = 0


class Game():
    def __init__(self, playerA, playerB, state=None, track=True, end=False):
        self.state = state or Connect4State()
        self.players = [playerA, playerB]
        self.track = track
        self.end = end

    def play(self):

        moves = np.zeros(49, dtype=int)

        while True:
            ctr = self.state.ctr
            player_no = ctr % 2
            move = self.players[player_no].make_move(self.state)
            if move not in self.state.get_legal_moves():
                raise ValueError(f'move {move} made by player {self.players[player_no]} was not legal')
            moves[ctr] = move
            self.state.update_board(move, player_no)

            if res:=self.state.is_terminal():
                winner = res

                if self.end:
                    for i in range(2):
                        self.players[i].end(self.state, winner)
                if self.track:
                    with open(f"game{games_played}", 'w') as file:
                        file.write(str(moves[:ctr + 1])[1:-1] + f'\n{winner}')
                return winner
        
        