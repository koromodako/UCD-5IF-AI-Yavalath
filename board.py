# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    board.py
# date:    2016-10-30
# author:  paul dautry (16201434)
# purpose:
#   This file contains the implementation of Board class which represent a 
#   Yavalath board with associated game state data. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  IMPORTS
#==============================================================================
#==============================================================================
#  FUNCTIONS/CLASSES
#==============================================================================
class Board(object):
    """Board"""
    # players IDs
    PR_1=1
    PR_2=2
    # board size
    SIDE=9
    # end game states
    EG_DRAW=0
    EG_WIN=1
    EG_LOSE=2
    EG_NEXT=3
    def __init__(self):
        """__init__"""
        super(Board, self).__init__()
        self.reset()

    def reset(self):
        """reset"""
        self.board = [
            -1,-1,-1,-1, 0, 0, 0, 0, 0,
            -1,-1,-1, 0, 0, 0, 0, 0, 0,
            -1,-1, 0, 0, 0, 0, 0, 0, 0,
            -1, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0,-1,
             0, 0, 0, 0, 0, 0, 0,-1,-1,
             0, 0, 0, 0, 0, 0,-1,-1,-1,
             0, 0, 0, 0, 0,-1,-1,-1,-1
        ]
        self.nxt_pl = self.PR_1
        self.fst_mv_taken = False
        self.mv_count = 0
        self.latest_mv = None

    def next_player(self):
        """next_player"""
        return self.nxt_pl

    def move_count(self):
        """move_count"""
        return self.mv_count

    def take_first_move(self):
        """take_first_move"""
        self.fst_mv_taken = True
        return self.latest_mv

    def print_line(self, ridx, indent):
        """print_line"""
        print(' '*indent, end='')
        for i in range(0,self.SIDE):
            v=self.board[ridx*self.SIDE+i]
            if v!=-1:
                c=' '
                if v==self.PR_1:
                    c='X'
                elif v==self.PR_2:
                    c='O'
                print('| {} '.format(c), end='')
        print('|')

    def print(self):
        """print"""
        print('         / \\ / \\ / \\ / \\ / \\')
        self.print_line(0, 8) 
        print('       / \\ / \\ / \\ / \\ / \\ / \\')
        self.print_line(1, 6)
        print('     / \\ / \\ / \\ / \\ / \\ / \\ / \\')
        self.print_line(2, 4)
        print('   / \\ / \\ / \\ / \\ / \\ / \\ / \\ / \\')
        self.print_line(3, 2)
        print(' / \\ / \\ / \\ / \\ / \\ / \\ / \\ / \\ / \\')
        self.print_line(4, 0)
        print(' \\ / \\ / \\ / \\ / \\ / \\ / \\ / \\ / \\ /')
        self.print_line(5, 2)
        print('   \\ / \\ / \\ / \\ / \\ / \\ / \\ / \\ /')
        self.print_line(6, 4)
        print('     \\ / \\ / \\ / \\ / \\ / \\ / \\ /')
        self.print_line(7, 6)
        print('       \\ / \\ / \\ / \\ / \\ / \\ /')
        self.print_line(8, 8)
        print('         \\ / \\ / \\ / \\ / \\ /')

    def is_playable(self, r, c):
        """is_playable"""
        valid = False
        y = c
        for k in range(0,9):
            v = self.board[r*self.SIDE+k] 
            if v != -1:
                y -= 1
                if y == 0:
                    if v == 0:
                        y = k
                        valid = True
                    break
        return (valid, r, y)

    def do(self, x, y):
        """do"""
        self.board[x*self.SIDE+y] = self.nxt_pl
        self.nxt_pl = (self.PR_1 if self.nxt_pl == self.PR_2 else self.PR_2)
        self.mv_count += 1
        self.latest_mv = (x,y)

    def ai_do(self, x, y, pl):
        """ai_do"""
        self.board[x*self.SIDE+y] = pl 

    def ai_undo(self, x, y):
        """ai_undo"""
        self.board[x*self.SIDE+y] = 0

    def ai_board_lines(self, pl):
        board_lines = [ '' for i in range(0,3*self.SIDE) ]
        # fill lines and columns
        for x in range(0,9):
            for y in range(0,9):
                v = self.board[x*self.SIDE+y]
                if v != -1:
                    if v == pl:
                        board_lines[x] += '1'
                        board_lines[self.SIDE+y] += '1'
                    else:
                        board_lines[x] += '0'
                        board_lines[self.SIDE+y] += '0'
        # fill diagonals
        for c in range(4,9):
            for r in range(0,9):
                y = c - r
                if y >= 9 or y < 0: 
                    break
                if self.board[r*self.SIDE+y] == pl:
                    board_lines[2*self.SIDE+c-4] += '1'
                else:
                    board_lines[2*self.SIDE+c-4] += '0'
        for r in range(1,5):
            for c in range(0,9):
                x = r + c
                y = self.SIDE-1-c
                if x >= 9 or x < 0 or y >= 9 or y < 0:
                    break 
                if self.board[x*self.SIDE+y] == pl:
                    board_lines[3*self.SIDE-r] += '1'
                else:
                    board_lines[3*self.SIDE-r] += '0'
        # return lines
        return board_lines

    def end_game(self):
        """end_game"""
        # -- initialise variables
        (x,y) = self.latest_mv
        pl = self.board[x*self.SIDE+y]
        mx_seq = 0
        seq = 1
        k = 1
        # -- check draw
        if self.fst_mv_taken and self.mv_count == 62:
            return self.EG_DRAW
        elif not self.fst_mv_taken and self.mv_count == 61:
            return self.EG_DRAW
        # -- check for a winner or a loser
        # ---- check line
        while True:
            if y+k >= 9: 
                break
            if self.board[x*self.SIDE+y+k] != pl:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if y-k < 0:
                break
            if self.board[x*self.SIDE+y-k] != pl:
                break
            seq += 1
            k += 1
        mx_seq = max(mx_seq, seq)
        seq = 1
        # ---- check column
        k = 1
        while True:
            if x+k >= 9:
                break
            if self.board[(x+k)*self.SIDE+y] != pl:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if x-k < 0:
                break
            if self.board[(x-k)*self.SIDE+y] != pl:
                break
            seq += 1
            k += 1
        mx_seq = max(mx_seq, seq)
        seq = 1
        # ---- check diagonal
        k = 1
        while True:
            if x+k >= 9 or y-k < 0: 
                break
            if self.board[(x+k)*self.SIDE+y-k] != pl:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if x-k < 0 or y+k >= 9: 
                break
            if self.board[(x-k)*self.SIDE+y+k] != pl:
                break
            seq += 1
            k += 1
        mx_seq = max(mx_seq, seq)
        # -- determine case
        if mx_seq >= 4:
            return self.EG_WIN
        elif mx_seq == 3:
            return self.EG_LOSE
        return self.EG_NEXT
            
