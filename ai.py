# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    ai.py
# date:    2016-10-30
# author:  koromodako (16201434)
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
# static evaluation patterns
PATTERNS = {
#   pattern: weight
# best patterns
    'xx0x' : 20,
    'x0xx' : 20,
    '0xx0x': 10, # required by assignment instructions
    'x0xx0': 10, # required by assignment instructions
    '0x00x': 5,  # required by assignment instructions
    'x00x0': 5,  # required by assignment instructions
# worst patterns
    '0xx0' :-10, # required by assignment instructions
    '0x0x0':-10  # required by assignment instructions
}
# 'infinite' scores
MAX_SCORE =  100
MIN_SCORE = -100
#==============================================================================
#  FUNCTIONS/CLASSES
#==============================================================================
class AI(object):
    """AI player"""
    # ai levels
    LVL_1 = 3
    LVL_2 = 4
    LVL_3 = 5

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
        if h == 0:
            return (None, None, self.static_eval(board, player))
        else:
            moves = self.move_generator.gen_moves(h)
            m_i = None
            for mv in moves:
                if board.ai_is_playable(mv[0], mv[1]):
                    board.do(mv[0], mv[1])
                    end_game = board.end_game(mv[0], mv[1])
                    if end_game == board.EG_NEXT:
                        (ri, rj, rscore) = self.negamax(board,
                                                board.next_player, h-1, -b, -a)
                    board.undo(mv[0], mv[1])
                    if end_game == board.EG_WIN:
                        score = MAX_SCORE
                    elif end_game == board.EG_LOSE:
                        score = MIN_SCORE
                    elif end_game == board.EG_NEXT:
                        score = - rscore
                    else: # board.EG_DRAW
                        score = 0
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
            return (m_i, m_j, a)

    def static_eval(self, board, player):
        """Computes the score of the given player on the given board
           arguments:
               board  -- Board object
               player -- Integer value of the player defined by Board class
        """
        self.static_evals[-1] += 1
        board_lines = board.ai_board_lines()
        score = p1_score = p2_score = 0
        # first player score
        for line in board_lines:
            for pattern, weight in PATTERNS.items():
                p = pattern.replace('x', str(Board.PR_1))
                p1_score += line.count(p) * weight
        # second player score
        for line in board_lines:
            for pattern, weight in PATTERNS.items():
                p = pattern.replace('x', str(Board.PR_2))
                p2_score += line.count(p) * weight
        # compute final score
        if player == Board.PR_1:
            score = p1_score - p2_score
        else:
            score = p2_score - p1_score
        return score

    def reset(self):
        """Resets internal counters"""
        self.static_evals = []
