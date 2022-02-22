from copy import deepcopy
class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.WhiteToMove = True
        self.movelog = []
        self.moves = 1
        self.Possible = False
        self.Valid = False
        self.EnpassantW = []
        self.EnpassantB = []
        self.ValidEnpassW = []
        self.ValidEnpassB = []
        self.EnpassW = False
        self.EnpassB = False
        self.EnpassMove = []
        self.EnpassMade = []
        self.EnMade = False
        self.AllWhiteMoves = {}
        self.AllBlackMoves = {}
        self.AllWhiteValidMoves = {}
        self.AllBlackValidMoves = {}
        self.MoveMade = False
        self.ValidEn = []
        self.temp_check = False
        self.Checked = False
        self.CheckMate = False
        self.StealMate = False
        self.EndGame = False
        self.End = False
        self.WhiteWin = False
        self.BlackWin = False
        self.Moved = False


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.Moved = True
        self.WhiteToMove = not self.WhiteToMove
        self.Possible = False
        self.Valid = False
        self.EnpassantW = []
        self.EnpassantB = []
        self.AllWhiteValidMoves = {}
        self.AllBlackValidMoves = {}
        self.ValidEnpassW = []
        self.Moved = True
        self.ValidEnpassB = []
        self.moves += 1

    def undoMoves(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove
            self.Possible = False
            self.Valid = False
            self.MoveMade = False
            self.EnpassantW = []
            self.EnpassantB = []
            self.EnpassW = False
            self.EnpassB = False
            self.EnpassMove = []
            self.CheckMate = False
            self.StealMate = False
            self.EndGame = False
            self.End = False
            self.ValidEnpassW = []
            self.ValidEnpassB = []
            self.Moved = False
            self.WhiteWin = False
            self.BlackWin = False
            self.CreateAllMoves()
            self.CreateAllValidMoves()

            if (self.moves > 1):
                self.moves -= 1
        if self.EnMade:
            rowEn = self.EnpassMade[len(self.EnpassMade)-1][0]
            colEn = self.EnpassMade[len(self.EnpassMade)-1][1]
            if self.WhiteToMove:
                self.board[rowEn][colEn] = "bp"
            else:
                self.board[rowEn][colEn] = "wp"
            self.EnMade = False

    def CreateAllMoves(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != "--":
                    color = self.board[i][j][0]
                    if self.board[i][j][1] == "p":
                        self.GetPawnMoves(color,i,j)
                    elif self.board[i][j][1] == "N":
                        self.GetKnightMoves(color,i,j)
                    elif self.board[i][j][1] == "R":
                        self.GetRookMoves(color,i,j)
                    elif self.board[i][j][1] == "B":
                        self.GetBishopMoves(color,i,j)
                    elif self.board[i][j][1] == "Q":
                        self.GetQueenMoves(color,i,j)
                    elif self.board[i][j][1] == "K":
                        self.GetKingMoves(color,i,j)

    def CreateAllValidMoves(self):
        if self.WhiteToMove:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j][0] == "w" and self.board[i][j][1] != "K":
                        Moves = []
                        Start = str(i) + str(j)
                        color = "w"
                        for item in self.AllWhiteMoves[Start]:
                            temp_board = deepcopy(self.board)
                            temp_board[i][j] = "--"
                            temp_board[item[0]][item[1]] = self.board[i][j]
                            self.CheckCheck(color,temp_board)
                            if self.temp_check == False:
                                temp = item
                                Moves.append(temp)
                        self.AllWhiteValidMoves[Start] = Moves
        else:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j][0] == "b" and self.board[i][j][1] != "K":
                        Moves = []
                        Start = str(i) + str(j)
                        color = "b"
                        for item in self.AllBlackMoves[Start]:
                            temp_board = deepcopy(self.board)
                            temp_board[i][j] = "--"
                            temp_board[item[0]][item[1]] = self.board[i][j]
                            self.CheckCheck(color,temp_board)
                            if self.temp_check == False:
                                temp = item
                                Moves.append(temp)
                        self.AllBlackValidMoves[Start] = Moves
        if len(self.EnpassMove) != 0:
            for item in self.EnpassMove:
                temp_board = deepcopy(self.board)
                temp_board[item[0]][item[1]] = "--"
                temp_board[item[2]][item[3]] = self.board[item[0]][item[1]]
                temp_board[self.EnpassMade[len(self.EnpassMade)-1][0]][self.EnpassMade[len(self.EnpassMade)-1][1]] = "--"
                if self.WhiteToMove:
                    color = "w"
                    self.CheckCheck(color,temp_board)
                else:
                    color = "b"
                    self.CheckCheck(color,temp_board)
                if self.temp_check == False:
                    self.ValidEn.append(item)

        if self.WhiteToMove:
            color = "w"
            for i in range(8):
                if self.board[6][i] == "wp":
                    if len(self.EnpassantW) != 0:
                        for item in self.EnpassantW:
                            if [6,i] == [item[0],item[1]]:
                                temp_board = deepcopy(self.board)
                                temp_board[6][i] = "--"
                                temp_board[4][i] = "wp"
                                self.CheckCheck(color,temp_board)
                                if self.temp_check == False:
                                    self.ValidEnpassW.append(item)
        else:
            color = "b"
            for i in range(8):
                if self.board[1][i] == "bp":
                    if len(self.EnpassantB) != 0:
                        for item in self.EnpassantB:
                            if [1, i] == [item[0], item[1]]:
                                temp_board = deepcopy(self.board)
                                temp_board[1][i] = "--"
                                temp_board[3][i] = "wp"
                                self.CheckCheck(color, temp_board)
                                if self.temp_check == False:
                                    self.ValidEnpassB.append(item)

    #Tốt
    def GetPawnMoves(self,color,row,col):
        PawnMoves = []
        Start = str(row) + str(col)
        #Enpass Data
        if len(self.EnpassMade) != 0:
            rowEn = self.EnpassMade[len(self.EnpassMade)-1][0]
            colEn = self.EnpassMade[len(self.EnpassMade)-1][1]
            moveEn = self.EnpassMade[len(self.EnpassMade)-1][2]
        #Tốt trắng
        if color == "w" and self.WhiteToMove == True:
            #Trắng đi lên 1 ô
            if row > 0:
                if self.board[row-1][col] == "--":
                    temp=[row-1,col]
                    PawnMoves.append(temp)
            #Trắng đi lên 2 ô
            if row == 6:
                if self.board[row-1][col] == "--" and self.board[row-2][col] == "--":
                    temp=[row,col,row-2,col]
                    self.EnpassantW.append(temp)
            #Trắng đi qua trái + Enpassant
            if col > 0:
                if self.board[row-1][col-1][0] == "b":
                    temp = [row-1,col-1]
                    PawnMoves.append(temp)
                if self.EnpassB:
                    if len(self.EnpassMade) != 0:
                        if self.board[row-1][col-1] == "--":
                            if [row,col-1] == [rowEn,colEn]:
                                if moveEn == self.moves - 1:
                                    temp = [row,col,row - 1, col - 1]
                                    self.EnpassMove.append(temp)
            #Trắng đi qua phải + Enpassant
            if col < 7:
                if self.board[row-1][col+1][0] == "b":
                    temp = [row-1,col+1]
                    PawnMoves.append(temp)
                if self.EnpassB:
                    if len(self.EnpassMade) != 0:
                        if self.board[row-1][col+1] == "--" and [row,col+1] == [rowEn,colEn] and moveEn == self.moves-1:
                            temp = [row,col,row - 1, col + 1]
                            self.EnpassMove.append(temp)
        #Tốt đen
        elif color == "b" and not self.WhiteToMove:
            #Đen đi xuống 1 ô
            if row < 7:
                if self.board[row+1][col] == "--":
                    temp = [row+1,col]
                    PawnMoves.append(temp)
            #Đen đi xuống 2 ô
            if row == 1:
                if self.board[row+1][col] == "--" and self.board[row+2][col] == "--":
                    temp=[row,col,row+2,col]
                    self.EnpassantB.append(temp)
            #Đen đi qua trái + Enpassant
            if col > 0:
                if self.board[row+1][col-1][0] == "w":
                    temp = [row+1,col-1]
                    PawnMoves.append(temp)
                if self.EnpassW:
                    if len(self.EnpassMade) != 0:
                        if self.board[row+1][col-1] == "--" and [row,col-1] == [rowEn,colEn] and moveEn == self.moves-1:
                            temp = [row,col,row+1,col-1]
                            self.EnpassMove.append(temp)
            #Đen đi qua phải + Enpassant
            if col < 7:
                if self.board[row+1][col+1][0] == "w":
                    temp = [row+1,col+1]
                    PawnMoves.append(temp)
                if self.EnpassW:
                    if len(self.EnpassMade) != 0:
                        if self.board[row+1][col+1] == "--" and [row,col+1] == [rowEn,colEn] and moveEn == self.moves-1:
                            temp = [row,col,row+1,col+1]
                            self.EnpassMove.append(temp)
        if color == "w":
            self.AllWhiteMoves[Start] = PawnMoves
        else:
            self.AllBlackMoves[Start] = PawnMoves

    #Ngựa
    def GetKnightMoves(self,color,row,col):
        Value = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]
        Start = str(row) + str(col)
        KnightMoves = []
        for item in Value:
            if (row+item[0] <= 7) and (row+item[0] >= 0) and (col+item[1] <= 7) and (col+item[1] >=0):
                Moves = [row+item[0],col+item[1]]
                KnightMoves.append(Moves)
        if color == "w":
            self.AllWhiteMoves[Start] = KnightMoves
        else:
            self.AllBlackMoves[Start] = KnightMoves

    #Xe
    def GetRookMoves(self,color,row,col):
        Start=str(row)+str(col)
        RookMoves = []

        #Đi lên
        if (row > 0):
            i = 1
            while(row-i >= 0):
                if self.board[row-i][col] == "--":
                    Moves = [row-i,col]
                    RookMoves.append(Moves)
                elif self.board[row-i][col][0] == color:
                    break
                elif self.board[row-i][col][0] != color:
                    Moves = [row-i,col]
                    RookMoves.append(Moves)
                    break
                i += 1
        #Đi xuống
        if (row < 7):
            for i in range (row+1,8):
                if self.board[i][col] == "--":
                    Moves = [i,col]
                    RookMoves.append(Moves)
                elif self.board[i][col][0] != color:
                    Moves = [i, col]
                    RookMoves.append(Moves)
                    break
                elif self.board[i][col][0] == color:
                    break
        #Qua trái
        if (col > 0):
            i = 1
            while (col-i >= 0):
                if self.board[row][col-i] == "--":
                    Moves = [row,col-i]
                    RookMoves.append(Moves)
                elif self.board[row][col-i][0] != color:
                    Moves = [row, col - i]
                    RookMoves.append(Moves)
                    break
                elif self.board[row][col-i][0] == color:
                    break
                i += 1
        #Qua phải
        if (col < 7):
            for i in range(col+1,8):
                if self.board[row][i] == "--":
                    Moves = [row,i]
                    RookMoves.append(Moves)
                elif self.board[row][i][0] != color:
                    Moves = [row,i]
                    RookMoves.append(Moves)
                    break
                elif self.board[row][i][0] == color:
                    break
        if color == "w":
            self.AllWhiteMoves[Start] = RookMoves
        else:
            self.AllBlackMoves[Start] = RookMoves

    #Tượng
    def GetBishopMoves(self,color,row,col):
        Start = str(row) + str(col)
        BishopMoves = []
        #Đi chéo lên bên trái
        if row > 0 and col > 0:
            i = 1
            while(True):
                if self.board[row-i][col-i] == "--":
                    temp = [row-i,col-i]
                    BishopMoves.append(temp)
                elif self.board[row-i][col-i][0] != color:
                    temp = [row - i, col - i]
                    BishopMoves.append(temp)
                    break
                elif self.board[row-i][col-i][0] == color:
                    break
                if (row-i == 0) or (col-i == 0):
                    break
                i += 1
        #Đi chéo lên bên phải
        if (row > 0) and (col < 7):
            i = 1
            while(True):
                if self.board[row-i][col+i] == "--":
                    temp = [row-i,col+i]
                    BishopMoves.append(temp)
                elif self.board[row-i][col+i][0] != color:
                    temp = [row - i,col + i]
                    BishopMoves.append(temp)
                    break
                elif self.board[row - i][col + i][0] == color:
                    break
                if (row-i == 0) or (col + i == 7):
                    break
                i += 1
        #Đi chéo xuống bên trái
        if (row < 7) and (col > 0):
            i = 1
            while(True):
                if self.board[row+i][col-i] == "--":
                    temp = [row+i,col-i]
                    BishopMoves.append(temp)
                elif self.board[row+i][col-i][0] != color:
                    temp = [row + i, col - i]
                    BishopMoves.append(temp)
                    break
                elif self.board[row+i][col-i][0] == color:
                    break
                if (row+i == 7) or (col-i == 0):
                    break
                i += 1
        #Đi chéo xuống bên phải
        if (row < 7) and (col < 7):
            i = 1
            while(True):
                if self.board[row+i][col+i] == "--":
                    temp = [row+i,col+i]
                    BishopMoves.append(temp)
                elif self.board[row+i][col+i] != color:
                    temp = [row + i, col + i]
                    BishopMoves.append(temp)
                    break
                elif self.board[row+i][col+i] == color:
                    break
                if (row+i == 7) or (col+i == 7):
                    break
                i += 1

        if color == "w":
            self.AllWhiteMoves[Start] = BishopMoves
        else:
            self.AllBlackMoves[Start] = BishopMoves

    #Hậu
    def GetQueenMoves(self,color,row,col):
        Start = str(row) + str(col)
        QueenMoves = []
        # Đi lên
        if (row > 0):
            i = 1
            while (row - i >= 0):
                if self.board[row - i][col] == "--":
                    Moves = [row - i, col]
                    QueenMoves.append(Moves)
                elif self.board[row - i][col][0] == color:
                    break
                elif self.board[row - i][col][0] != color:
                    Moves = [row - i, col]
                    QueenMoves.append(Moves)
                    break
                i += 1
        # Đi xuống
        if (row < 7):
            for i in range(row + 1, 8):
                if self.board[i][col] == "--":
                    Moves = [i, col]
                    QueenMoves.append(Moves)
                elif self.board[i][col][0] != color:
                    Moves = [i, col]
                    QueenMoves.append(Moves)
                    break
                elif self.board[i][col][0] == color:
                    break
        # Qua trái
        if (col > 0):
            i = 1
            while (col - i >= 0):
                if self.board[row][col - i] == "--":
                    Moves = [row, col - i]
                    QueenMoves.append(Moves)
                elif self.board[row][col - i][0] != color:
                    Moves = [row, col - i]
                    QueenMoves.append(Moves)
                    break
                elif self.board[row][col - i][0] == color:
                    break
                i += 1
        # Qua phải
        if (col < 7):
            for i in range(col + 1, 8):
                if self.board[row][i] == "--":
                    Moves = [row, i]
                    QueenMoves.append(Moves)
                elif self.board[row][i][0] != color:
                    Moves = [row, i]
                    QueenMoves.append(Moves)
                    break
                elif self.board[row][i][0] == color:
                    break
        # Đi chéo lên bên trái
        if row > 0 and col > 0:
            i = 1
            while (True):
                if self.board[row - i][col - i] == "--":
                    temp = [row - i, col - i]
                    QueenMoves.append(temp)
                elif self.board[row - i][col - i][0] != color:
                    temp = [row - i, col - i]
                    QueenMoves.append(temp)
                    break
                elif self.board[row - i][col - i][0] == color:
                    break
                if (row - i == 0) or (col - i == 0):
                    break
                i += 1
        # Đi chéo lên bên phải
        if (row > 0) and (col < 7):
            i = 1
            while (True):
                if self.board[row - i][col + i] == "--":
                    temp = [row - i, col + i]
                    QueenMoves.append(temp)
                elif self.board[row - i][col + i][0] != color:
                    temp = [row - i, col + i]
                    QueenMoves.append(temp)
                    break
                elif self.board[row - i][col + i][0] == color:
                    break
                if (row - i == 0) or (col + i == 7):
                    break
                i += 1
        # Đi chéo xuống bên trái
        if (row < 7) and (col > 0):
            i = 1
            while (True):
                if self.board[row + i][col - i] == "--":
                    temp = [row + i, col - i]
                    QueenMoves.append(temp)
                elif self.board[row + i][col - i][0] != color:
                    temp = [row + i, col - i]
                    QueenMoves.append(temp)
                    break
                elif self.board[row + i][col - i][0] == color:
                    break
                if (row + i == 7) or (col - i == 0):
                    break
                i += 1
        # Đi chéo xuống bên phải
        if (row < 7) and (col < 7):
            i = 1
            while (True):
                if self.board[row + i][col + i] == "--":
                    temp = [row + i, col + i]
                    QueenMoves.append(temp)
                elif self.board[row + i][col + i] != color:
                    temp = [row + i, col + i]
                    QueenMoves.append(temp)
                    break
                elif self.board[row + i][col + i] == color:
                    break
                if (row + i == 7) or (col + i == 7):
                    break
                i += 1

        if color == "w":
            self.AllWhiteMoves[Start] = QueenMoves
        else:
            self.AllBlackMoves[Start] = QueenMoves

    #Vua
    def GetKingMoves(self,cplor,row,col):
        pass

    def CheckIfPossibleToMove(self,startRow,startCol,endRow,endCol):
        Start=str(startRow)+str(startCol)
        #Normal Moves
        if self.WhiteToMove:
            for item in self.AllWhiteValidMoves[Start]:
                if [endRow,endCol] == item:
                    self.Possible = True
                    break
        else:
            for item in self.AllBlackValidMoves[Start]:
                if [endRow,endCol] == item:
                    self.Possible = True
                    break
        #White Enpassant
        if self.Possible == False and self.WhiteToMove:
            if len(self.ValidEnpassW) != 0:
                for item in self.ValidEnpassW:
                    if [startRow,startCol,endRow,endCol] == item:
                        temp = [endRow,endCol,self.moves]
                        self.EnpassMade.append(temp)
                        self.Possible = True
                        self.EnpassW = True
                        break
        #Balck Enpassant
        elif self.Possible == False and self.WhiteToMove == False:
            if len(self.ValidEnpassB) != 0:
                for item in self.ValidEnpassB:
                    if [startRow, startCol, endRow, endCol] == item:
                        temp = [endRow, endCol,self.moves]
                        self.EnpassMade.append(temp)
                        self.Possible = True
                        self.EnpassB = True
                        break
        #Enpass
        if self.Possible == False:
            if len(self.ValidEn) != 0:
                for item in self.EnpassMove:
                    if [startRow,startCol,endRow,endCol] == item:
                        self.EnMade = True
                        self.Possible = True
                        self.Enpass()
                        break
            self.EnpassMove = []
        #Castling


    def Enpass(self):
        self.board[self.EnpassMade[len(self.EnpassMade)-1][0]][self.EnpassMade[len(self.EnpassMade)-1][1]] = "--"

    def CheckCheck(self,color,board):
        self.temp_check = False
        king = str(color) + "K"
        pos = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == king:
                    temp = [i,j]
                    pos.append(temp)
                    break

        if self.WhiteToMove:
            for item in self.AllBlackMoves:
                for things in self.AllBlackMoves[item]:
                    if pos[0] == things:
                        self.temp_check = True
        else:
            for item in self.AllWhiteMoves:
                for things in self.AllWhiteMoves[item]:
                    if pos[0] == things:
                        self.temp_check = True

    def CheckEndGame(self):
        Lose = True
        Draw = True
        if self.WhiteToMove:
            color = "w"
        else:
            color = "b"
        self.CheckCheck(color,self.board)
        if self.WhiteToMove:
            if self.temp_check:
                if len(self.ValidEnpassW) == 0:
                    if len(self.ValidEn) == 0:
                        for item in self.AllWhiteValidMoves:
                            if len(self.AllWhiteValidMoves[item]) != 0:
                                Lose = False
                                break
                        if Lose:
                            self.BlackWin = True
            elif len(self.ValidEnpassW) == 0:
                if len(self.ValidEn) == 0:
                    for item in self.AllWhiteValidMoves:
                        if len(self.AllWhiteValidMoves[item]) != 0:
                            Draw = False
                            break
                    if Draw:
                        self.StealMate = True
        else:
            if self.temp_check:
                if len(self.ValidEnpassB) == 0:
                    if len(self.ValidEn) == 0:
                        for item in self.AllBlackValidMoves:
                            if len(self.AllBlackValidMoves[item]) != 0:
                                Lose = False
                                break
                        if Lose:
                            self.WhiteWin = True
            elif len(self.ValidEnpassB) == 0:
                if len(self.ValidEn) == 0:
                    for item in self.AllBlackValidMoves:
                        if len(self.AllBlackValidMoves[item]) != 0:
                            Draw = False
                            break
                    if Draw:
                        self.StealMate = True
        if self.WhiteWin or self.BlackWin or self.StealMate:
            self.EndGame = True

        if self.EndGame:
            self.End = True
        else:
            self.End = False



    def CheckPromotion(self,piece,row):
        #Promotion for White:
        if self.WhiteToMove == False:
            if (piece == "p") and (row == 0):
                self.Promote = True
        #Promotion for Black
        else:
            if piece == "p" and row == 7:
                self.Promote = True


    def PromotePawn(self, PieceChoosed, color, row, col):
        print(color)
        print(PieceChoosed)
        To = color + PieceChoosed
        self.board[row][col] = To
        self.Promote = False



class Move():

    rankToRow = {"1":7,"2":6,"3":5,"4":4,
                 "5":3,"6":2,"7":1,"8":0}

    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]


