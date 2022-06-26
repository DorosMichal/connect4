from playeres import RandomPlayer, ManualPlayer, NetPlayer, NetValuePlayer
from mcts_player import MCTS_Player
from game import Game
from datetime import datetime
from playeres import Method

random_player = RandomPlayer.creator()
net_player = NetPlayer.creator(Method.MOVE)
mcts_net = MCTS_Player.creator(7, 5, True)
mcts_roll = MCTS_Player.creator(7, 1, False)
net_value = NetValuePlayer.creator()
# mcts_player2 = MCTS_Player.creator(100, 10)
# mcts_player3 = MCTS_Player.creator(150, 30)
manual_player = ManualPlayer.creator()
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

game = Game(net_value, manual_player)
game.play()
# print(game.play_batch(30, False, False, 0))
