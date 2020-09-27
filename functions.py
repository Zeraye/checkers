# importing libraries
import pawn
import constants as const
import variables as var

# function for initializing pawns
def init_pawns():
    for row in range(8):
        for col in range(8):
            # two top rows
            if (row == 0 and col % 2 != 0) or (row == 1 and col % 2 == 0) or (row == 2 and col % 2 != 0): var.pawns.append(pawn.Pawn(row, col, 0))
            # two bottom rows
            elif (row == 5 and col % 2 == 0) or (row == 6 and col % 2 != 0) or (row == 7 and col % 2 == 0): var.pawns.append(pawn.Pawn(row, col, 1))

# function for getting row and col from mouse position
def get_rowcol(mouse_pos):
    return int(mouse_pos[1] / const.SQUARE_SIDE), int(mouse_pos[0] / const.SQUARE_SIDE)

# function for finding pawn by clicked position
def find_pawn(click_pos):
    for pawn in var.pawns:
        # pawn found
        if pawn.get_pos() == click_pos: return pawn
    # none pawn found
    return None

# managing move
def manage_move(old_click_pos, new_click_pos):
    # checking move legality
    # TODO: checking move legality
    if False:
        return False
    # managing capture
    # TODO: managing capture
    # move is legal and capturing is managed
    return True
