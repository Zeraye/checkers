# importing libraries
import pygame
import math
import constants as const

# pawn drawing function
def draw_pawns(screen, board):
    for row in range(8):
        for col in range(8):
            if len(board[row][col]) != 0: board[row][col][0].draw_pawn(screen)

# board drawing function
def draw_board(screen):
    for row in range(8):
        for col in range(8):
            if (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0): pygame.draw.rect(screen, const.GREEN, (const.SQUARE_SIDE * row, const.SQUARE_SIDE * col, const.SQUARE_SIDE, const.SQUARE_SIDE))
            else: pygame.draw.rect(screen, const.WHITE, (const.SQUARE_SIDE * row, const.SQUARE_SIDE * col, const.SQUARE_SIDE, const.SQUARE_SIDE))

# highlighting clicked square
def hl_click(screen, click_pos):
    if click_pos != None: pygame.draw.rect(screen, const.BLUE, (click_pos[0] * const.SQUARE_SIDE, click_pos[1] * const.SQUARE_SIDE, const.SQUARE_SIDE, const.SQUARE_SIDE), math.ceil(const.SQUARE_SIDE / 30))

# main drawing function
def draw_main(screen, board, click_pos):
    screen.fill(const.BLACK)
    draw_board(screen)
    draw_pawns(screen, board)
    hl_click(screen, click_pos)
    pygame.display.flip()
