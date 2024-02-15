import tkinter as tk
import random

# Create a tkinter window
window = tk.Tk()
window.title("Tic Tac Toe")

# Initialize game variables
gameBoard = [[' ' for _ in range(3)] for _ in range(3)]

possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
player_turn = True
game_over_flag = False

# Define the heuristic function
def heuristic(board, player):
    player_symbol = 'O' if player == 'O' else 'X'
    opponent_symbol = 'X' if player == 'O' else 'O'

    # Calculate the number of winning opportunities for the player
    player_winning_opportunities = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = player_symbol
                if is_winner(board, player_symbol):
                    player_winning_opportunities += 1
                board[i][j] = ' '

    # Calculate the number of winning opportunities for the opponent
    opponent_winning_opportunities = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = opponent_symbol
                if is_winner(board, opponent_symbol):
                    opponent_winning_opportunities += 1
                board[i][j] = ' '

    # The heuristic value is the difference between player's and opponent's winning opportunities
    return player_winning_opportunities - opponent_winning_opportunities

# Function to check for a winner
def check_winner(player):
    player_symbol = 'O' if player == 'O' else 'X'

    for i in range(3):
        if all(gameBoard[i][j] == player_symbol for j in range(3)) or all(gameBoard[j][i] == player_symbol for j in range(3)):
            game_over(player)
            return

    if all(gameBoard[i][i] == player_symbol for i in range(3)) or all(gameBoard[i][2 - i] == player_symbol for i in range(3)):
        game_over(player)
        return

    if not possibleNumbers:
        game_over("Draw")

# Function to end the game
def game_over(winner):
    global game_over_flag
    game_over_flag = True
    if winner == "Draw":
        result_label.config(text="It's a Draw!")
    else:
        result_label.config(text=winner + " wins!")
    for row in buttons:
        for button in row:
            button["state"] = "disabled"

# Function to handle computer's move using the Greedy Algorithm
def computer_move():
    global game_over_flag
    if not possibleNumbers or game_over_flag:
        return

    best_move = None
    best_heuristic = float('inf')

    for move in possibleNumbers:
        row, col = (move - 1) // 3, (move - 1) % 3
        if gameBoard[row][col] == ' ':
            gameBoard[row][col] = 'O'

            # Calculate the heuristic value for this move
            move_heuristic = heuristic(gameBoard, 'O')

            # Undo the move
            gameBoard[row][col] = ' '

            if move_heuristic < best_heuristic:
                best_heuristic = move_heuristic
                best_move = move

    if best_move:
        row, col = (best_move - 1) // 3, (best_move - 1) % 3
        gameBoard[row][col] = 'O'
        possibleNumbers.remove(best_move)
        printGameBoard()
        check_winner('O')
        if not check_game_over():
            player_turn = True

# Function to update the game board
def printGameBoard():
    for row in range(3):
        for col in range(3):
            cell = gameBoard[row][col]
            buttons[row][col]["text"] = cell
            buttons[row][col]["state"] = "disabled" if cell != " " else "normal"

# Function to check if the game is over
def check_game_over():
    if " " not in [cell for row in gameBoard for cell in row]:
        game_over("Draw")
        return True
    return False

# Function to handle player's move
def player_move(row, col):
    global game_over_flag
    if game_over_flag:
        return
    
    if gameBoard[row][col] == " ":
        gameBoard[row][col] = "X"
        printGameBoard()
        possibleNumbers.remove(row * 3 + col + 1)
        check_winner("X")
        if not game_over_flag:
            computer_move()

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
