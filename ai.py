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
import sys
from board  import Board
#==============================================================================
#  GLOBALS
#==============================================================================
INFINITY = sys.maxsize
#==============================================================================
#  FUNCTIONS/CLASSES
#==============================================================================
class AI(object):
    """AI player"""
    # ai levels
    LVL_1 = 3
    LVL_2 = 4
    LVL_3 = 5
    # ai modes
    MODE_SIMPLE  = 1
    MODE_KILLER  = 2
    MODE_HISTORY = 3
    # static evaluation patterns
    PATTERNS = {
    #   pattern: weight
    # best patterns
        'xxxx' : 50,
        '0xx0x': 5,
        'x0xx0': 5,
        '0x00x': 2,
        'x00x0': 2,
    # worst patterns
        '0xx0' :-1,
        '0x0x0':-1,
        'xxx'  :-40
    }

    def __init__(self, pseudo, level, mode):
        """Constructs the AI object"""
        super(AI, self).__init__()
        self.pseudo = pseudo
        self.level = level
        self.mode = mode

    def name(self):
        """Returns the name of the AI player"""
        return self.pseudo

    def next_move(self, board):
        """Computes the next move to be played by the AI player
           arguments:
               board -- Board object
        """
        (i, j, score) = self.negamax(board, board.next_player(), self.level-1, -INFINITY, INFINITY)
        return (i, j)

    def negamax(self, board, player, h, a, b):
        """Recursive negamax algorithm with alpha-beta pruning
           arguments:
               board -- Board object
               h     -- lower level of the tree to be searched (zero-based)
               a     -- alpha bound
               b     -- beta bound
        """
        # -- debug
        #print('%snegamax(board, h=%d, a=%d, b=%d)' % ('\t'*h, h, a, b))
        # -- debug
        if h == 0:
            return (None, None, self.static_eval(board, player))
        else:
            m_i = m_j = None
            for i in range(0,9):
                for j in range(0,9):
                    if board.ai_is_playable(i,j):
                        # -- debug
                        #print('%sconsidering(%d,%d)' % (h*'\t', i, j))
                        # -- debug
                        board.ai_do(i,j)
                        (ri, rj, rscore) = self.negamax(board, board.next_player(), h-1, -b, -a)
                        score = - rscore
                        if score >= b:
                            board.ai_undo(i,j)
                            return (i, j, score)
                        if score > a:
                            a = score
                            m_i = i
                            m_j = j
                        board.ai_undo(i,j)
            return (m_i, m_j, a)

    def static_eval(self, board, player):
        """Computes the score of the given player on the given board
           arguments:
               board  -- Board object
               player -- Integer value of the player defined by Board class
        """
        # -- debug
        #print('static_eval(board, player=%d)' % player) 
        # -- debug
        board_lines = board.ai_board_lines()
        score = p1_score = p2_score = 0
        # first player score
        for line in board_lines:
            for pattern, weight in self.PATTERNS.items():
                p = pattern.replace('x', str(Board.PR_1))
                p1_score += line.count(p) * weight
        # second player score
        for line in board_lines:
            for pattern, weight in self.PATTERNS.items():
                p = pattern.replace('x', str(Board.PR_2))
                p2_score += line.count(p) * weight
        # compute final score
        if player == Board.PR_1:
            score = p1_score - p2_score
        else:
            score = p2_score - p1_score
        # -- debug
        #print('p1=%d, p2=%d, score=%d' % (p1_score, p2_score, score))
        # -- debug
        return score

