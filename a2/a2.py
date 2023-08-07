from __future__ import annotations
from typing import Optional
from a2_support import UserInterface, TextInterface
from constants import *

# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackboard changelog. 
__version__ = 1.0

# Uncomment this function when you have completed the Level class and are ready
# to attempt the Model class.

# def load_game(filename: str) -> list['Level']:
#     """ Reads a game file and creates a list of all the levels in order.
    
#     Parameters:
#         filename: The path to the game file
    
#     Returns:
#         A list of all Level instances to play in the game
#     """
#     levels = []
#     with open(filename, 'r') as file:
#         for line in file:
#             line = line.strip()
#             if line.startswith('Maze'):
#                 _, _, dimensions = line[5:].partition(' - ')
#                 dimensions = [int(item) for item in dimensions.split()]
#                 levels.append(Level(dimensions))
#             elif len(line) > 0 and len(levels) > 0:
#                 levels[-1].add_row(line)
#     return levels


# Write your classes here


def main():
    # Write your code here
    pass

if __name__ == '__main__':
    main()
