import numpy as np
from state import Connect4State


class Game():
    def __init__(self, create_playerA, create_playerB, state=None):
        self.state = state or Connect4State()
        self.creators = [create_playerA, create_playerB]
        self.players = [creator() for creator in self.creators]

    def play(self, track=True, end=False, games_played=0):
        moves = np.zeros(49, dtype=int)

        while True:
            player = self.state.player
            move = self.players[player].make_move(self.state)
            if move not in self.state.get_legal_moves():
                raise ValueError(f'move {move} made by player {self.players[player]} was not legal')
            moves[self.state.ctr] = move
            self.state.update_board(move)

            if self.state.is_terminal():
                winner = self.state.result()

                if end:
                    for i in range(2):
                        self.players[i].end(self.state, winner)
                if track:
                    with open(f"games/game{games_played}", 'w') as file:
                        file.write(str(moves[:self.state.ctr])[1:-1] + f'\n{winner}')
                return winner
        
    def play_batch(self, batch_size, turns=True, track=False, start_enumeration=0):
        score = {-1:0, 0:0, 1:0}
        for i in range(batch_size):
            self.state = Connect4State()
            p1, p2 = (i%2, (i+1)%2) if turns else (0,1)
            self.players = [self.creators[p1](), self.creators[p2]()]
            res = self.play(track, False, i + start_enumeration)
            score[res if p1 == 0 else -res] += 1
        return score
