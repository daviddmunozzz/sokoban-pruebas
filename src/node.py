'''
    Module Name: node
    Author name: David Muñoz Escribano
    Realase: 17-11-2024
    Module version: 1.0
    Module description: This module contains the class Node, which represents a node in the search tree.
'''

'''
    Class Name: Node
    Author name: David Muñoz Escribano
    Realase: 17-11-2024
    Class version: 1.0
    Class description: It contains diferent attributes and methods to represent the node.
'''
class Node:
    def __init__(self, node_ID, state, parent, action, depth, cost, heuristic, strategy):
        self.node_ID = node_ID
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.value = self.calculate_value(strategy)
    '''
        Method Name: __eq__
        Name of the original author: David Muñoz Escribano
        Description: Checks if two nodes are equal, comparing their states.
        Return value: bool
    '''
    def __eq__(self, other) -> bool:
        return self.state == other.state
    '''
        Method Name: calculate_value
        Name of the original author: David Muñoz Escribano
        Description: Depends on the strategy of algorithm it calculates the value of the node.
        Return value: int, value of the node
    '''

    def calculate_value(self, strategy) -> int:
        value = 0.00
        if strategy == 'BFS':
            value = round((float(self.depth)), 2) 
        elif strategy == 'DFS':
            value = round((1 / (float(self.depth) + 1.00)), 2)
        elif strategy == 'UC':
            value = round((float(self.cost)), 2)
        return value
    
    '''
        Method Name: check_visited
        Name of the original author: David Muñoz Escribano
        Description: Checks that the state of the successor isn't in visited.
        Return value: bool      
    '''
    def check_visited(self, state, visited) -> bool:
        return all(node.state != state for node in visited)
