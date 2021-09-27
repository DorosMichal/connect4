from playeres import RandomPlayer, ManualPlayer
from mcts_player import MCTS_Player
from game import Game

random_player1 = RandomPlayer()
random_player2 = RandomPlayer()
mcts_player = MCTS_Player()
manual_player = ManualPlayer()


# game = Game(random_player2, random_player1)

game = Game(manual_player, mcts_player)
game.play()
