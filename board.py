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
    # impossible moves
    IMPOSSIBLE = [
        (0,0), (0,1), (0,2), (0,3), (1,0), 
        (1,1), (1,2), (2,0), (2,1), (3,0), 
        (5,8), (6,7), (6,8), (7,6), (7,8), 
        (7,8), (8,5), (8,6), (8,7), (8,8)
    ]

    def __init__(self):
        """Constructs the Board object"""
        super(Board, self).__init__()
        self.reset()

    def reset(self):
        """Resets board object"""
        self.board = [
            [-1,-1,-1,-1, 0, 0, 0, 0, 0],
            [-1,-1,-1, 0, 0, 0, 0, 0, 0],
            [-1,-1, 0, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0,-1],
            [ 0, 0, 0, 0, 0, 0, 0,-1,-1],
            [ 0, 0, 0, 0, 0, 0,-1,-1,-1],
            [ 0, 0, 0, 0, 0,-1,-1,-1,-1]
        ]
        self.nxt_player = self.PR_1
        self.fst_mv_taken = False
        self.mv_count = 0
        self.latest_mv = None

    def next_player(self):
        """Returns next player as an integer"""
        return self.nxt_player

    def move_count(self):
        """Returns count of moves as an integer"""
        return self.mv_count

    def take_first_move(self):
        """Takes first move as second player move
           returns:
               the latest move which is a couple of integer values
        """
        self.fst_mv_taken = True
        return self.latest_mv

    def print_line(self, ridx, indent):
        """Prints a line of the board
           arguments:
               ridx   -- integer value of the index of the row (zero-based)
               indent -- integer value of the indent to be printed before the 
                         row
        """
        print(' '*indent, end='')
        for i in range(0,self.SIDE):
            v=self.board[ridx][i]
            if v!=-1:
                c=' '
                if v==self.PR_1:
                    c='X'
                elif v==self.PR_2:
                    c='O'
                print('| {} '.format(c), end='')
        print('|')

    def print(self):
        """Prints the board"""
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
        """Assert the existance and availability of the position
           arguments:
               r -- row to be considered (zero-based)
               c -- number of playable column (one-based)
           returns:
               a tuple of a boolean and two integer values indicating if the 
               cell can be played and the real coordinates of the cell in the
               matrix
        """
        valid = False
        y = c
        for k in range(0, self.SIDE):
            v = self.board[r][k]
            if v != -1:
                y -= 1
                if y == 0:
                    if v == 0:
                        y = k
                        valid = True
                    break
        return (valid, r, y)

    def update_next_player(self):
        """Updates next player value swapping from 1-to-2 and 2-to-1"""
        if self.nxt_player == self.PR_2:
            self.nxt_player = self.PR_1
        else:
            self.nxt_player = self.PR_2

    def do(self, x, y):
        """Executes a real move and updates board-related variables
           arguments:
               x -- index of the row in the matrix (zero-based)
               y -- index of the column in the matrix (zero-based)
        """
        self.board[x][y] = self.nxt_player
        self.update_next_player()
        self.mv_count += 1
        self.latest_mv = (x,y)

    def end_game(self):
        """Detects if the board is in an end game state"""
        # -- initialise variables
        (x,y) = self.latest_mv
        player = self.board[x][y]
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
            if y+k >= self.SIDE:
                break
            if self.board[x][y+k] != player:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if y-k < 0:
                break
            if self.board[x][y-k] != player:
                break
            seq += 1
            k += 1
        mx_seq = max(mx_seq, seq)
        seq = 1
        # ---- check column
        k = 1
        while True:
            if x+k >= self.SIDE:
                break
            if self.board[x+k][y] != player:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if x-k < 0:
                break
            if self.board[x-k][y] != player:
                break
            seq += 1
            k += 1
        mx_seq = max(mx_seq, seq)
        seq = 1
        # ---- check diagonal
        k = 1
        while True:
            if x+k >= self.SIDE or y-k < 0:
                break
            if self.board[x+k][y-k] != player:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if x-k < 0 or y+k >= self.SIDE:
                break
            if self.board[x-k][y+k] != player:
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

    def ai_is_playable(self, x, y):
        """Tests if the cell is playable for the AI
           arguments:
               x -- index of the row in the matrix (zero-based)
               y -- index of the column in the matrix (zero-based)
        """
        return (self.board[x][y]==0)

    def ai_do(self, x, y):
        """Simulates a move for the AI. Can be reverted using ai_undo.
           arguments:
               x -- index of the row in the matrix (zero-based)
               y -- index of the column in the matrix (zero-based)
        """
        self.board[x][y] = self.nxt_player
        self.update_next_player()

    def ai_undo(self, x, y):
        """Reset a move simulated for the AI. Can be reverted using ai_do.
           arguments:
               x -- index of the row in the matrix (zero-based)
               y -- index of the column in the matrix (zero-based)
        """
        self.board[x][y] = 0
        self.update_next_player()

    def ai_board_lines(self):
        """Convert the board matrix to a list of strings representing 
           lines, the two diagonals of the hexagonal board
        """
        board_lines = [ '' for i in range(0,3*self.SIDE) ]
        # convert lines and columns
        for x in range(0, self.SIDE):
            for y in range(0, self.SIDE):
                v = self.board[x][y]
                if v != -1:
                    board_lines[x] += str(v)
                    board_lines[self.SIDE+y] += str(v)
        # convert diagonals
        for c in range(4, self.SIDE):
            for r in range(0, self.SIDE):
                y = c - r
                if y >= self.SIDE or y < 0:
                    break
                board_lines[2*self.SIDE+c-4] += str(self.board[r][y])
        for r in range(1,5):
            for c in range(0, self.SIDE):
                x = r + c
                y = self.SIDE-1-c
                if x >= self.SIDE or x < 0 or y >= self.SIDE or y < 0:
                    break
                board_lines[3*self.SIDE-r] += str(self.board[x][y])
        return board_lines

