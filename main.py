# importing libraries
import pygame
import draw
import functions as func
import constants as const

# initializing all pygame functions
pygame.init()
# window creating
WINDOW = pygame.display.set_mode((const.SIDE, const.SIDE))
# setting title caption to window
pygame.display.set_caption('Checkers')

# main function
def main(screen):
    # inital game settings
    max_depth = 1
    pawns = []
    player1 = True
    pos = None
    pawns = func.init_pawns(pawns)
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
                old_pawn = func.find_pawn(old_pos, pawns)
                # getting new clicked position
                pos = func.get_rowcol(pygame.mouse.get_pos())
                # getting new clicked pawn
                pawn = func.find_pawn(pos, pawns)
                # clicking twice unhighligh square
                if old_pos == pos: pos = None
                # disable clicking on enemy pawn
                elif pawn != None and pawn.get_color() != player1: pos = None
                # when click before was on pawn and now on empty square
                elif old_pawn != None and pawn == None:
                    # managing move (move legality, capturing), changing player
                    player1 = func.manage_move(old_pos, pos, pawns, player1)
                    # unhighlighing
                    pos = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player1 = not player1
        # drawing board and objects
        draw.draw_main(screen, pos, pawns)
        # computer moving
        if not player1: player1, pawns = func.make_best_move(pawns, player1, max_depth)

# running game
if __name__ == '__main__':
    main(WINDOW)
