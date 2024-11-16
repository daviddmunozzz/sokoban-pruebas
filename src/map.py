'''
    Module Name: map
    Author name: David Muñoz Escribano
    Realase: 08-10-2024
    Module version: 1.0
    Module description: This module satisfies the proposed task 1 of the sokoban game. It contains
    the class Map that represents the map of the game and the methods to generate the hash of the level

'''
import hashlib  # Import the hashlib module to use the MD5 algorithm

'''
    Method Name: hashMD5
    Description: Method to generate the hash of the level using the MD5 algorithm
    Return value: str, hash of the level
'''
def hashMD5(string) -> str:
    return (hashlib.md5(str(string).encode()).hexdigest()).upper()

from node import Node

'''
    Class Name: Map
    Author name: David Muñoz Escribano
    Realase: 08-10-2024
    Class version: 1.0
    Class description: This class encapsulates the attributes and methods to represent the map of the game. 
'''
class Map:
    '''
        Method Name: __init__
        Description: Constructor of the class Map and attributes defition
        Return value: None
    '''
    def __init__(self, level) -> None:
        self.level = level       # Level of the game, command parameter
        
        self.ID = ' '            # Hash of the level

        self.rows = 0            # Number of rows
        self.columns = 0         # Number of columns

        self.wallList = []       # List of walls (#)
        self.player = ()         # Player (@)
        self.boxList = []        # List of boxes ($)
        self.targetList = []     # List of targets (.)

        self.map = []            # Map of the game
        self.empty_map = []      # Map of the game without player and boxes

        self.dictionary = {}     # Dictionary to store ID and position of the player and boxes

    '''
        Method Name: define_grid
        Name of the original author: David Muñoz Escribano
        Description: Method to define the grid of the game, it iterates in the level if it finds a '\n' 
        it increments the number of rows and resets the number of columns, else it increments the number of columns.
        Return value: list initialized with ' ' in all positions
    '''
    def define_grid(self) -> list:
        NR = 1    # Number of rows
        NC = 0    # Number of columns
        maxNC = 0 # Maximum number of columns
        for i in self.level:
            if i == '\n':
                NR += 1
                if NC > maxNC: # Check if NC is bigger than maxNC, if it is, update maxNC
                    maxNC = NC
                NC = 0
            else:
                NC += 1  
        
        self.rows = NR          # Save in the rows instance variable
        self.columns = maxNC    # Save in the columns instance variable
        
        # Create and initialize the grid introducing ' ' in all positions
        return [[' ' for col in range(maxNC)] for row in range(NR)]

    '''
        Method Name: make_map
        Name of the original author: David Muñoz Escribano
        Description of the Method: Method to create the map of the game, calling define_grid method to store
        characters in their i,j positions and save them in a list. Also, it calls hashMD5 method to generate the hash of the level.
        Return value: None
    '''
    def make_map(self) -> None:
        grid = self.define_grid()

        i = 0 # Iterator of rows
        j = 0 # Iterator of columns

        # w is the iterator of the level, when it finds a '\n' it increments i and resets j
        for w in range(len(self.level)):
            if self.level[w] == '\n':
                i += 1
                j = 0
            else: # If it is not a '\n' it stores the character in the grid and storing in the corresponding list
                if self.level[w] == '#':
                    grid[i][j] = self.level[w]
                    self.wallList.append((i, j)) 
                    j += 1
                elif self.level[w] == '@':
                    grid[i][j] = self.level[w]
                    self.player = (i, j)
                    j += 1
                elif self.level[w] == '$':
                    grid[i][j] = self.level[w]
                    self.boxList.append((i, j))
                    j += 1
                elif self.level[w] == '.':
                    grid[i][j] = self.level[w]
                    self.targetList.append((i, j))
                    j += 1
                elif self.level[w] == '*':          
                    grid[i][j] = self.level[w]
                    self.boxList.append((i,j))
                    self.targetList.append((i,j))
                    j += 1
                elif self.level[w] == '+':
                    grid[i][j] = self.level[w]
                    self.player = (i, j)
                    self.targetList.append((i, j))
                    j += 1
                elif self.level[w] == ' ':
                    grid[i][j] = self.level[w]    
                    j += 1

        # Save the grid in the map instance variable
        self.map = grid  
        self.empty_map = grid
        self.blank_map()
        # Generate the hash ID of the level
        self.ID = hashMD5((str(self.player) + str(self.boxList)).replace(' ', ''))
        # Store the ID in the dictionary
        self.dictionary = {self.ID: (self.player, self.boxList)}

    '''
        Method Name: show_map_elements
        Name of original author: David Muñoz Escribano
        Description: Method to print the map of the game
        Return value: None
    '''
    def show_map_elements(self) -> None:
        print(("ID:" + self.ID + 
            "\n\tRows:" + str(self.rows) +
            "\n\tColumns:" + str(self.columns) +  
            "\n\tWalls:" + str(self.wallList) +
            "\n\tTargets:" + str(self.targetList) +
            "\n\tPlayer:" + str(self.player) +
            "\n\tBoxes:" + str(self.boxList) + "\n").replace(' ', ''))                

    '''
        Method Name: successors
        Name of the original author: David Muñoz Escribano
        Description: Method to generate the successors of the actual state of the game, it checks the possible movements
        of the mutable elements (player and boxes) and stores them in a list of tuples with the direction, the hash of the 
        new state and cost. 
        The get_moves method returns a list of tuples <direction, successor(i,j), current(i,j)>, e.g. ('U',(i-2,j),(i-1,j))
        In case of boxes, it is necessary to update the position of each box in the boxList, the current position will be 
        the player position and the successor position will be the new position of the box, in the player case, the successor
        position will be the new position of the player, and boxes will remain the same.
        Return value: list of successors by tuple <direction, new state, cost>
    '''
    def successors(self) -> list:
        movements = self.get_moves()
        successors = [] 
        cost = 1
        for move in movements:
            if move[0].isupper():
                boxList_successors = self.boxList.copy()
                it = self.get_index(move[2])           # Get the index of the box in the boxList
                boxList_successors[it] = move[1]
                boxList_successors = sorted(boxList_successors)             # Sort the boxList
                ID = hashMD5((str(move[2]) + str(boxList_successors)).replace(' ', '')) # Generate the hash of the new state
                successors.append((move[0], ID, cost))
                #self.dictionary = {ID: (move[2], boxList_successors)} 
                self.dictionary[ID] = (move[2], boxList_successors) # Store the movement with the new ID
            else:
                ID = hashMD5((str(move[1]) + str(self.boxList)).replace(' ', ''))
                successors.append((move[0], ID, cost))
                self.dictionary[ID] = (move[1], self.boxList)
        return successors

    ''' 
        Method Name: get_index
        Name of the original author: David Muñoz Escribano
        Description: This method return the index that match with the movement
        Return value: int, index of the move in the boxList
    '''
    def get_index(self, move) -> int:
        try:
            return self.boxList.index(move)
        except ValueError:
            return -1

    '''
        Method Name: get_moves
        Name of the original author: David Muñoz Escribano
        Description: Method that returns the possible movements of the player and boxes, they differ in the first element
        in tuple (upper case for boxes and lower case for player). First of all it checks in the directions that it is possible
        to move, if in that direction there is a box, check again if it is possible to move the box in that direction.
        The order of the movements is Up, Right, Down and Left <u|U|r|R|d|D|l|L>.
        Return value: list of tuples <direction, successor(i,j), current(i,j)>
    '''
    def get_moves(self):
        i = self.player[0]
        j = self.player[1]
        movements = []   # Tuple: <direction, suc(i,j), current(i,j)>

        # Check Up
        if self.map[i-1][j] in (' ', '.') or self.map[i-1][j] in ('$', '*'):    
            if self.map[i-1][j] in ('$', '*'):
                if self.map[i-2][j] in (' ', '.'):
                    movements.append(('U', (i-2, j), (i-1, j)))
            else:
                movements.append(('u', (i-1, j), (i, j)))
        # Check Right
        if self.map[i][j+1] in (' ', '.') or self.map[i][j+1] in ('$', '*'):
            if self.map[i][j+1] in ('$', '*'):
                if self.map[i][j+2] in (' ', '.'):
                    movements.append(('R', (i, j+2), (i, j+1)))
            else:
                movements.append(('r', (i, j+1), (i, j)))
        # Check Down
        if self.map[i+1][j] in (' ', '.') or self.map[i+1][j] in ('$', '*'):
            if self.map[i+1][j] in ('$', '*'):
                if self.map[i+2][j] in (' ', '.'):
                    movements.append(('D', (i+2, j), (i+1, j)))
            else:
                movements.append(('d', (i+1, j), (i, j)))
        # Check Left
        if self.map[i][j-1] in (' ', '.') or self.map[i][j-1] in ('$', '*'):
            if self.map[i][j-1] in ('$', '*'):
                if self.map[i][j-2] in (' ', '.'):
                    movements.append(('L', (i, j-2), (i, j-1)))
            else:
                movements.append(('l', (i, j-1), (i, j)))
        
        return movements

    '''
        Method Name: show_successors
        Name of the original author: David Muñoz Escribano
        Description: Method to print the successors of the actual state of the game
        Return value: None
    '''
    def show_successors(self) -> None:
        print("ID:" + self.ID)
        for successor in self.successors():
            print("\t" + str(successor).replace('(', '[').replace(')', ']').replace(' ', '').replace("'", ""))
    
    '''
        Method Name: objective
        Name of the original author: David Muñoz Escribano
        Description: Method to check if the level is resolved, it iterates in the map and if it finds a '.' (target) it means that
        the level is not resolved.
        Return value: None
    '''
    def objective(self) -> bool:
        resolved = True
        for position in self.map:
            for element in position:
                if element == '$':
                    resolved = False
        return resolved

    def solve_sokoban(self, strategy, max_depth) -> None:
        fringe = []
        visited = []
        solution = False

        node_ID = [0]
        depth = 0
        cost = 0.00
        heuristic = 0.00
        value = 0.00
        fringe.append(Node(node_ID[0], self.ID, None, 'NOTHING', depth, cost, heuristic, value)) # Insert the root node in the fringe
        
        while fringe and not solution:
            node = fringe[0]
            self.update_map(node)
        
            if self.objective(): 
                solution = True
            if fringe[0].depth <= max_depth and node not in visited:
                visited.append(node)                
                expanded_nodes = self.expand(node, visited, strategy, node_ID)
                if expanded_nodes:
                    fringe.extend(expanded_nodes)                
            fringe.pop(0)

        if solution:
            self.make_path(node, visited)
        else:
            print("Solution not exists")
                
    def make_path(self, node, visited) -> list:
        path = []
        while node.parent is not None:
            path.insert(0, node)
            node = node.parent
        path.insert(0, node)
        self.print_path(path)
   
    def print_path(self, path) -> None:
        print(str(repr(self.level)).replace("'", ""))
        for node in path:
            if node.parent is not None:
                print(f"{node.node_ID},{node.state},{node.parent.node_ID},{node.action},{node.depth},{node.cost},{node.heuristic},{node.value}")
            else:
                print(f"{node.node_ID},{node.state},None,{node.action},{node.depth},{node.cost},{node.heuristic},{node.value}")

    def expand(self, node, visited, strategy, node_ID) -> list:
        S = self.successors()
        nodes = []
        
        for suc in S: # suc = ('U', ID, cost)
            node_ID[0] += 1
            if self.check_visited(suc[1],visited):                                               # Value depends on algorithm (BFS, DFS, UC)                                                                                    
                nodes.append(Node(node_ID[0], suc[1], node, suc[0], node.depth +1, node.cost + 1.00, node.heuristic, self.calculate_value(node,strategy)))
            if nodes:
                nodes.sort(key=lambda n: (n.value, n.node_ID)) 
        return nodes
    
    def check_visited(self, state, visited) -> bool:
        for node in visited:
            if node.state == state: 
                return False
        return True

    def calculate_value(self, node, strategy) -> int:
        value = 0.00
        if strategy == 'BFS':
            value = float(node.value) + 1.00 
        elif strategy == 'DFS':
            value = float(node.value) / (node.depth + 1)
        elif strategy == 'UC':
            value = float(node.cost)
        return value
    
    def blank_map(self) -> None:
        for i in range(self.rows):
            for j in range(self.columns):
                if self.map[i][j] in ('@', '$'):
                    self.empty_map[i][j] = ' '
                elif self.map[i][j] in ('+', '*'):
                    self.empty_map[i][j] = '.'

    def update_map(self, node) -> None: 
        suc_positions = self.dictionary[node.state] # P0 = player position, P1 = boxList positions
        new_player = suc_positions[0]
        new_boxList = suc_positions[1]

        self.map = [row.copy() for row in self.empty_map]

        # Update the player position
        if self.map[new_player[0]][new_player[1]] == '.':
            self.map[new_player[0]][new_player[1]] = '+'
        else:
            self.map[new_player[0]][new_player[1]] = '@' 
        self.player = new_player

        # Update box positions
        for box in new_boxList:
            if self.map[box[0]][box[1]] == '.':
                self.map[box[0]][box[1]] = '*'
            else:
                self.map[box[0]][box[1]] = '$'  
        self.boxList = new_boxList
