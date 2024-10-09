'''
    Module Name: task1
    Author name: David Muñoz Escribano
    Realase: 08-10-2024
    Module version: 1.0
    Module description: This module satisfies the proposed task 1 of the sokoban game. It contains
    the class Map that represents the map of the game and the methods to generate the hash of the level

'''
import hashlib  # Import the hashlib module to use the MD5 algorithm

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

    '''
        Method Name: hashMD5
        Description: Method to generate the hash of the level using the MD5 algorithm
        Return value: None
    '''
    def hashMD5(self) -> None:  
        string = (str(self.player) + str(self.boxList)).replace(' ', '')    # Concatenate the player position and the box list
        self.ID = (hashlib.md5(str(string).encode()).hexdigest()).upper() # Generate the hash, convert to uppercase and store it in the ID attribute
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
                    j += 1
                elif self.level[w] == '+':
                    grid[i][j] = self.level[w]
                    j += 1
                elif self.level[w] == ' ':
                    grid[i][j] = self.level[w]    
                    j += 1
        # Now the instance has the position of the player and boxes and can hash the level
        self.hashMD5()

    '''
        Method Name: to_String
        Name of original author: David Muñoz Escribano
        Description: Method to print the map of the game
        Return value: str, summary of the map
    '''
    def to_String(self) -> str:
        return ("ID:" + self.ID + 
                "\nRows:" + str(self.rows) +
                "\nColumns:" + str(self.columns) +
                "\nWalls:" + str(self.wallList) +
                "\nTargets:" + str(self.targetList) +
                "\nPlayer:" + str(self.player) +
                "\nBoxes:" + str(self.boxList) + "\n").replace(' ', '')
                
