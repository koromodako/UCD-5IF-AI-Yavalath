# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    yavalath.py
# date:    2016-10-30
# author:  paul dautry (16201434)
# purpose:
#
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
    def __init__(self, p1=AI(), p2=Player("HUMAN")):
        super(Yavalath, self).__init__()
        self.board = Board()
        self.p1 = p1
        self.p2 = p2

    def run(self):
        # -- reset game board
        self.board.reset()
        # -- loop while game is not over
        eg = Board.EG_NEXT
        while eg == Board.EG_NEXT:
            # -- select player and ask for a move
            x = y = None
            mvc = self.board.move_count()
            print('---------------------------------------------')
            if self.board.next_player() == Board.PR_1:
                print(' TURN: {} - PLAYER: {}'.format(mvc, self.p1.name()))
                print('---------------------------------------------')
                self.board.print()
                (x,y) = self.p1.next_move(self.board)
            else:
                print(' TURN: {} - PLAYER: {}'.format(mvc, self.p2.name()))
                print('---------------------------------------------')
                self.board.print()
                (x,y) = self.p2.next_move(self.board)
            # -- execute move
            self.board.do(x,y)
            # -- check end game clause
            eg = self.board.end_game()
        # -- print game result
        print('---------------------------------------------')
        print('[GAME OVER]> ', end='')
        if eg == Board.EG_DRAW:
            print('This is a draw!')
        elif eg == Board.EG_WIN:
            if self.board.next_player() == Board.PR_1:
                print('{} wins'.format(self.p2.name()))
            else:
                print('{} wins'.format(self.p1.name()))
        else:
            if self.board.next_player() == Board.PR_1:
                print('{} loses'.format(self.p2.name()))
            else:
                print('{} loses'.format(self.p1.name()))
        print('---------------------------------------------')
        self.board.print()
