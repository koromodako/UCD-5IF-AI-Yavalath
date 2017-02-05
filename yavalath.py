# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    yavalath.py
# date:    2016-10-30
# author:  paul dautry (16201434)
# purpose:
#   This file contains the implementation of the Yavalath class which
#   contains Yavalath's game logic and game's main loop.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  IMPORTS
#==============================================================================
from board  import Board
from player import Player
from ai     import AI
#==============================================================================
#  FUNCTIONS/CLASSES
#==============================================================================
class Yavalath(object):
    """Yavalath"""
    def __init__(self, p1=Player("Bob"), p2=Player("Stuart")):
        """Constructs Yavalath object"""
        super(Yavalath, self).__init__()
        self.board = Board()
        self.p1 = p1
        self.p2 = p2

    def run(self, verbose=True, detailed=False):
        """Starts game's main loop"""
        # -- reset game board
        self.board.reset()
        # -- loop while game is not over
        eg = Board.EG_NEXT
        while eg == Board.EG_NEXT:
            # -- select player and ask for a move
            x = y = None
            mvc = self.board.move_count
            if verbose:
                print('---------------------------------------------')
            if self.board.next_player == Board.PR_1:
                if verbose:
                    print(' TURN: {} - PLAYER: {}'.format(mvc, self.p1.name))
                    print('---------------------------------------------')
                    self.board.print(detailed)
                (x,y) = self.p1.next_move(self.board)
            else:
                if verbose:
                    print(' TURN: {} - PLAYER: {}'.format(mvc, self.p2.name))
                    print('---------------------------------------------')
                    self.board.print(detailed)
                (x,y) = self.p2.next_move(self.board)
            # -- execute move
            self.board.do(x,y)
            if verbose:
                self.board.print_pos(x,y)
            # -- check end game clause
            eg = self.board.end_game(x,y)
        # -- print game result
        if verbose:
            print('---------------------------------------------')
        winner = None
        if eg == Board.EG_DRAW:
            if verbose:
                print('This is a draw!')
        elif eg == Board.EG_WIN:
            if self.board.next_player == Board.PR_1:
                winner = self.p2.name
            else:
                winner = self.p1.name
        else:
            if self.board.next_player == Board.PR_1:
                winner = self.p1.name
            else:
                winner = self.p2.name
        if verbose:
            print('[GAME OVER]> %s wins !' % winner)
            print('---------------------------------------------')
            self.board.print()
        return winner
