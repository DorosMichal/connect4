from game import Game
from mcts_player import MCTS_Player
from state import ConnectNState
from config import logging

p1 = MCTS_Player(40,2)
p2 = MCTS_Player(40,2)

game = Game(p1, p2, ConnectNState(), logging)
game.play()