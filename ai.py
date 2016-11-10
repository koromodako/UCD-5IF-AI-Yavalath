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
from move_generator import MoveGenerator
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
    # static evaluation patterns
    PATTERNS = {
    #   pattern: weight
    # best patterns
        'xxxx' : 50,
        'xx0x' : 5,
        'x0xx' : 5,
        '0xx0x': 5, # required by assignment instructions
        'x0xx0': 5, # required by assignment instructions
        '0x00x': 2, # required by assignment instructions
        'x00x0': 2, # required by assignment instructions
    # worst patterns
        '0xx0' :-1, # required by assignment instructions
        '0x0x0':-1, # required by assignment instructions
        'xxx'  :-20
    }

    def __init__(self, name, level, mode):
        """Constructs the AI object"""
        super(AI, self).__init__()
        self.name = name
        self.level = level
        self.move_generator = MoveGenerator(mode)
        self.static_evals = []

    def next_move(self, board):
        """Computes the next move to be played by the AI player
           arguments:
               board -- Board object
        """
        self.static_evals.append(0)
        self.move_generator.reset(self.level)
        (i, j, score) = self.negamax(board,
            board.next_player, self.level-1, -INFINITY, INFINITY)
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
            moves = self.move_generator.gen_moves(h)
            # -- debug
            #print(moves)
            # -- debug
            m_i = None
            for mv in moves:
                if board.ai_is_playable(mv[0], mv[1]):
                    # -- debug
                    #print('%sconsidering(%d,%d)' % (h*'\t', i, j))
                    # -- debug
                    board.do(mv[0], mv[1])
                    (ri, rj, rscore) = self.negamax(board,
                        board.next_player, h-1, -b, -a)
                    board.undo(mv[0], mv[1])
                    score = - rscore
                    if score >= b:
                        self.move_generator.incr_pruning(mv, h)
                        return (mv[0], mv[1], score)
                    if score > a:
                        a = score
                        m_i = mv[0]
                        m_j = mv[1]
            if m_i is None:
                m_i = mv[0]
                m_j = mv[1]
            # -- debug
            #print('alpha=%d, beta=%d, score=%d, h=%d' % (a,b,score,h))
            #board.print()
            # --debug
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
        self.static_evals[-1] += 1
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

    def reset(self):
        """Resets internal counters"""
        self.static_evals = []
