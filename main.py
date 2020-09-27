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
    click_pos = None
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
                old_click_pos = click_pos
                # getting old clicked pawn
                old_click_pawn = func.find_pawn(old_click_pos)
                # getting new clicked position
                click_pos = func.get_rowcol(pygame.mouse.get_pos())
                # getting new clicked pawn
                click_pawn = func.find_pawn(click_pos)
                # clicking twice unhighligh square
                if old_click_pos == click_pos: click_pos = None
                # disable clicking on enemy pawn
                if click_pawn != None and click_pawn.get_color() != var.player1: click_pos = None
                # when click before was on pawn and now on empty square
                if old_click_pawn != None and click_pawn == None:
                    # managing move (move legality, capturing)
                    if func.manage_move(old_click_pos, click_pos):
                        # moving pawn
                        old_click_pawn.move(click_pos)
                        # unhighlighing
                        click_pos = None
                        # changing player
                        var.player1 = not var.player1


        # drawing board and objects
        draw.draw_main(screen, click_pos)

# running game
if __name__ == '__main__':
    main(WINDOW)
