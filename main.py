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
    click_pos = None
    # creating clock
    clock = pygame.time.Clock()
    # creating board
    board = func.start_board()
    # main loop
    while True:
        clock.tick(const.FPS)
        for event in pygame.event.get():
            # closing game
            if event.type == pygame.QUIT:
                pygame.quit()
            # mouse click detection
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                click_pos = func.get_rowcol(mouse_pos)
        # drawing board and objects
        draw.draw_main(screen, board, click_pos)

# running game
if __name__ == '__main__':
    main(WINDOW)
