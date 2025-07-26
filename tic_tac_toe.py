import tkinter as tk
import math
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe with Minimax")
        self.board = [[" "]*3 for _ in range(3)]
        self.buttons = [[None]*3 for _ in range(3)]
        self.turn = "O"
        self.create_board()
        self.window.mainloop()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.window, text=" ", font=("Arial", 24), width=5, height=2,
                                command=lambda r=i, c=j: self.on_click(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_click(self, row, col):
        if self.board[row][col] == " " and self.turn == "O":
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")
            if self.check_winner("O"):
                self.show_result("You win!")
                return
            if not self.is_moves_left():
                self.show_result("It's a tie!")
                return
            self.turn = "X"
            self.window.after(500, self.computer_move)

    def computer_move(self):
        move = self.best_move()
        if move:
            i, j = move
            self.board[i][j] = "X"
            self.buttons[i][j].config(text="X")
            if self.check_winner("X"):
                self.show_result("Computer wins!")
                return
            if not self.is_moves_left():
                self.show_result("It's a tie!")
                return
            self.turn = "O"

    def show_result(self, msg):
        messagebox.showinfo("Game Over", msg)
        if messagebox.askyesno("Play Again", "Do you want to play another round?"):
            self.reset()
        else:
            self.window.destroy()

    def reset(self):
        self.board = [[" "]*3 for _ in range(3)]
        self.turn = "O"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_moves_left(self):
        return any(self.board[i][j] == " " for i in range(3) for j in range(3))

    def minimax(self, is_max):
        if self.check_winner("X"): return 1
        if self.check_winner("O"): return -1
        if not self.is_moves_left(): return 0

        if is_max:
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "X"
                        best = max(best, self.minimax(False))
                        self.board[i][j] = " "
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "O"
                        best = min(best, self.minimax(True))
                        self.board[i][j] = " "
            return best

    def best_move(self):
        best_score = -math.inf
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "X"
                    score = self.minimax(False)
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

# Start GUI
TicTacToeGUI()
