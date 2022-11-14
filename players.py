from abc import ABC, abstractmethod
import random
from state import GameState


class Player(ABC):
    """player MUST not modify the state"""

    @abstractmethod
    def make_move(self, state: GameState) -> int:
        pass

    @abstractmethod
    def end(self, state: GameState, winner: int) -> None:
        pass


class RandomPlayer(Player):
    def make_move(self, state: GameState) -> int:
        move = random.choice(state.get_legal_moves())
        return move

    def end(self, state: GameState, winner: int) -> None:
        pass


class ManualPlayer(Player):
    def make_move(self, state: GameState) -> int:
        state.print_board()
        try:
            move = int(input())
            if move not in state.get_legal_moves():
                raise ValueError
        except ValueError:
            print(f"nie mozesz zrobić takiego ruchu, jeszcze raz")
            return self.make_move(state)
        return move

    def end(self, state: GameState, winner: int) -> None:
        state.print_board()
        print("game over")
