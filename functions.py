# importing libraries
import random
import copy
import math
import pawn
import constants as const

# function for initializing pawns
def init_pawns(pawns):
    for row in range(8):
        for col in range(8):
            # two top rows
            if (row == 0 and col % 2 != 0) or (row == 1 and col % 2 == 0) or \
                (row == 2 and col % 2 != 0): pawns.append(pawn.Pawn(row, col, 0))
            # two bottom rows
            elif (row == 5 and col % 2 == 0) or (row == 6 and col % 2 != 0) or \
                (row == 7 and col % 2 == 0): pawns.append(pawn.Pawn(row, col, 1))
    # returning initialized pawns
    return pawns

# function for getting row and col from mouse position
def get_rowcol(mouse_pos):
    return int(mouse_pos[1] / const.SQUARE_SIDE), int(mouse_pos[0] / const.SQUARE_SIDE)

# function for finding pawn by clicked position
def find_pawn(pos, pawns):
    for pawn in pawns:
        # pawn found
        if pawn.get_pos() == pos: return pawn
    # none pawn found
    return None

# function for counting pawns in one color
def count_pawns(color, pawns, type = 0):
    i = 0
    for pawn in pawns:
        if pawn.get_color() == color and pawn.get_type() == type: i += 1
    return i

# function for counting upgraded pawns in one color
def count_upgraded(color, pawns):
    i = 0
    for pawn in pawns:
        if pawn.get_type() == 1: i += 1
    return i


# function for checking every possible move
def possible_moves(pawns, player):
    moves = []
    # for every pawn on board
    for pawn in pawns:
        # checking every position
        for row in range(8):
            for col in range(8):
                # giving possible moves for next player
                if (player == pawn.get_color()):
                    # add move if is legal
                    if check_move((pawn.get_pos()), (row, col), pawns) != False:
                        moves.append([pawn.get_pos(), (row, col)])
    return moves

# checking move legality
def check_move(old_pos, new_pos, pawns):
    # checking whether clicking on pawn
    if find_pawn(new_pos, pawns) != None: return False
    # checking whether pawn is not king
    if find_pawn(old_pos, pawns).get_type() == 0:
        # checking whether pawn is moving back
        if find_pawn(old_pos, pawns).get_type() == 0 and \
            (find_pawn(old_pos, pawns).get_color() == 0 and \
            old_pos[0] >= new_pos[0]) or \
            (find_pawn(old_pos, pawns).get_color() == 1 and \
            old_pos[0] <= new_pos[0]): return False
    # moving by 2 square diagonally (capturing)
    if abs(old_pos[0] - new_pos[0]) == 2 and abs(old_pos[1] - new_pos[1]) == 2:
        # calculating square betweem old and new position
        mid_pos = ((old_pos[0] + new_pos[0]) / 2,(old_pos[1] + new_pos[1]) / 2)
        # checking whether is enemy pawn in mid_pos
        if find_pawn(mid_pos, pawns) == None or \
            find_pawn(old_pos, pawns).get_color() == find_pawn(mid_pos, pawns).get_color(): return False
        # returning mid_pos when move is capturing
        return mid_pos
    # moving more by 1 square diagonally (after checking move by 2 square)
    elif abs(old_pos[0] - new_pos[0]) != 1 or abs(old_pos[1] - new_pos[1]) != 1: return False
    # correct move
    return True

# function for managing move
def manage_move(old_pos, new_pos, pawns, player1):
    # checking move legality
    move = check_move(old_pos, new_pos, pawns)
    # return False when move is illegal
    if not move: return player1
    # capturing pawn
    if type(move) is not bool:
        # deleting captured pawn
        find_pawn(move, pawns).delete(pawns)
    # moving pawn
    find_pawn(old_pos, pawns).move(new_pos)
    # upgrading pawn do king
    if (find_pawn(new_pos, pawns).get_color() == 0 and new_pos[0] == 7) or \
        (find_pawn(new_pos, pawns).get_color() == 1 and new_pos[0] == 0):
            find_pawn(new_pos, pawns).upgrade()
    # correct move, change player
    return not player1

################################################################################
################################# AI MANAGEMENT ################################
################################################################################

