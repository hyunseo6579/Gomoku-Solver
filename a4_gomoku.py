# make gomoku with pygame
# make it playable by clicks since gomoku uses 9 x 9 board

import pygame


def main():

    pygame.init()
    pygame.display.set_caption("Gomoku_Assignment4_MaristellaJho")
    window = pygame.display.set_mode((700,700))
    playBtn = pygame.image.load("assets/play.png")
    title = Title(window)
    game = Game(window)
    playerMove = Player(window)
    solver = Solver(window)

    # black goes first, and player always starts off
    player = 0

    # create board and store position of top left corner of each point (where stones will be placed)
    # starting point == (17,21); x axis += 77, y axis += 76 pixels
    w,h = 9,9
    board = [[0 for x in range(w)] for y in range(h)]
    moveBoard = [[0 for x in range(w)] for y in range(h)]
    for i in range(9):
        for j in range(9):
            board[i][j] = (17+(77*i),21+(76*j))
    
    run = True
    frame = 0

    while run:
        window.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if frame == 0 and playBtn.get_rect(topleft = (350-(playBtn.get_width()/2),450)).collidepoint(pos):
                    frame = 1
                elif frame == 1:
                    # check player, if user's turn check if occupied, if not, make move
                    if player == 0:
                        if playerMove.checkMove(pos, board, moveBoard):
                            playerMove.makeMove(pos, board, moveBoard)
                            player = 1
                    # if it's not player's turn, solver make move
        if player == 1:
            if solver.checkProgress(moveBoard) == 0:
                solver.makeMove(moveBoard)
                player = 0
            elif solver.checkProgress(moveBoard) == -1:
                print("end game, it's a draw")
            elif solver.checkProgress(moveBoard) == 1:
                print("end game, black won")
            else:
                print("end game, white won")

        if frame == 0:
            title.blit()
        if frame == 1:
            game.blit(board,moveBoard)

        pygame.display.update()


class Title:

    def __init__(self, window):
        self.window = window
        self.pic = pygame.image.load("assets/title.png")
        self.playBtn = pygame.image.load("assets/play.png")

    def blit(self):
        self.window.blit(self.pic,(0,0))
        self.window.blit(self.playBtn, (350 - (self.playBtn.get_width() / 2), 450))


class Game:

    def __init__(self,window):
        self.window = window
        self.board = pygame.image.load("assets/9x9.jpg")
        self.black = pygame.image.load("assets/black.png")
        self.white = pygame.image.load("assets/white.png")

    def blit(self, board, moveBoard):
        self.window.blit(self.board,(0,0))

        for i in range(9):
            for j in range(9):
                if moveBoard[i][j] == 1:
                    self.window.blit(self.black,board[i][j])
                elif moveBoard[i][j] == 2:
                    self.window.blit(self.white,board[i][j])


# decide whether to accept player moves
class Player:

    def __init__(self, window):
        self.window = window

    # check whether the click is for a move that is valid
    def checkMove(self, pos, board, moveBoard):
        for i in range(9):
            for j in range(9):
                rect = pygame.Rect(board[i][j],(50,50))
                if rect.collidepoint(pos):
                    if moveBoard[i][j] == 0:
                        return True
        return False

    # return position to place the stone on
    def makeMove(self, pos, board, moveBoard):
        for i in range(9):
            for j in range(9):
                rect = pygame.Rect(board[i][j], (50, 50))
                if rect.collidepoint(pos):
                    # 1 means player move, 2 means solver move
                    moveBoard[i][j] = 1


