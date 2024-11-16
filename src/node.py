class Node:
    def __init__(self, node_ID, state, parent, action:float, depth, cost:float, heuristic:float, value:int):
        self.node_ID = node_ID
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.value = value

    def __eq__(self, other) -> bool:
        return self.state == other.state
    
