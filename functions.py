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
def count_pawns(pawns, color):
    pieces = kings = 0
    for pawn in pawns:
        if pawn.get_color() == color and pawn.get_type() == 0: pieces += 1
        if pawn.get_color() == color and pawn.get_type() == 1: kings += 1
    return pieces, kings

# function for checking every possible move
def possible_moves(pawns, player):
    moves = []
    # for every pawn on board
    for pawn in pawns:
        pawn_pos = pawn.get_pos()
        pawn_type = pawn.get_type()
        if not player: start_row = max(pawn_pos[0] + 1, 0) if pawn_type == 0 else max(pawn_pos[0] - 2, 0)
        else: start_row = max(pawn_pos[0] - 1, 0) if pawn_type == 0 else max(pawn_pos[0] - 2, 0)
        start_col = max(pawn_pos[1] - 2, 0)
        end_row = min(pawn_pos[0] + 3, 8)
        end_col = min(pawn_pos[1] + 3, 8)
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
        # for row in range(0, 8):
        #     for col in range(0, 8):
            # giving possible moves for next player
                if (player == pawn.get_color()):
                    # add move if is legal
                    if check_move((pawn_pos), (row, col), pawns) != False:
                        moves.append([pawn_pos, (row, col)])
    return moves

# checking move legality
def check_move(old_pos, new_pos, pawns):
    new_pawn = find_pawn(new_pos, pawns)
    old_pawn = find_pawn(old_pos, pawns)
    # checking whether clicking on pawn
    if new_pawn != None: return False
    # checking whether pawn is not king
    if old_pawn.get_type() == 0:
        # checking whether pawn is moving back
        if (old_pawn.get_type() == 0 and old_pawn.get_color() == 0 and old_pos[0] >= new_pos[0]) or \
            (old_pawn.get_color() == 1 and old_pos[0] <= new_pos[0]): return False
    # moving by 2 square diagonally (capturing)
    if abs(old_pos[0] - new_pos[0]) == 2 and abs(old_pos[1] - new_pos[1]) == 2:
        # calculating square betweem old and new position
        mid_pos = ((old_pos[0] + new_pos[0]) / 2,(old_pos[1] + new_pos[1]) / 2)
        mid_pawn = find_pawn(mid_pos, pawns)
        # checking whether is enemy pawn in mid_pos
        if mid_pawn == None or \
            old_pawn.get_color() == mid_pawn.get_color(): return False
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
    new_pawn = find_pawn(new_pos, pawns)
    if (new_pawn.get_color() == 0 and new_pos[0] == 7) or \
        (new_pawn.get_color() == 1 and new_pos[0] == 0):
            new_pawn.upgrade()
    # correct move, change player
    return not player1

# function for calculating advantage
def calc_advantage(pawns, old_pawns):
    # advantage
    cookies = 0
    n_poss_mvs_human = len(possible_moves(pawns, 1))
    n_poss_mvs_ai = len(possible_moves(pawns, 0))
    o_poss_mvs_human = len(possible_moves(old_pawns, 1))
    o_poss_mvs_ai = len(possible_moves(old_pawns, 0))
    n_pws_human = count_pawns(pawns, 1)
    n_pws_ai = count_pawns(pawns, 0)
    o_pws_human = count_pawns(old_pawns, 1)
    o_pws_ai = count_pawns(old_pawns, 0)
    # ai winning
    if n_poss_mvs_human == 0: cookies += math.inf
    # ai losing
    elif n_poss_mvs_ai == 0: cookies -= math.inf
    # upgrading ai pawn
    if n_pws_ai[1] > o_pws_ai[1]: cookies += 10
    # upgrading human's pawn
    elif n_pws_human[1] > o_pws_human[1]: cookies -= 10
    # capturing human's upgraded pawn
    if n_pws_human[1] < o_pws_human[1]: cookies += 7
    # having upgraded pawn captured
    elif n_pws_ai[1] < o_pws_ai[1]: cookies -= 7
    # capturing enemy's pawn
    if n_pws_human[0] < o_pws_human[0]: cookies += 5
    # having pawn captured
    elif n_pws_ai[0] < o_pws_ai[0]: cookies -= 5
    # counting moves
    if n_poss_mvs_human < o_poss_mvs_human: cookies += 1
    elif n_poss_mvs_human > o_poss_mvs_human: cookies -= 1
    if n_poss_mvs_ai < o_poss_mvs_ai: cookies -= 1
    elif n_poss_mvs_ai > o_poss_mvs_ai: cookies += 1
    # returning advantage
    return cookies

def make_best_move(pawns, player1):
    max_depth = 3
    print('[AI] START CALCULATING...')
    best_score = -math.inf
    best_move = None
    original_pawns = copy.deepcopy(pawns)
    move_count = 0
    move_sum = len(possible_moves(pawns, player1))
    for move in possible_moves(pawns, player1):
        move_count += 1
        copy_pawns = copy.deepcopy(pawns)
        manage_move(move[0], move[1], pawns, player1)
        # score = score_counting(not player1, pawns, copy_pawns, 0)
        score = minimax(False, 0, max_depth, pawns, copy_pawns)
        pawns = copy_pawns
        if score > best_score:
            best_score = score
            best_move = move
        elif score == best_score and random.randint(1, 10) > 3:
            best_score = score
            best_move = move
        print('[AI] MOVES ANALYZED {} / {}'.format(move_count, move_sum))
    manage_move(best_move[0], best_move[1], original_pawns, player1)
    print('[AI] BEST SCORE', best_score)
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
        elif score == best_score and random.randint(1, 10) > 3:
            best_score = score
    return sum_score + best_score

# minimax algorithm
def minimax(is_max, depth, max_depth, pawns, copy_pawns):
    if count_pawns(pawns, 0)[0] + count_pawns(pawns, 0)[1] == 0 or \
        count_pawns(pawns, 1)[0] + count_pawns(pawns, 1)[1] == 0 or \
        depth == max_depth:
            return calc_advantage(pawns, copy_pawns)
    if is_max:
        best_score = -math.inf
        for move in possible_moves(pawns, 1):
            copy_pawns = copy.deepcopy(pawns)
            manage_move(move[0], move[1], pawns, False)
            score = minimax(False, depth + 1, max_depth, pawns, copy_pawns)
            pawns = copy_pawns
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in possible_moves(pawns, 0):
            copy_pawns = copy.deepcopy(pawns)
            manage_move(move[0], move[1], pawns, True)
            score = minimax(True, depth + 1, max_depth, pawns, copy_pawns)
            pawns = copy_pawns
            best_score = min(score, best_score)
        return best_score
