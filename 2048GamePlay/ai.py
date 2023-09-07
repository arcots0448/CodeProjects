from __future__ import absolute_import, division, print_function
import copy, random
from game import Game
import pdb

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        # (state, score)
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO, DONE
        if self.children:
            return False
        else:
            return True

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move
    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        if depth == 0:
            return

        if node.player_type == 0:
            for direction in MOVES:
                state_copy = self.simulator.current_state()
                if self.simulator.move(direction) == False:
                    continue
                child = Node(self.simulator.current_state(), 1)
                self.build_tree(child, depth-1)
                node.children.append((direction,child))
                self.simulator.set_state(state_copy[0],state_copy[1])
        else:
            open_tiles = self.simulator.get_open_tiles()
            for tile in open_tiles:
                state_copy = self.simulator.current_state()
                i = tile[0]
                j = tile[1]
                self.simulator.tile_matrix[i][j] = 2
                child = Node(self.simulator.current_state(), 0)
                self.build_tree(child, depth-1)
                node.children.append((None,child))
                self.simulator.set_state(state_copy[0], state_copy[1])

    def build_tree_ec(self, node=None, depth=0, alpha=float('-inf'), beta=float('inf')):
        if depth == 0:
            return

        if node.player_type == 0:
            for direction in MOVES:
                state_copy = self.simulator.current_state()
                if self.simulator.move(direction) == False:
                    continue
                child = Node(self.simulator.current_state(), 1)

                node.children.append((direction,child))
                score = self.build_tree_ec(child, depth-1, alpha, beta)
                self.simulator.set_state(state_copy[0],state_copy[1])
                if score != None:
                    alpha = max(alpha, score)
                if beta <= alpha:
                    break  # beta cutoff
            return alpha
        else:
            open_tiles = self.simulator.get_open_tiles()
            for tile in open_tiles:
                state_copy = self.simulator.current_state()
                i = tile[0]
                j = tile[1]
                self.simulator.tile_matrix[i][j] = 2
                child = Node(self.simulator.current_state(), 0)

                node.children.append((None,child))
                score = self.build_tree_ec(child, depth-1, alpha, beta)
                self.simulator.set_state(state_copy[0], state_copy[1])
                if score != None:
                    beta = min(beta, score)
                if beta <= alpha:
                    break  # alpha cutoff
            return beta


    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same

        # Check if node is a terminal node
        if node.is_terminal():
            # If it's a terminal node, return the node's value
            return (None, node.state[1])

        # Check if node is a MAX_PLAYER
        elif node.player_type == 0:
            # If it's a MAX_PLAYER, find the child with the maximum value
            best_direction = None
            max_value = float('-inf')
            for child in (node.children):
                trash, child_value = self.expectimax(child[1])
                if child_value > max_value:
                    best_direction = child[0]
                    max_value = child_value
            return (best_direction, max_value)

        # If it's a CHANCE_PLAYER, find the average of the child values
        else:
            expected_value = 0
            num_children = len(node.children)
            for child in node.children:
                trash, child_value = self.expectimax(child[1])
                expected_value += child_value * (1/num_children)
            return (None, expected_value)

    
    def expectimax_ec(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same

        # Check if node is a terminal node
        if node.is_terminal():
            # If it's a terminal node, return the node's value
            return (None, node.state[1])

        # Check if node is a MAX_PLAYER
        elif node.player_type == 0:
            # If it's a MAX_PLAYER, find the child with the maximum value
            best_direction = None
            max_value = float('-inf')
            for child in (node.children):
                trash, child_value = self.expectimax_ec(child[1])
                #child_value *= self.heuristic(child[1])
                if child_value > max_value:
                    best_direction = child[0]
                    max_value = child_value
            return (best_direction, max_value)

        # If it's a CHANCE_PLAYER, find the average of the child values
        else:
            expected_value = 0
            num_children = len(node.children)
            for child in node.children:
                trash, child_value = self.expectimax_ec(child[1])
                #child_value *= self.heuristic(child[1])
                expected_value += child_value * (1/num_children)
            return (None, expected_value)

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        #print(self.simulator.tile_matrix,self.simulator.board_size)
        self.build_tree_ec(self.root, 7)
        direction, _ = self.expectimax_ec(self.root)
        return direction

