#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    main.py
# date:    2016-10-30
# author:  paul dautry (16201434)
# purpose:
#   This file contains the implementation of the 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  IMPORTS
#==============================================================================
from yavalath import Yavalath
from player   import Player
from ai       import AI
#==============================================================================
#  FUNCTIONS
#==============================================================================
def input_name(player_name):
    while True:
        name = input('Enter a name for {}: '.format(player_name))
        if len(name) > 0:
            return name
        else:
            print('[!] Invalid input. Name must not be empty.')
#==============================================================================
#  MAIN SCRIPT
#==============================================================================
print("""
-------------------------------------------------------------------------------
                            YAVALATH MAIN MENU
-------------------------------------------------------------------------------

                           1. PLAYER vs. PLAYER
                           2. PLAYER vs. AI
                           3.     AI vs. AI
""")
P1 = None
P2 = None
while True:
    mode=ord(input('Enter your choice: '))-48
    if mode == 1:
        P1 = Player(input_name('player 1'))
        P2 = Player(input_name('player 2'))
        break
    elif mode == 2:
        P1 = Player(input_name('player'))
        P2 = AI()
        break
    elif mode == 3:
        P1 = AI()
        P2 = AI()
        break
    else:
        print('[!] Invalid input. Try again.')
print("""
-------------------------------------------------------------------------------
""")
y=Yavalath(P1,P2)
y.run()