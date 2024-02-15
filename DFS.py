import tkinter as tk
import random

# Function to check for a winner
def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# DFS-based computer move
def computer_move():
    best_score = -float("inf")
    best_move = None
    

    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        i, j = best_move
        board[i][j] = "O"
        buttons[i][j].config(text="O")
        buttons[i][j].config(state="disabled")

        if check_winner(board, "O"):
            result_label.config(text="Computer (O) wins!")
        elif all(board[i][j] != " " for i in range(3) for j in range(3)):
            result_label.config(text="It's a draw!")

# Minimax algorithm for DFS
def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if all(board[i][j] != " " for i in range(3) for j in range(3)):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

# Player's move
def player_move(i, j):
    if board[i][j] == " ":
        board[i][j] = "X"
        buttons[i][j].config(text="X")
        buttons[i][j].config(state="disabled")

        if check_winner(board, "X"):
            result_label.config(text="Player (X) wins!")
        elif all(board[i][j] != " " for i in range(3) for j in range(3)):
            result_label.config(text="It's a draw!")
        else:
            computer_move()

# Create the tkinter window
window = tk.Tk()
window.title("Tic Tac Toe")

# Create the game board
board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None, None, None] for _ in range(3)]

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(
            window,
            text=" ",
            font=("normal", 20),
            width=6,
            height=3,
            command=lambda i=i, j=j: player_move(i, j),
        )
        buttons[i][j].grid(row=i, column=j)

# Create a label for the game result
result_label = tk.Label(window, text="", font=("normal", 16))
result_label.grid(row=3, column=0, columnspan=3)

# Start the game
window.mainloop()
