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
    PATTERNS = {
    #   pattern: weight
    # good patterns
        '01101': 1,
        '10110': 1,
        '01001': 1,
        '10010': 1,
    # bad patterns
        '0110' :-1,
        '01010':-1
    }

    def __init__(self):
        """__init___"""
        super(AI, self).__init__()

    def name(self):
        """name"""
        return "AI"

    def next_move(self, board):
        """next_move"""
        pass
    
    def static_eval(self, board):
        """static_eval"""
        board_lines = board.ai_board_lines()
        print(board_lines)
        score = 0
        for line in board_lines:
            for pattern, weight in self.PATTERNS.items():
                score += line.count(pattern) * weight
        return score

