from math import sqrt, log
from state import Connect4State
from game import Game
from playeres import RandomPlayer, Player

INF = 10**9

def sgn(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0

class Node():
    C = sqrt(2)
    def __init__(self, state, parent, move):
        self.state = state
        self.chosen = 0
        self.won = 0
        self.parent = parent
        self.move = move
        self.children = None

    def priority(self):
        if self.chosen == 0: return INF
        return self.won/self.chosen + Node.C * sqrt(log(self.parent.chosen)/self.chosen)

    def select(self):
        pass


class MCTS_Node(Node):

    def select(self):
        if self.children is None:
            return self
        return max(self.children, key=lambda c : c.priority()).select()

    def rollout(self):
        game = Game(RandomPlayer(), RandomPlayer(), self.state, track=False)
        return game.play()

    def update_res(self, res):
        self.chosen += 1
        player = self.state.ctr % 2
        self.won += Connect4State.score_map[player] == res
        
    def give_child_with_move(self, move):
        return list(filter(lambda c: c.move == move, self.children))[0]

class MCTS:
    N = 1000
    def __init__(self, root):
        self.root = root
        self.root.children = self._create_children(root)

    def _create_children(self, node):
        player = node.state.ctr % 2
        legal_moves = node.state.get_legal_moves()
        res = []
        for move in legal_moves:
            new_state = node.state.copy()
            new_state.update_board(move, player ^ 1)
            child_node = MCTS_Node(new_state, node, move)
            res.append(child_node)
        return res

    def simulate(self, node):
        res = sum(node.rollout() for _ in range(MCTS.N))
        return sgn(res)
            
    def big_rollout(self):
        node_to_expand = self.root.select()
        res = node_to_expand.state.is_terminal()
        if not res:
            node_to_expand.children = self._create_children(node_to_expand)
            res = self.simulate(node_to_expand)

        node = node_to_expand
        while node.parent is None:
            node.update_res(res)
            node = node.parent

    def give_best_node(self):
        return max(self.root.state.children, lambda c: c.priority())
    
    def make_best_move(self):
        best_node = self.give_best_node()
        self.root = best_node
        return best_node.move

class MCTS_Player(Player):
    def __init__(self, depth=100):
        root = MCTS_Node(Connect4State(), None, None)
        self.mcts = MCTS(root)
        self.depth = depth

    def make_move(self, state):
        if state.ctr > 2:
            self.mcts.root = self.mcts.root.give_child_with_move(state.last_move)
        for _ in range(self.depth):
            self.mcts.big_rollout()
        
        best = self.mcts.make_best_move()
        state.last_move = best
        return best



