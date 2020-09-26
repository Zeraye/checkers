# importing libraries
import pawn
import constants as const

# function to create board
def start_board():
    # creating empty board
    board = [[[] for col in range(8)] for row in range(8)]
    # filling empty board for the first time
    for row in range(8):
        for col in range(8):
            if (row == 0 and col % 2 != 0) or (row == 1 and col % 2 == 0) or (row == 2 and col % 2 != 0): board[row][col].append(pawn.Pawn(row, col, 0, 0))
            elif (row == 5 and col % 2 == 0) or (row == 6 and col % 2 != 0) or (row == 7 and col % 2 == 0): board[row][col].append(pawn.Pawn(row, col, 1, 0))
    return board

# function for getting row and col from mouse position
def get_rowcol(mouse_pos):
    return int(mouse_pos[0] / const.SQUARE_SIDE), int(mouse_pos[1] / const.SQUARE_SIDE)
