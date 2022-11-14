from math import sqrt, log
from typing import List
from state import ConnectNState, GameState, Move
from game import Game
from players import RandomPlayer, Player
from config import logging

INF = 10 ** 9


def sgn(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


class MCTS_Node:
    C = sqrt(2)

    def __init__(self, state: GameState, parent: "MCTS_Node", move: Move):
        self.state = state
        self.chosen = 0
        self.won = 0
        self.parent = parent
        self.move = move
        self.children = None

    def priority(self) -> float:
        if self.chosen == 0:
            return INF
        return self.won / self.chosen + MCTS_Node.C * sqrt(
            log(self.parent.chosen) / self.chosen
        )

    def select_best_child(self) -> "MCTS_Node":
        if self.state.is_terminal() or self.children is None:
            return self
        return max(self.children, key=lambda c: c.priority()).select_best_child()

    def rollout(self) -> int:
        random_player = RandomPlayer()
        game = Game(random_player, random_player, self.state.copy())
        return game.play()

    def update_res(self, res: int) -> None:
        self.chosen += 2
        player = self.state.current_player ^ 1
        self.won += (ConnectNState.score_map[player] == res) * 2  # if win
        self.won += res == 0  # if draw

    def give_child_with_move(self, move: Move) -> "MCTS_Node":
        return next(filter(lambda c: c.move == move, self.children))


class MCTS:
    def __init__(self, root: MCTS_Node, depth: int, number_of_simulations: int):
        self.depth = depth
        self.simulations = number_of_simulations
        self.root = root
        self.root.children = MCTS._create_children(root)

    def make_best_move(self) -> Move:
        for _ in range(self.depth):
            self._big_rollout()

        best_node = self._give_best_node()
        self.root = best_node
        return best_node.move

    def make_opponents_move(self, state: GameState) -> None:
        if state.ctr >= 1:  # skip at first move
            move = state.last_move
            new_root = self.root.give_child_with_move(move)
            self.root = new_root

    def _simulate_roll(self, node: MCTS_Node) -> int:
        res = sum(node.rollout() for _ in range(self.simulations))
        return sgn(res)

    def _big_rollout(self) -> None:
        node_to_expand = self.root.select_best_child()
        res = None
        if node_to_expand.state.is_terminal():
            res = node_to_expand.state.result()
        else:
            node_to_expand.children = self._create_children(node_to_expand)
            res = self._simulate_roll(node_to_expand)

        node = node_to_expand
        while node is not None:
            node.update_res(res)
            node = node.parent

    def _give_best_node(self) -> MCTS_Node:
        node = max(self.root.children, key=lambda c: c.chosen)
        logging.log(logging.INFO,
            f"The best node is {node} with score {node.priority()} , representing move {node.move}"
        )
        return node

    @staticmethod
    def _create_children(node: MCTS_Node) -> List[MCTS_Node]:
        legal_moves = node.state.get_legal_moves()
        res = []
        for move in legal_moves:
            new_state = node.state.copy()
            new_state.update_board(move)
            child_node = MCTS_Node(new_state, node, move)
            res.append(child_node)
        return res


class MCTS_Player(Player):
    def __init__(self, depth: int = 100, rollouts: int = 10):
        # depth must be at least number of children so that it goes two levels and generate children
        root = MCTS_Node(ConnectNState(), None, None)
        self.mcts = MCTS(root, depth, rollouts)

    def make_move(self, game_state: ConnectNState) -> Move:
        self._update_root(game_state)
        best = self.mcts.make_best_move()
        return best

    def end(self, state, winner):
        pass

    def _update_root(self, game_state):
        self.mcts.make_opponents_move(game_state)
