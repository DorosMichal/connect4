import random


class Player:
    """player MUST not modify the board, even though it can"""

    def make_move(self, board, legal_moves):
        pass

    def end(self, board, winner):
        pass


class RandomPlayer(Player):
    def make_move(self, state):
        move = random.choice(state.get_legal_moves())
        return move


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

