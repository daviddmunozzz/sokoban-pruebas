'''
    Module Name: sokoban
    Author name: David Muñoz Escribano
    Realase: 08-10-2024
    Module version: 1.0
    Module description: This is the main module of the sokoban game. It contains the method sokoban_exec to execute the game

'''
from parser import get_parser # Import the get_parser method from the parser module
from task1 import Map         # Import the Map class from the task1 module

'''
    Method name: sokoban_exec
    Name of the original author: David Muñoz Escribano
    Description: Collect the arguments from the command line and execute the corresponding task
'''
def sokoban_exec() -> None:
    # Get the arguments parser
    parser = get_parser()

    # Parse the arguments
    args = parser.parse_args()

    # Replace \n from the level string by carriage return in code
    level = args.level.replace('\\n', '\n')
    
    # Check the task to execute
    if args.task == 'T1':
        map = Map(level)        # Create the map object
        map.make_map()          # Make the map
        print(map.to_String())  # Print the map

''' 
    Main method to execute the sokoban game
'''
if __name__ == '__main__':
    sokoban_exec()