class Solver:

    def __init__(self, window):
        self.window = window

    # note, the "board" passed in the following methods are all "moveBoards" in main which contains information about
    # stones that are placed in each position.
    def checkProgress(self, board):
        # check for horizontal 5
        for i in range(2,7):
            for j in range(9):
                if board[i][j] == 1 and board[i-1][j] == 1 and board[i+1][j] == 1 and board[i-2][j] == 1 and board[i+2][j] == 1:
                    # if horizontal 5 of 1s found, 1 won
                    return 1
                elif board[i][j] == 2 and board[i-1][j] == 2 and board[i+1][j] == 2 and board[i-2][j] == 2 and board[i+2][j] == 2:
                    # elif row of 5 of 2s found, 2 won
                    return 2

        # check for vertical 5
        for i in range(9):
            for j in range(2,7):
                if board[i][j] == 1 and board[i][j-1] == 1 and board[i][j+1] == 1 and board[i][j-2] == 1 and \
                        board[i][j+2] == 1:
                    # if vertical 5 of 1s found, 1 won
                    return 1
                elif board[i][j] == 2 and board[i][j-1] == 2 and board[i][j+1] == 2 and board[i][j-2] == 2 and \
                        board[i][j+2] == 2:
                    # elif column of 5 of 2s found, 2 won
                    return 2

        # check for both diagonal 5s
        for i in range(2,7):
            for j in range(2,7):
                # first check both diagonals of 1
                if board[i][j] == 1 and board[i-1][j-1] == 1 and board[i+1][j+1] == 1 and board[i-2][j-2] == 1 and board[i+2][j+2] == 1:
                    return 1
                elif board[i][j] == 1 and board[i-1][j+1] == 1 and board[i+1][j-1] == 1 and board[i-2][j+2] == 1 and board[i+2][j-2] == 1:
                    return 1

                # now check both diagonals of 2
                elif board[i][j] == 2 and board[i-1][j-1] == 2 and board[i+1][j+1] == 2 and board[i-2][j-2] == 2 and board[i+2][j+2] == 2:
                    return 2
                elif board[i][j] == 2 and board[i - 1][j + 1] == 2 and board[i + 1][j - 1] == 2 and board[i - 2][
                    j + 2] == 2 and board[i + 2][j - 2] == 2:
                    return 2

        # check if board is full
        count = 0
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    count += 1
        if count == 81:
            return -1

        # if neither has won yet, and board is not full, continue
        return 0

    def makeMove(self, board):
        if self.defend(board):
            return
        else:
            self.move(board)
            return

## not yet tested
    def defend(self, board):
        # find any rows of 3 or more (that can become 5) and defend
        # if row of 4 is found with no defend on one end, return False (since no defense move will work anyway)

        # check for horizontal 3
        for i in range(2,7):
            for j in range(9):
                if board[i][j] == 1 and board[i-1][j] == 1 and board[i+1][j] == 1:
                    if board[i-2][j] == 0:
                        board[i-2][j] = 2
                        return True
                    elif board[i+2][j] == 0:
                        board[i+2][j] = 2
                        return True

        # check for vertical 3
        for i in range(9):
            for j in range(2,7):
                if board[i][j] == 1 and board[i][j-1] == 1 and board[i][j+1] == 1:
                    if board[i][j-2] == 0:
                        board[i][j-2] = 2
                        return True
                    elif board[i][j+2] == 0:
                        board[i][j+2] = 2
                        return True

        # check for both diagonal 3s
        for i in range(2,7):
            for j in range(2,7):
                # check both diagonals of 1
                if board[i][j] == 1 and board[i-1][j-1] == 1 and board[i+1][j+1] == 1:
                    if board[i-2][j-2] == 0:
                        board[i-2][j-2] = 2
                        return True
                    elif board[i+2][j+2] == 0:
                        board[i + 2][j + 2] = 2
                        return True
                elif board[i][j] == 1 and board[i-1][j+1] == 1 and board[i+1][j-1] == 1:
                    if board[i - 2][j + 2] == 0:
                        board[i - 2][j + 2] = 2
                        return True
                    elif board[i + 2][j - 2] == 0:
                        board[i + 2][j - 2] = 2
                        return True

        # if no defense move was made, return False
        return False

    def move(self, board):
        # find any of solver's stone that can be turned into a connected 5
        # if not, find any spot that has empty 5
        # if not (in this case it would be lose or draw), place anywhere
        pass


main()
