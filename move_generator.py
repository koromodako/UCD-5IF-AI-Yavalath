# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    move_generator.py
# date:    2016-11-09
# author:  paul dautry (16201434)
# purpose:
#   This file contains the implementation of MoveGenerator class which
#   generates moves accordingly to the selected mode.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  IMPORTS
#==============================================================================
from board  import Board
#==============================================================================
#  FUNCTIONS/CLASSES
#==============================================================================
class MoveGenerator(object):
    """MoveGenerator"""
    # move generator modes
    MODE_SIMPLE  = 1
    MODE_KILLER  = 2
    MODE_HISTORY = 3

    def __init__(self, mode):
        """Constructs the MoveGenerator object"""
        super(MoveGenerator, self).__init__()
        self.mode = mode
        self.hash = {}
        self.moves = []
        # generate moves without impossible coordinates
        for i in range(0, Board.SIDE):
            for j in range(0, Board.SIDE):
                if (i,j) not in Board.IMPOSSIBLE:
                    self.moves.append((i,j))

    def reset(self, h):
        """Resets internal structure according to the mode"""
        self.hash = {}
        if self.mode == self.MODE_KILLER:
            for k in range(0, h):
                self.hash[k] = {}
                for move in self.moves:
                    self.hash[k][move] = 0
        elif self.mode == self.MODE_HISTORY:
            for move in self.moves:
                self.hash[move] = 0

    def gen_moves(self, h):
        """Generates moves accordingly to its mode
           arguments:
               h -- height for which moves should be generated
        """
        s = None
        if self.mode == self.MODE_SIMPLE:
            return self.moves
        elif self.mode == self.MODE_KILLER:
            s = sorted(self.hash[h].items(), key=lambda x: -x[1])
        elif self.mode == self.MODE_HISTORY:
            s = sorted(self.hash.items(), key=lambda x: -x[1])
        return [ v[0] for v in s ]

    def incr_pruning(self, move, h):
        """Updates pruning structure"""
        # -- debug
        #print('incr_pruning(move=%s, h=%d)' % (move, h))
        # -- debug
        if self.mode == self.MODE_KILLER:
            self.hash[h][move] += 1
        elif self.mode == self.MODE_HISTORY:
            self.hash[move] += 1
