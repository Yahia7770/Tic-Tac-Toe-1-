import tkinter as tk
import random

# Create a tkinter window
window = tk.Tk()
window.title("Tic Tac Toe")

# Initialize game variables
gameBoard = [[' ' for _ in range(3)] for _ in range(3)]
possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
player_turn = True

# Function to update the game board
def printGameBoard():
    for row in range(3):
        for col in range(3):
            cell = gameBoard[row][col]
            buttons[row][col]["text"] = cell
            buttons[row][col]["state"] = "disabled" if cell != " " else "normal"

# Function to handle player's move
def player_move(row, col):
    global player_turn
    if gameBoard[row][col] == " ":
        gameBoard[row][col] = "X"
        printGameBoard()
        possibleNumbers.remove(row * 3 + col + 1)
        player_turn = False
        check_winner()
        if not player_turn:
            computer_move()

# Function to handle computer's move
def computer_move():
    if not possibleNumbers:
        return

    best_move = bfs_find_best_move(gameBoard, possibleNumbers)
    row, col = (best_move - 1) // 3, (best_move - 1) % 3
    gameBoard[row][col] = "O"
    possibleNumbers.remove(best_move)
    printGameBoard()
    check_winner()
    player_turn = True

# Function to check for a winner
def check_winner():
    for i in range(3):
        if all(gameBoard[i][j] == "X" for j in range(3)) or all(gameBoard[j][i] == "X" for j in range(3)):
            game_over("X")
            return
        if all(gameBoard[i][j] == "O" for j in range(3)) or all(gameBoard[j][i] == "O" for j in range(3)):
            game_over("O")
            return

    if all(gameBoard[i][i] == "X" for i in range(3)) or all(gameBoard[i][2 - i] == "X" for i in range(3)):
        game_over("X")
        return
    if all(gameBoard[i][i] == "O" for i in range(3)) or all(gameBoard[i][2 - i] == "O" for i in range(3)):
        game_over("O")
        return

    if not possibleNumbers:
        game_over("Draw")

# Function to end the game
def game_over(winner):
    if winner == "Draw":
        result_label.config(text="It's a Draw!")
    else:
        result_label.config(text=winner + " wins!")
    for row in buttons:
        for button in row:
            button["state"] = "disabled"

# BFS-based computer move
def bfs_find_best_move(board, available_moves):
    best_score = -float("inf")
    best_move = None

    for move in available_moves:
        row, col = (move - 1) // 3, (move - 1) % 3
        new_board = [row[:] for row in board]
        new_board[row][col] = "O"
        score = bfs_minimax(new_board, "X")
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

# BFS-based minimax algorithm
def bfs_minimax(board, player):
    if check_winner_bfs(board, "O"):
        return 1
    if check_winner_bfs(board, "X"):
        return -1
    if not any(" " in row for row in board):
        return 0

    best_score = -float("inf") if player == "O" else float("inf")

    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                new_board = [row[:] for row in board]
                new_board[i][j] = player
                if player == "O":
                    score = bfs_minimax(new_board, "X")
                    best_score = max(best_score, score)
                else:
                    score = bfs_minimax(new_board, "O")
                    best_score = min(best_score, score)

    return best_score

# Function to check for a winner in the BFS minimax algorithm
def check_winner_bfs(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Create buttons for the game board
buttons = [[None, None, None], [None, None, None], [None, None, None]]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(window, text=" ", width=10, height=4, command=lambda row=row, col=col: player_move(row, col))
        buttons[row][col].grid(row=row, column=col)

# Label for game result
result_label = tk.Label(window, text="", font=("Helvetica", 16))
result_label.grid(row=3, column=0, columnspan=3)

# Start the game with player's move
printGameBoard()

window.mainloop()
