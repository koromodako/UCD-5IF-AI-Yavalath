#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    main.py
# date:    2016-10-30
# author:  paul dautry (16201434)
# purpose:
#   This file contains the implementation of the main menu of the game
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  IMPORTS
#==============================================================================
from yavalath       import Yavalath
from player         import Player
from ai             import AI
from move_generator import MoveGenerator
from random         import randint
#==============================================================================
#  GLOBALS
#==============================================================================
AI_NAMES = ['Joker', 'Aquaman', 'Superman', 'Batman', 'Spiderman']
IDX = -1
#==============================================================================
#  FUNCTIONS
#==============================================================================
def input_game_mode():
    while True:
        mode=input('[i] Enter a game mode: ')
        if len(mode) == 1:
            v = ord(mode)-48
            if v in [1,2,3]:
                return v
        print('[!] Invalid input. Expect a number in [1,3].')

def input_name(player_name):
    while True:
        name = input('[i] Enter a name for %s: ' % player_name)
        if len(name) > 0:
            return name
        else:
            print('[!] Invalid input. Name must not be empty.')

def input_level(ai_name):
    while True:
        level = input('[i] Enter a level for %s (AI): ' % ai_name)
        if len(level) == 1:
            v = ord(level)-48
            lvl = None
            if v == 1:
                lvl = AI.LVL_1
            elif v == 2:
                lvl = AI.LVL_2
            elif v == 3:
                lvl = AI.LVL_3
            if lvl is not None:
                print('[i] Level %d selected.' % v)
                return lvl
        print('[!] Invalid input. Expect a number in [1,3].')

def input_mode(ai_name):
    while True:
        mode = input('[i] Enter a mode for %s (AI): ' % ai_name)
        if len(mode) == 1:
            v = ord(mode)-48
            if v == 1:
                print('[i] Simple mode selected.')
                return MoveGenerator.MODE_SIMPLE
            elif v == 2:
                print('[i] Killer mode selected.')
                return MoveGenerator.MODE_KILLER
            elif v == 3:
                print('[i] History mode selected.')
                return MoveGenerator.MODE_HISTORY
        print('[!] Invalid input. Expect a number in [1,3].')

def input_p1_first(p1, p2):
    while True:
        answer = input('[i] Do you agree with %s playing first ? [y/n]: ' % 
            p1.name)
        if 'y' == answer:
            return True
        elif 'n' == answer:
            return False
        print('[!] Invalid input. Expect "y" or "n".')

def get_ai_name():
    global IDX
    i = -1
    while i == -1 or i == IDX:
        i = randint(0, len(AI_NAMES)-1)
    IDX = i
    return AI_NAMES[IDX]

#==============================================================================
#  MAIN SCRIPT
#==============================================================================
print("""
+-----------------------------------------------------------------------------+
|                           YAVALATH MAIN MENU                                |
+-----------------------------------------------------------------------------+
|                                GAME MODE                                    |
+-----------------------------------------------------------------------------+
|                                                                             |
|                          1. PLAYER vs. PLAYER                               |
|                          2. PLAYER vs. AI                                   |
|                          3.     AI vs. AI                                   |
|                                                                             |
+------------------------------------+----------------------------------------+
|              AI MODE               |                AI LEVEL                |
+------------------------------------+----------------------------------------+
|                                    |                                        |
|             1. SIMPLE              |              1. EASY                   |
|             2. KILLER              |              2. MEDIUM                 |
|             3. HISTORY             |              3. DIFFICULT              |
|                                    |                                        |
+------------------------------------+----------------------------------------+
""")
P1 = None
P2 = None
mode = input_game_mode()
print('[i] Game mode selected ', end='')
if mode == 1:
    print('PLAYER vs. PLAYER.')
    P1 = Player(input_name('player 1'))
    P2 = Player(input_name('player 2'))
elif mode == 2:
    print('PLAYER vs. AI.')
    P1 = Player(input_name('player'))
    p2_name = get_ai_name() 
    P2 = AI(p2_name,input_level(p2_name),input_mode(p2_name))
elif mode == 3:
    print('AI vs. AI.')
    p1_name = get_ai_name()
    P1 = AI(p1_name,input_level(p1_name),input_mode(p1_name))
    p2_name = get_ai_name()
    P2 = AI(p2_name,input_level(p2_name),input_mode(p2_name))
print("""
-------------------------------------------------------------------------------
""")
y=None
if input_p1_first(P1, P2):
    y=Yavalath(P1,P2)
else:
    y=Yavalath(P2,P1)
y.run()
