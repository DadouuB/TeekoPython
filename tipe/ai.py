import sys
sys.path.append('C:/Users/13dav/OneDrive/Documents/Python_Scripts/tipe')
import numpy as np
import random as rand
import copy
from game import Game
class Ai:


    def __init__(self,ia):
            self.ia = ia
            self.jeu=Game()


    def start(self,pawn,player,board,n):
        (a,b)=n
        if (a,b) ==(0,0) :
            return None
        elif a == 0 or b == 0:
            return self.depthN(pawn,player,board,n,ia)
        else :
            self.jeu.pion_place+=1
            return self.depthNiavsia(pawn,player,board,n,ia)

    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**(1/2)


    def possible_moves(self,p,board):
        move1=[]
        move2=[]
        for x,y in np.argwhere(board==1):
            move1.append((x,y))
        for x,y in np.argwhere(board==-1):
            move2.append((x,y))
        (x,y)=p
        liste=[]
        for i in range(4):
            for j in range(4):
                if self.distance(x,y,i,j)<=(2**(1/2)) and (i,j) not in move1 and (i,j) not in move2 :
                    liste.append((i,j))
        return liste

#Calculate and store every possibilites from a given position 1 move ahead
    def succesors(self,player,board,pions):
        move1=[]
        move2=[]
        for x,y in np.argwhere(board==1):
            move1.append((x,y))
        for x,y in np.argwhere(board==-1):
            move2.append((x,y))
        succesors=[]
        if player ==1:
            if pions<8:
                    for i in range(4):
                        for j in range(4):
                            if board[i][j]==0:
                                pos=copy.deepcopy(board)
                                pos[i][j] = player* (-1)
                                succesors.append(pos)
            else:
                for pawn in move2:
                    coup_possibles = self.possible_moves(pawn,board)
                    for pos2 in coup_possibles:
                        plateau_bis=copy.deepcopy(board)
                        self.test_movements(player* (-1),plateau_bis,pawn,pos2)
                        succesors.append(plateau_bis)
        else :
            if pions<8:
                    for i in range(4):
                        for j in range(4):
                            if board[i][j]==0:
                                pos=copy.deepcopy(board)
                                pos[i][j] = player* (-1)
                                succesors.append(pos)


            else :
                for pawn in move1:
                    coup_possibles = self.possible_moves(pawn,board)
                    for pos2 in coup_possibles:
                        plateau_bis=copy.deepcopy(board)
                        self.test_movements(player* (-1),plateau_bis,pawn,pos2)
                        succesors.append(plateau_bis)

        return succesors


    def test_movements(self,player,board,p1,p2):
        (x1,y1)=p1
        (x2,y2)=p2
        if player ==1:
            board[x1][y1] , board[x2][y2] = 0,1
        else:
             board[x1][y1] , board[x2][y2] = 0,-1






    # Algorithm MinMax
    def neighbor(self,p,player,board):
        (x,y) =p
        nbneigbor = 0
        if player == 1:
            for i in range(2):
                for j in range(2):
                    if board[x-1+i][y-1+j]==1:
                        nbneigbor+=1
        else:
            for i in range(2):
                for j in range(2):
                    if board[x-1+i][y-1+j]==-1:
                        nbneigbor+=-1
        return nbneigbor

    def total_neighbor(self,player,board):
        move1=[]
        move2=[]
        for x,y in np.argwhere(board==1):
            move1.append((x,y))
        for x,y in np.argwhere(board==-1):
            move2.append((x,y))
        nbneigbor=0
        if player == 1:
            for elem in move1:
                nbneigbor+=self.neighbor(elem,player,board)
        else:
            for elem2 in move2:
                nbneigbor+=self.neighbor(elem2,player,board)
        return nbneigbor

    def value(self,p,player):
        (x,y) = p
        if p == (2,2):
            return 12* player
        elif ((x-2)**2+(y-2)**2)**(1/2)<=(2**(1/2)):
            return 10 *player
        elif p in [(0,0), (0,4), (4,0), (4,4)]:
            return 4 * player
        elif p in [(0,1),(0,3),(4,1),(4,3)]:
            return 6 * player
        elif p in [(0,2),(2,0),(4,2),(2,4)]:
            return 5 * player
        return 0

    def total_value(self,player,board):
        tot=0
        move1=[]
        move2=[]
        for x,y in np.argwhere(board==1):
            move1.append((x,y))
        for x,y in np.argwhere(board==-1):
            move2.append((x,y))
        if player==1:
            for elem in move1:
                tot+=self.value(elem,player)
        else:
            for elem2 in move2:
                tot+=self.value(elem2,player)
        return tot

    def h(self,board):
        if self.jeu.victory(board) == 1:
            return np.Inf
        elif  self.jeu.victory(board) == -1:
            return -np.Inf
        else:
            return self.total_value(1,board) + self.total_neighbor(1,board) + self.total_neighbor(-1,board) + self.total_value(-1,board)


# ai

    def easy(self,pawn,player,board):
        move2=[]
        for x,y in np.argwhere(board==-1):
            move2.append((x,y))
        if pawn<8:
            x= rand.randint(0,4)
            y= rand.randint(0,4)
            while board[x][y] !=0:
                x= rand.randint(0,4)
                y= rand.randint(0,4)
            return (x,y)
        else :

            i=rand.randint(0,3)
            x1,y1 = move2[i]
            l=self.possible_moves((x1,y1),board)
            j = rand.randint(0,len(l)-1)
            (x2,y2)= l[j]
            return (x1,y1,x2,y2)



    def max_alphabeta (self,player,board,pions,n,alpha,beta):
            succesors = self.succesors(player,board,pions)
            if n==0 or succesors == [] or self.jeu.victory(board)!= 0:
                return self.h(board)
            maxi = -np.Inf
            for pos in succesors:
                alpha= self.min_alphabeta(player*(-1),pos,pions+1,n-1,alpha,beta)
                if alpha>= maxi:
                    maxi = alpha
                if alpha >= beta:
                    return alpha
            return maxi

    def min_alphabeta (self,player,board,pions,n,alpha,beta):
            succesors = self.succesors(player,board,pions)
            if n==0 or succesors == [] or self.jeu.victory(board)!= 0:
                return self.h(board)
            min = np.Inf
            for pos in succesors:
                beta= self.max_alphabeta(player*(-1),pos,pions+1,n-1,alpha,beta)
                if beta<=min:
                    min = beta
                if alpha >=beta:
                    return beta
            return min


    def depthN(self,pawn,player,board,depth):
        ai = self.ia
        move1=[]
        move2=[]
        for x,y in np.argwhere(board==1):
            move1.append((x,y))
        for x,y in np.argwhere(board==-1):
            move2.append((x,y))
        if player==ai:
            best_val=np.Inf*(-player)
            position=(2,2)
            if pawn<8:
                for i in range(5):
                    for j in range(5):
                        if board[i][j]==0:
                            test=copy.deepcopy(board)
                            test[i][j]= player
                            value = self.max_alphabeta(player,test,pawn,depth,-np.Inf,np.Inf)
                            if value*player > player*best_val:
                                best_val = value
                                position=(i,j)
                return position
            else :
                for elem in move2:
                    for elem2 in self.possible_moves(elem,board):
                        test=copy.deepcopy(board)
                        self.test_movements(player,test,elem,elem2)
                        if self.jeu.victory(test) ==(player):
                            return elem + elem2
                        value = self.max_alphabeta(player,test,pawn,depth,-np.Inf,np.Inf)
                        if player*value > player*best_val:
                            best_val = value
                            position = elem + elem2
                return position
