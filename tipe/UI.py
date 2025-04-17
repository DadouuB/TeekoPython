import sys
sys.path.append('C:/Users/13dav/OneDrive/Documents/Python_Scripts/tipe')
import tkinter as tk
from tkinter import Button, messagebox
from ai import Ai
from game import Game

class GameUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Choix du mode de jeu")

        self.mode = None
        self.setup_menu()



    def setup_menu(self):
        tk.Label(self.master, text="Choisissez un mode de jeu", font=("Arial", 16)).pack(pady=20)
        Button(self.master, text="Joueur vs Joueur", width=20, command=lambda: self.start_game("pvp")).pack(pady=10)
        Button(self.master, text="Joueur vs IA", width=20, command=lambda: self.start_game("pve")).pack(pady=10)
        tk.Label(self.master, text="").pack(pady=5)
        tk.Label(self.master, text="Profondeur IA 1 :", font=("Arial", 12)).pack(pady=2)
        self.depth_entry_1 = tk.Entry(self.master)
        self.depth_entry_1.insert(0, "2")
        self.depth_entry_1.pack(pady=2)


    def start_game(self, mode):

        self.mode = mode
        self.window = tk.Toplevel(self.master)
        self.window.title("Jeu du plateau")
        self.window.geometry("600x600")
        self.game = Game()
        try:
                self.depth_ia = int(self.depth_entry_1.get())
        except:
                self.depth_ia = 2
        self.ai_2 = Ai(-1)
        self.current_player = 1
        self.pions_place = 0
        self.selected_pawn = None
        self.cells = []

        self.display_board()


    def display_board(self):
        for i in range(5):
            row = []
            for j in range(5):
                btn = Button(self.window, text=" ", width=10, height=5, bg='white',
                             command=lambda i=i, j=j: self.cell_click(i, j))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.cells.append(row)

        self.message = Button(self.window, text="Au tour du joueur 1", bg='white', fg='black')
        self.message.grid(row=5, column=0, columnspan=5)

    def cell_click(self, i, j):

        board = self.game.board

        if self.pions_place < 8:
            if board[i][j] == 0:
                self.play_move(i, j)
                self.pions_place += 1
                if self.check_victory():
                    return
                if self.mode == "pve" and self.current_player == -1:
                    self.window.after(300, self.ai_move)
        else:
            if self.mode == "pve" and self.current_player == -1:
                return

            if self.selected_pawn is None:
                if board[i][j] == self.current_player:
                    self.selected_pawn = (i, j)
                    self.cells[i][j].config(bg='yellow')
            else:
                if board[i][j] == 0 and self.is_adjacent(self.selected_pawn, (i, j)):
                    self.move_pawn(self.selected_pawn, (i, j))
                    if self.check_victory():
                        return
                    self.selected_pawn = None
                    if self.mode == "pve" and self.current_player == -1:
                        self.window.after(300, self.ai_move)
                else:
                    self.cells[self.selected_pawn[0]][self.selected_pawn[1]].config(bg='white')
                    self.selected_pawn = None

    def move_pawn(self, start, end):
        x1, y1 = start
        x2, y2 = end
        board = self.game.board

        symbol = "X" if self.current_player == 1 else "O"
        color = "blue" if self.current_player == 1 else "red"

        board[x1][y1] = 0
        board[x2][y2] = self.current_player

        self.cells[x1][y1].config(text=" ", bg='white')
        self.cells[x2][y2].config(text=symbol, bg=color)

        self.current_player *= -1
        self.message.config(text=f"Au tour du joueur {'1' if self.current_player == 1 else '2'}")

    def play_move(self, i, j):
        board = self.game.board
        board[i][j] = self.current_player
        symbol = "X" if self.current_player == 1 else "O"
        color = "blue" if self.current_player == 1 else "red"
        self.cells[i][j].config(text=symbol, bg=color)

        self.current_player *= -1
        self.message.config(text=f"Au tour du joueur {'1' if self.current_player == 1 else '2'}")

    def ai_move(self):
        board = self.game.board
        move = self.ai_2.depthN(self.pions_place, -1, board, self.depth_ia)
        if self.pions_place<8:
            if move:
                i, j = move
                self.play_move(i, j)
                self.pions_place += 1
                self.check_victory()
        else:
            if move:
                x1, y1, x2, y2 = move
                self.move_pawn((x1, y1), (x2, y2))
                self.check_victory()


    def is_adjacent(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

    def check_victory(self):
        winner = self.game.victory(self.game.board)
        if winner != 0:
            text = "Joueur 1" if winner == 1 else "Joueur 2"
            if self.mode == "pve" and winner == -1:
                text = "IA"
            elif self.mode == "ivi":
                text = "IA 1" if winner == 1 else "IA 2"

            messagebox.showinfo("victory", f"{text} a gagné !")
            self.window.destroy()
            return True
        return False

# start
if __name__ == "__main__":
    root = tk.Tk()
    app = GameUI(root)
    root.mainloop()
