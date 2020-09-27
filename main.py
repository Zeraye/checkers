# importing libraries
import pygame
import draw
import functions as func
import constants as const
import variables as var

# initializing all pygame functions
pygame.init()
# window creating
WINDOW = pygame.display.set_mode((const.SIDE, const.SIDE))
# setting title caption to window
pygame.display.set_caption('Checkers')

# main function
def main(screen):
    # inital game settings
    pos = None
    func.init_pawns()
    # creating clock
    clock = pygame.time.Clock()
    # main loop
    while True:
        clock.tick(const.FPS)
        for event in pygame.event.get():
            # closing game
            if event.type == pygame.QUIT:
                pygame.quit()
            # mouse click detection
            if event.type == pygame.MOUSEBUTTONDOWN:
                # getting old clicked position
                old_pos = pos
                # getting old clicked pawn
                old_pawn = func.find_pawn(old_pos)
                # getting new clicked position
                pos = func.get_rowcol(pygame.mouse.get_pos())
                # getting new clicked pawn
                pawn = func.find_pawn(pos)
                # clicking twice unhighligh square
                if old_pos == pos: pos = None
                # disable clicking on enemy pawn
                elif pawn != None and pawn.get_color() != var.player1: pos = None
                # when click before was on pawn and now on empty square
                elif old_pawn != None and pawn == None:
                    # managing move (move legality, capturing), changing player
                    if func.manage_move(old_pos, pos): var.player1 = not var.player1
                    # unhighlighing
                    pos = None
        # drawing board and objects
        draw.draw_main(screen, pos)

# running game
if __name__ == '__main__':
    main(WINDOW)
