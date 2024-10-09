'''
    Module Name: parser
    Author name: David Muñoz Escribano
    Realase: 08-10-2024
    Module version: 1.0
    Module description: This module contains the method get_parser to get the arguments from the command line
'''
import argparse  # Import the argparse module to get the arguments from the command line

'''
    Method name: get_parser
    Name of the original author: David Muñoz Escribano
    Description: This method check and collect the arguments specified in the command line
    Return value: argparse.ArgumentParser, define an object that saves the arguments as attributes
'''
def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Arguments for sokoban') # Create the parser object
    parser.add_argument('task', type=str, help='Task to execute')
    parser.add_argument('-l', '--level', type=str, help='Level to execute')
    return parser