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
def find_pawn(pos):
    for pawn in var.pawns:
        # pawn found
        if pawn.get_pos() == pos: return pawn
    # none pawn found
    return None

# function for checking every possible move
def possible_moves():
    # for every pawn on board
    for pawn in var.pawns:
        # checking every position
        for row in range(8):
            for col in range(8):
                # add move if is legal
                if check_move((pawn.get_pos()), (row, col)) != False: var.possible_moves.append(((pawn.get_pos()), (row, col)))

# checking move legality
def check_move(old_pos, new_pos):
    # checking whether clicking on same type pawn
    if find_pawn(new_pos) != None and find_pawn(old_pos).get_color() == find_pawn(new_pos).get_color(): return False
    # checking whether pawn is not king
    if find_pawn(old_pos).get_type() == 0:
        # checking whether pawn is moving back
        if find_pawn(old_pos).get_type() == 0 and \
            (find_pawn(old_pos).get_color() == 0 and \
            old_pos[0] >= new_pos[0]) or \
            (find_pawn(old_pos).get_color() == 1 and \
            old_pos[0] <= new_pos[0]): return False
    # moving by 2 square diagonally (capturing)
    if abs(old_pos[0] - new_pos[0]) == 2 and abs(old_pos[1] - new_pos[1]) == 2:
        # calculating square betweem old and new position
        mid_pos = ((old_pos[0] + new_pos[0]) / 2,(old_pos[1] + new_pos[1]) / 2)
        # checking whether is enemy pawn in mid_pos
        if find_pawn(mid_pos) == None or \
            find_pawn(old_pos).get_color() == find_pawn(mid_pos).get_color(): return False
        # returning mid_pos when move is capturing
        return mid_pos
    # moving more by 1 square diagonally (after checking move by 2 square)
    elif abs(old_pos[0] - new_pos[0]) != 1 or abs(old_pos[1] - new_pos[1]) != 1: return False
    # correct move
    return True

# function for managing move
def manage_move(old_pos, new_pos):
    # checking move legality
    move = check_move(old_pos, new_pos)
    # return False when move is illegal
    if not move: return move
    # capturing pawn
    if type(move) is not bool:
        # deleting captured pawn
        find_pawn(move).delete()
        # player after capturing can move again
        var.player1 = not var.player1
    # moving pawn
    find_pawn(old_pos).move(new_pos)
    # upgrading pawn do king
    if (find_pawn(new_pos).get_color() == 0 and new_pos[0] == 7) or \
        (find_pawn(new_pos).get_color() == 1 and new_pos[0] == 0): find_pawn(new_pos).upgrade()
    ###################################################
    possible_moves()
    print('possible moves ', len(var.possible_moves))
    var.possible_moves = []
    ###################################################
    # correct move
    return True