# function for calculating advantage
def calc_advantage(pawns, old_pawns):
    advantage = 0
    # winning
    if count_pawns(1, pawns) == 0 or len(possible_moves(pawns, 1)) == 0: advantage += math.inf
    # losing
    if count_pawns(0, pawns) == 0 or len(possible_moves(pawns, 0)) == 0: advantage -= math.inf
    # upgrading own pawn
    if count_upgraded(0, pawns) > count_upgraded(0, old_pawns): advantage += 7
    # upgrading enemy's pawn
    if count_upgraded(1, pawns) > count_upgraded(1, old_pawns): advantage -= 7
    # capturing enemy's upgraded pawn
    if count_pawns(1, pawns, 1) < count_pawns(1, old_pawns, 1): advantage += 5
    # having upgraded pawn captured
    if count_pawns(0, pawns, 1) < count_pawns(0, old_pawns, 1): advantage -= 5
    # capturing enemy's pawn
    if count_pawns(1, pawns) < count_pawns(1, old_pawns): advantage += 3
    # having pawn captured
    if count_pawns(0, pawns) < count_pawns(0, old_pawns): advantage -= 3
    # having more possible moves after move or enemy has less possible moves
    if len(possible_moves(pawns, 0)) > len(possible_moves(old_pawns, 0)) or \
        len(possible_moves(pawns, 1)) < len(possible_moves(old_pawns, 1)):
            advantage += 1
    # having less possible moves after move or enemy has more possible moves
    if len(possible_moves(pawns, 0)) < len(possible_moves(old_pawns, 0)) or \
        len(possible_moves(pawns, 1)) > len(possible_moves(old_pawns, 1)):
            advantage -= 1
    # returning advantage
    return advantage

def make_best_move(pawns, player1, max_depth):
    print('[AI] MAX DEPTH = {}'.format(max_depth))
    print('[AI] START CALCULATING...')
    best_score = -math.inf
    best_move = None
    original_pawns = copy.deepcopy(pawns)
    moves_number = len(possible_moves(pawns, player1))
    move_number = 0
    for move in possible_moves(pawns, player1):
        move_number += 1
        copy_pawns = copy.deepcopy(pawns)
        manage_move(move[0], move[1], pawns, player1)
        # score = minimax(False, 0, max_depth, pawns, copy_pawns)
        score = score_counting(not player1, pawns, copy_pawns, 0)
        # print('[AI] SCORE {}'.format(score))
        pawns = copy_pawns
        if score > best_score:
            best_score = score
            best_move = move
        elif score == best_score and random.randint(1, 2) % 2 == 0:
            best_score = score
            best_move = move
        print('[AI] MOVES ANALYZED {} %'.format(int((move_number * 100) / moves_number)))
    print('[AI] BEST MOVE FOUND \n')
    print('[AI] BEST SCORE {}'.format(best_score))
    manage_move(best_move[0], best_move[1], original_pawns, player1)
    return (not player1), original_pawns

# score counting function
def score_counting(player1, pawns, copy_pawns, sum_score):
    sum_score += calc_advantage(pawns, copy_pawns)
    best_score = math.inf
    for move in possible_moves(pawns, player1):
        copy_pawns = copy.deepcopy(pawns)
        manage_move(move[0], move[1], pawns, player1)
        score = calc_advantage(pawns, copy_pawns)
        pawns = copy_pawns
        if score < best_score:
            best_score = score
        elif score == best_score and random.randint(1, 2) % 2 == 0:
            best_score = score
    return sum_score + best_score

# # minimax algorithm
# def minimax(is_max, depth, max_depth, pawns, copy_pawns):
#     if count_pawns(0, pawns) == 0 or count_pawns(1, pawns) == 0 or depth == max_depth:
#         return calc_advantage(pawns, copy_pawns)
#     if is_max:
#         best_score = -math.inf
#         for move in possible_moves(pawns, 1):
#             copy_pawns = copy.deepcopy(pawns)
#             manage_move(move[0], move[1], pawns, False)
#             score = minimax(False, depth + 1, max_depth, pawns, copy_pawns)
#             pawns = copy_pawns
#             best_score = max(score, best_score)
#         return best_score
#     else:
#         best_score = math.inf
#         for move in possible_moves(pawns, 0):
#             copy_pawns = copy.deepcopy(pawns)
#             manage_move(move[0], move[1], pawns, True)
#             score = minimax(True, depth + 1, max_depth, pawns, copy_pawns)
#             pawns = copy_pawns
#             best_score = min(score, best_score)
#         return best_score
