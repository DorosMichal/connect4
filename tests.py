import pytest
from state import ConnectNState
import config

config.CONNECT_N = 4
config.BOARD_X = 7
config.BOARD_Y = 6
config.BOARD_SIZE = 42

board1 = """
x------
x------
x------
oxxxooo
oooxxxo
oooxxox
"""

board2 = """
-------
-------
o------
xo-----
xxo----
xxxoooo
"""
board3 = """
------x
----oxo
----xoo
oxxxooo
xxoxoxx
xoxoxoo
"""


def letter_to_val(letter: str):
    if letter == "o":
        return -1
    if letter == "x":
        return 1
    return 0


def board_to_state(board):
    board = board.split("\n")[1:-1]
    state = ConnectNState()
    first = True
    for i, line in enumerate(board):
        for j, let in enumerate(line):
            val = letter_to_val(let)
            state.board[i, j] = val
            if val:
                state.ctr += 1
                if first:
                    state.last_move = j
                    first = False
                if state._board_ctr[j] == config.BOARD_Y - 1:
                    state._board_ctr[j] = i - 1
    return state


@pytest.mark.parametrize(
    "board, expected_legal",
    ((board1, list(range(1, 7))), (board2, list(range(7))), (board3, list(range(6)))),
)
def test_get_legal_moves(board, expected_legal):
    state = board_to_state(board)
    legal = state.get_legal_moves()

    assert expected_legal == legal


@pytest.mark.parametrize(
    "board, expected_answer", ((board1, False), (board2, True), (board3, True))
)
def test_is_terminal(board, expected_answer):
    state = board_to_state(board)

    assert expected_answer == state.is_terminal()


@pytest.mark.parametrize(
    "board, expected_answer", ((board1, 0), (board2, -1), (board3, 1))
)
def test_result(board, expected_answer):
    state = board_to_state(board)

    assert expected_answer == state.result()
