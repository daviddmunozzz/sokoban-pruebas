class Node:
    def __init__(self, ID, parent, state, value, depth, cost, heuristic, action):
        self.ID = ID
        self.parent = parent
        self.state = state
        self.action = action
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.value = value

