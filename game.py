
import numpy as np

class Game():
    def  __init__ (self):
        self.board=np.zeros((5,5))
        self.joueur = 17
        self.pion_place=0

    def player_displaying(self):
        return "Player 1" if self.joueur == 1 else "Player 2"

    def victory(self,board):
        #row
        for i in range(5):
            if np.sum(board[i]==1)==4:
                if np.all(board[i][0:4]==1) or np.all(board[i][1:5]==1):
                    return 1
            elif np.sum(board[i]==-1)==4:
                if np.all(board[i][0:4]==(-1)) or np.all(board[i][1:5]==(-1)):
                    return -1
        #column
        for i in range(5):
            colonne=board[:,i]
            if np.sum(colonne ==1)==4:
                if np.all(colonne[0:4]==1) or np.all(colonne[1:5]==1):
                    return  1
            elif np.sum(colonne ==-1)==4:
                if np.all(colonne[0:4]==(-1)) or np.all(colonne[1:5]==(-1)):
                    return -1
        #square
        for i in range(4):
            for j in range(4):
                c = [board[i][j:j+2],board[i+1][j:j+2]]
                cube = np.array(c)
                if np.sum(cube)==4:
                    return  1
                elif np.sum(cube) == -4 :
                    return -1

        #diagonale
        for i in range(-1,2):
            diag = board.diagonal(i)
            oppdiag = np.fliplr(board).diagonal(i)
            if np.sum(diag == 1) == 4 or np.sum(oppdiag == 1) == 4:
                if np.all(diag[0:4] == 1) or np.all(oppdiag[0:4] == 1):
                    return  1
                if len(diag)>4:
                    if np.all(diag[1:5] == 1) or np.all(oppdiag[1:5] == 1):
                       return  1
            elif np.sum(diag == -1) == 4 or np.sum(oppdiag == -1) == 4:
                if np.all(diag[0:4] == -1) or np.all(oppdiag[0:4] == -1):
                    return  -1
                if len(diag)>4:
                    if np.all(diag[1:5] == -1) or np.all(oppdiag[1:5] == -1):
                        return  -1

        return 0




