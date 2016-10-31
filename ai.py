# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    ai.py
# date:    2016-10-30
# author:  paul dautry (16201434)
# purpose:
#   This file contains the implementation of AI class which simulate the 
#   behaviour of an AI player. Alpha-beta negamax with(out) killer heuristic 
#   or history heuristic.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  IMPORTS
#==============================================================================
from board  import Board
#==============================================================================
#  FUNCTIONS/CLASSES
#==============================================================================
class AI(object):
    """AI"""
    def __init__(self):
        super(AI, self).__init__()

    def name(self):
        return "AI"

    def next_move(self, board):
        pass
        