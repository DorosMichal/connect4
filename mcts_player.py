from math import sqrt, log
from state import Connect4State
from game import Game
from playeres import RandomPlayer, Player
from keras.models import load_model
import numpy as np

INF = 10 ** 9


def sgn(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


class MCTS_Node:
    C = sqrt(2)

    def __init__(self, state, parent, move):
        self.state = state
        self.chosen = 0
        self.won = 0
        self.parent = parent
        self.move = move
        self.children = None

    def priority(self):
        if self.chosen == 0:
            return INF
        return self.won / self.chosen + MCTS_Node.C * sqrt(
            log(self.parent.chosen) / self.chosen
        )

    def select(self):
        if self.state.is_terminal() or self.children is None:
            return self
        return max(self.children, key=lambda c: c.priority()).select()

    def rollout(self):
        random_player = RandomPlayer.creator()
        game = Game(random_player, random_player, self.state.copy())
        return game.play(track=False)

    def update_res(self, res):
        self.chosen += 2
        player = self.state.player ^ 1
        self.won += (Connect4State.score_map[player] == res) * 2  # if win
        self.won += res == 0  # if draw

    def give_child_with_move(self, move):
        return list(filter(lambda c: c.move == move, self.children))[0]


class MCTS:
    def __init__(self, root, N, net):
        self.N = N
        self.root = root
        self.root.children = MCTS._create_children(root)
        # for child in self.root.children:
        #     child.children = MCTS._create_children(child)
        if net:
            self.simulate = self.simulate_net
            self.model = load_model("trained_model")
        else:
            self.simulate = self.simulate_roll

    @staticmethod
    def _create_children(node):
        player = node.state.player
        legal_moves = node.state.get_legal_moves()
        res = []
        for move in legal_moves:
            new_state = node.state.copy()
            new_state.update_board(move)
            child_node = MCTS_Node(new_state, node, move)
            res.append(child_node)
        return res

    def simulate_roll(self, node):
        # can be overridden with neuralnet
        res = sum(node.rollout() for _ in range(self.N))
        return sgn(res)

    def simulate_net(self, node):
        def labels_to_value(labels):
            i = np.argmax(labels)
            return -1 if i < 5 else 1 if i > 5 else 0

        b = node.state.board.reshape(49) + 1
        b = np.array([np.eye(3)[b].reshape((7, 7, 3))])
        c = node.state.ctr % 2
        c = np.array([np.eye(2)[c]])
        input = [b, c]
        pred = self.model.predict(input)  # 7 moves, 11 values
        moves = pred[0][0]
        labels = pred[1][0]
        return labels_to_value(labels)

    def big_rollout(self):
        node_to_expand = self.root.select()
        res = None
        if node_to_expand.state.is_terminal():
            res = node_to_expand.state.result()
        else:
            node_to_expand.children = self._create_children(node_to_expand)
            res = self.simulate(node_to_expand)

        node = node_to_expand
        while node is not None:
            node.update_res(res)
            node = node.parent

    def give_best_node(self):
        return max(self.root.children, key=lambda c: c.chosen)

    def make_best_move(self):
        best_node = self.give_best_node()
        self.root = best_node
        return best_node.move


class MCTS_Player(Player):
    def __init__(self, depth=100, rollouts=10, net=False):
        # depth must be at least number of children so that it goes two levels and generate children
        root = MCTS_Node(Connect4State(), None, None)
        # root.state.ctr = -1
        self.mcts = MCTS(root, rollouts, net)
        self.depth = depth

    def make_move(self, game_state):
        self.update_root(game_state)
        for _ in range(self.depth):
            self.mcts.big_rollout()

        best = self.mcts.make_best_move()
        return best

    @classmethod
    def creator(cls, depth, rollouts, net):
        return lambda: MCTS_Player(depth, rollouts, net)

    def update_root(self, game_state):
        if game_state.ctr >= 1:  # skip at first move
            move = game_state.last_move
            new_root = self.mcts.root.give_child_with_move(move)
            self.mcts.root = new_root
