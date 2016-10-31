# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    player.py
# date:    2016-10-30
# author:  paul dautry (16201434)
# purpose:
#   This file contains the implementation of the Player class which represent 
#   a human player and contain all the logic needed to process user input.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  IMPORTS
#==============================================================================
from board  import Board
#==============================================================================
#  FUNCTIONS/CLASSES
#==============================================================================
class Player(object):
    """Player"""
    def __init__(self, pseudo):
        super(Player, self).__init__()
        self.pseudo = pseudo

    def name(self):
        return self.pseudo

    def next_move(self, board):
        valid = False
        x = y = None
        while not valid:
            mv = input('Enter your move: ')
            if board.move_count() == 1:
                if len(mv) == 1 and mv == 'X':
                    (x,y) = board.take_first_move()
                    break
            if len(mv) == 2:
                r=ord(mv[0])-65
                c=ord(mv[1])-48
                if r < 9 and r >= 0 and c <= 9 and c > 0:
                    (valid, x, y) = board.is_playable(r,c)
            if not valid:
                print('[!] Invalid input. Try again.')
        return (x, y)
        
