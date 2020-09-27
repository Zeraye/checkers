# importing libraries
import pygame
import math
import constants as const
import variables as var

# pawn class
class Pawn:
    def __init__(self, row, col, color, type = 0):
        self.row = row
        self.col = col
        self.color = color
        self.type = type

    # getting pawn position
    def get_pos(self):
        return self.row, self.col

    # getting pawn type
    def get_type(self):
        return self.type

    # getting pawn color
    def get_color(self):
        return self.color

    # moving pawn
    def move(self, new_pos):
        self.row = new_pos[0]
        self.col = new_pos[1]

    # upgrading pawn to king
    def upgrade(self):
        self.type = 1

    # pawn drawing function
    def draw(self, screen):
        # checking color
        if self.color == 0: color = const.RED
        elif self.color == 1: color = const.BLACK
        # checking if pawn is king
        if self.type == 1: pygame.draw.circle(screen, const.YELLOW, (int(const.SQUARE_SIDE * (self.col + 0.5)), int(const.SQUARE_SIDE * (self.row + 0.5))), math.ceil(const.PAWN_RADIUS - 2))
        # drawing pawn
        pygame.draw.circle(screen, color, (int(const.SQUARE_SIDE * (self.col + 0.5)), int(const.SQUARE_SIDE * (self.row + 0.5))), int(const.PAWN_RADIUS), math.ceil(const.PAWN_RADIUS / 2))

    # deleting pawn
    def delete(self):
        var.pawns.remove(self)
        del self
