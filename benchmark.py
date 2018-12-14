#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    benchmark.py
# date:    2016-11-10
# author:  koromodako (16201434)
# purpose:
#   This file contains the implementation of the benchmarking executed to get
#   game statistics
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  IMPORTS
#==============================================================================
from yavalath       import Yavalath
from player         import Player
from ai             import AI
from move_generator import MoveGenerator
import cProfile
import sys
#==============================================================================
#  GLOBALS
#==============================================================================
ITER = 1
PROFILE = False
PART = False
LEVELS = [ AI.LVL_1, AI.LVL_2, AI.LVL_3 ]
MODES = [
    MoveGenerator.MODE_SIMPLE,
    MoveGenerator.MODE_KILLER,
    MoveGenerator.MODE_HISTORY
]
AI_1 = []
AI_2 = []
for lvl in LEVELS:
    for mode in MODES:
        AI_1.append(AI('%d%d-1' % (lvl,mode), lvl, mode))
        AI_2.append(AI('%d%d-2' % (lvl,mode), lvl, mode))
#==============================================================================
#  FUNCTIONS
#==============================================================================
def benchmark_game(ai1,ai2):
    print('[benchmark]> Current config: %s vs. %s' % (ai1.name, ai2.name))
    for it in range(0,ITER):
        ai1.reset()
        ai2.reset()
        game = Yavalath(ai1,ai2)
        res = game.run(verbose=False)
        se1 = ai1.static_evals
        se2 = ai2.static_evals
        lse1 = len(se1)
        lse2 = len(se2)
        mse1 = mse2 = 0
        for se in se1:
            mse1 += se
        for se in se2:
            mse2 += se
        print('[benchmark]> %d;%s;%d;%d;%d'%(it,res,lse1+lse2,mse1/lse1,mse2/lse2))

def benchmark():
    print('[benchmark]> Benchmarking 3x3 configurations %d times each.' % ITER)
    print('[benchmark]> Results format: iteration;winner;tour_count;'
          'avg_stat_eval_p1;avg_stat_eval_p2')
    for ai1 in AI_1:
        for ai2 in AI_2:
            benchmark_game(ai1,ai2)
#==============================================================================
#  MAIN SCRIPT
#==============================================================================
for k in range(1,len(sys.argv)):
    arg = sys.argv[k]
    if '--profile' in arg:
        PROFILE=True
    if '--iter=' in arg:
        ITER=int(arg.split('=')[-1])
    if '--part' in arg:
        PART=True

if not PART:
    if PROFILE:
        cProfile.run('benchmark()')
    else:
        benchmark()
else:
    benchmark_game(AI_1[7],AI_2[8])
    benchmark_game(AI_1[8],AI_2[0])
    benchmark_game(AI_1[8],AI_2[1])
    benchmark_game(AI_1[8],AI_2[2])
    benchmark_game(AI_1[8],AI_2[3])
    benchmark_game(AI_1[8],AI_2[4])
    benchmark_game(AI_1[8],AI_2[5])
    benchmark_game(AI_1[8],AI_2[6])
    benchmark_game(AI_1[8],AI_2[7])
    benchmark_game(AI_1[8],AI_2[8])
