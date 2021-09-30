from playeres import RandomPlayer, ManualPlayer
from mcts_player import MCTS_Player
from game import Game

random_player1 = RandomPlayer()
random_player2 = RandomPlayer()
mcts_player = MCTS_Player()
manual_player = ManualPlayer()


game = Game(mcts_player, manual_player,)
game.play()
