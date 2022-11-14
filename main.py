from enum import Enum
from typing import List, Tuple
from config import MIN_DEPTH
from players import RandomPlayer, ManualPlayer
from mcts_player import MCTS_Player
from state import ConnectNState
from game import Game

available_oponenets = [RandomPlayer, MCTS_Player]


def ask_for_input(
    message: str, options: List[str], numeric: bool = False
) -> Tuple[int, str]:
    print(message)
    for i, option in enumerate(options):
        print(f"{i}) {option}")
    while True:
        try:
            choice = int(input("choose number: "))
            if numeric:
                return choice, ""
            if choice in range(len(options)):
                return choice, options[choice]
            raise ValueError
        except ValueError:
            print("Wrong value, please input number of chosen option")
        except EOFError:
            print("Exiting, bye bye")
            exit(0)


class Modes(Enum):
    single_player = "single-player"
    pvp = "pvp"


def welcome_prompt() -> None:
    print("Hi, let's play a connect4 game")
    _, mode = ask_for_input("What mode do you want to play?", [m.value for m in Modes])
    p1 = ManualPlayer()
    p2 = None
    player_to_start = None
    if Modes(mode) == Modes.single_player:
        oponent_no, _ = ask_for_input(
            "Choose your opponent", [op.__name__ for op in available_oponenets]
        )
        if available_oponenets[oponent_no] == MCTS_Player:
            depth, _ = ask_for_input("Choose depth of MCTS Player", [], True)
            depth = max(depth, MIN_DEPTH)
            rollout_no, _ = ask_for_input("Choose number of rollouts", [], True)
            rollout_no = max(rollout_no, 1)
            p2 = MCTS_Player(depth, rollout_no)
        p2 = available_oponenets[oponent_no]()
        player_to_start, _ = ask_for_input(
            "Do you want to go first or second?", ["first", "second"]
        )

    if p2 is None:
        p2 = ManualPlayer()
    if player_to_start == 1:
        p1, p2 = p2, p1

    game = Game(p1, p2, ConnectNState())
    game.play(end=True)
    welcome_prompt()


if __name__ == "__main__":
    welcome_prompt()
