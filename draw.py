# importing libraries
import pygame
import math
import pawn
import constants as const
import variables as var
import functions as func

# pawn drawing function
def draw_pawns(screen):
    for pawn in var.pawns:
        pawn.draw(screen)

# board drawing function
def draw_board(screen):
    for row in range(8):
        for col in range(8):
            if (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0): pygame.draw.rect(screen, const.GREEN, (const.SQUARE_SIDE * row, const.SQUARE_SIDE * col, const.SQUARE_SIDE, const.SQUARE_SIDE))
            else: pygame.draw.rect(screen, const.WHITE, (const.SQUARE_SIDE * row, const.SQUARE_SIDE * col, const.SQUARE_SIDE, const.SQUARE_SIDE))

# highlighting clicked square
def highlight(screen, pos):
    if pos != None and func.find_pawn(pos) != None: pygame.draw.rect(screen, const.BLUE, (pos[1] * const.SQUARE_SIDE, pos[0] * const.SQUARE_SIDE, const.SQUARE_SIDE, const.SQUARE_SIDE), math.ceil(const.SQUARE_SIDE / 30))

# main drawing function
def draw_main(screen, pos):
    screen.fill(const.BLACK)
    draw_board(screen)
    draw_pawns(screen)
    highlight(screen, pos)
    pygame.display.flip()
