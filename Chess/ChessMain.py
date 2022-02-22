import pygame as p
import ChessEngine

WIDTH = HEGHT = 512
DIMENSION = 8
SQ_SIZE = HEGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImage():
    pieces = ['wp','wR','wB','wN','wQ','wK','bp','bR','bB','bN','bQ','bK']
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImage()
    running = True
    sqSelected = ()
    playerClicks = []
    Click = []
    MoveMade = False
    while (running):
        if len(playerClicks) == 0 and gs.EndGame == False:
            gs.CreateAllMoves()
            gs.CreateAllValidMoves()
            if gs.Moved:
                gs.CheckEndGame()
        for e in p.event.get():
            if gs.EndGame and gs.End:
                if gs.WhiteWin:
                    print("White Win!")
                elif gs.BlackWin:
                    print("BlackWin!")
                elif gs.StealMate:
                    print("Draw!")
                gs.End = False
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                #print (str(row) + str(col))
                if gs.EndGame == False:
                    if sqSelected == (row,col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                if len(playerClicks) == 1 and gs.board[playerClicks[0][0]][playerClicks[0][1]] == "--":
                    sqSelected = ()
                    playerClicks = []
                #print(len(playerClicks))
                if len(playerClicks) == 2 and gs.board[playerClicks[0][0]][playerClicks[0][1]][0] == gs.board[playerClicks[1][0]][playerClicks[1][1]][0]:
                    sqSelected = (row,col)
                    playerClicks = [sqSelected]

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    WhiteToMove = gs.WhiteToMove
                    ColorSelected = gs.board[move.startRow][move.startCol][0]
                    ColorEaten = gs.board[move.endRow][move.endCol][0]
                    Piece = gs.board[move.startRow][move.startCol][1]
                    #print(ColorSelected)
                    #print(WhiteToMove)
                    if (ColorSelected == "w" and WhiteToMove == True) or (ColorSelected == "b" and WhiteToMove != True):
                        gs.CheckIfPossibleToMove(move.startRow,move.startCol,move.endRow,move.endCol)
                        if (gs.Possible):
                            gs.makeMove(move)
                            gs.MoveMade = True
                            Click = playerClicks
                            gs.CheckPromotion(Piece,move.endRow)
                    sqSelected = ()
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                endRow = move.endRow
                endCol = move.endCol
                if e.key == p.K_z:
                    gs.undoMoves()
                elif e.key == p.K_q:
                    running = False




            #DrawPromotionPiece(screen)
        drawGameState(screen,gs,playerClicks,MoveMade,Click)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs,playerClicks,moveMade,click):
    drawBoard(screen)
    if (len(playerClicks) != 0):
        if (gs.WhiteToMove and gs.board[playerClicks[0][0]][playerClicks[0][1]][0] == "w") or ((not gs.WhiteToMove) and gs.board[playerClicks[0][0]][playerClicks[0][1]][0] == "b"):
            drawHighlightStart(screen,playerClicks[0][0],playerClicks[0][1])
    if gs.MoveMade:
        drawHighlightEnd(screen,click[1][0],click[1][1])
        drawHighlightStart(screen,click[0][0],click[0][1])
    if (len(playerClicks) == 2):
        gs.MoveMade = False
    drawPieces(screen,gs.board)



def drawBoard(screen):
    colors = [p.Color(243, 255, 255),p.Color(255, 204, 255)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def drawHighlightStart(screen,row,col):
    color = p.Color(173, 255, 196)
    p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawHighlightEnd(screen,row,col):
    color = p.Color(173, 255, 196)
    p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
def DrawPromotionPiece(screen):
    pass

if __name__ == "__main__":
    main()