from playeres import RandomPlayer, ManualPlayer
from mcts_player import MCTS_Player
from game import Game
from datetime import datetime

random_player = RandomPlayer.creator()
mcts_player = MCTS_Player.creator(50, 5)
mcts_player2 = MCTS_Player.creator(100, 10)
mcts_player3 = MCTS_Player.creator(150, 30)
# manual_player = ManualPlayer.creator()
# score = {-1:0, 0:0, 1:0}
# for i in range(100):
#     game = Game(random_player, mcts_player)
#     res = game.play(track=False)
#     score[res] += 1
# print(score)
# def play_batch(p1, p2, n):
#     score = {-1:0, 0:0, 1:0, 2:0}
#     for i in range(n):
#         game = Game(p1, p2)
#         try:
#             res = game.play(track=False)
#             score[res] += 1
#         except:
#             score[2] += 1
#     print(score)

# play_batch(random_player, random_player, 200)
# play_batch(random_player, mcts_player, 200)
# play_batch(mcts_player, random_player, 200)
# play_batch(mcts_player, mcts_player2, 100)
# play_batch(mcts_player2, mcts_player, 100)
# play_batch(mcts_player, mcts_player3, 50)
# play_batch(mcts_player3, mcts_player, 50)
# play_batch(mcts_player3, mcts_player2, 100)
# play_batch(mcts_player2, mcts_player3, 100)

game = Game(mcts_player, mcts_player)
print(game.play_batch(2*10**4, False, True, 20))