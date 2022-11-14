INFO = 20


class Game:
    def __init__(self, playerA, playerB, state, logger=None):
        self.state = state
        self.players = [playerA, playerB]
        self.logger = logger

    def play(self, end=False) -> int:
        while True:
            player = self.state.current_player
            move = self.players[player].make_move(self.state)
            if move not in self.state.get_legal_moves():
                raise ValueError(
                    f"move {move} made by player {self.players[player]} was not legal"
                )
            self.state.update_board(move)
            if self.logger:
                self.logger.log(INFO, move)

            if self.state.is_terminal():
                winner = self.state.result()

                if end:
                    for i in range(2):
                        self.players[i].end(self.state, winner)
                if self.logger:
                    self.logger.log(INFO, winner)
                return winner
