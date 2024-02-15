import tkinter as tk
import random

# Create a tkinter window
window = tk.Tk()
window.title("Tic Tac Toe")

# Initialize game variables
gameBoard = [[' ' for _ in range(3)] for _ in range(3)]
possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
player_turn = True

# Define the heuristic function
def heuristic(board, player):
    player_symbol = 'O' if player == 'O' else 'X'
    opponent_symbol = 'X' if player == 'O' else 'O'

    # Calculate the number of winning opportunities for the player
    player_winning_opportunities = count_winning_opportunities(board, player_symbol)

    # Calculate the number of winning opportunities for the opponent
    opponent_winning_opportunities = count_winning_opportunities(board, opponent_symbol)

    # The heuristic value is the difference between player's and opponent's winning opportunities
    return player_winning_opportunities - opponent_winning_opportunities

# Function to count the number of winning opportunities for a symbol
def count_winning_opportunities(board, symbol):
    winning_opportunities = 0

    # Rows
    for row in range(3):
        if all(cell == symbol for cell in board[row]):
            winning_opportunities += 1

    # Columns
    for col in range(3):
        if all(board[row][col] == symbol for row in range(3)):
            winning_opportunities += 1

    # Diagonals
    if all(board[i][i] == symbol for i in range(3)):
        winning_opportunities += 1
    if all(board[i][2 - i] == symbol for i in range(3)):
        winning_opportunities += 1

    return winning_opportunities

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
        check_winner('X')
        if not check_game_over():
            computer_move()

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
    if winner == "Draw":
        result_label.config(text="It's a Draw!")
    else:
        result_label.config(text=winner + " wins!")
    for row in buttons:
        for button in row:
            button["state"] = "disabled"

# Function to check if the game is over
def check_game_over():
    if not possibleNumbers:
        game_over("Draw")
        return True
    return False

# Function to handle computer's move using the A* Algorithm
def computer_move():
    if not possibleNumbers:
        return

    best_move = None
    best_heuristic_cost = float('inf')

    for move in possibleNumbers:
        row, col = (move - 1) // 3, (move - 1) % 3
        if gameBoard[row][col] == ' ':
            gameBoard[row][col] = 'O'

            # Calculate the heuristic value for this move
            move_heuristic = heuristic(gameBoard, 'O')

            # Calculate the cost for this move (you can define a cost function if needed)
            move_cost = 0

            # Calculate the heuristic + cost value
            move_heuristic_cost = move_heuristic + move_cost

            # Undo the move
            gameBoard[row][col] = ' '

            if move_heuristic_cost < best_heuristic_cost:
                best_heuristic_cost = move_heuristic_cost
                best_move = move

    if best_move:
        row, col = (best_move - 1) // 3, (best_move - 1) % 3
        gameBoard[row][col] = 'O'
        possibleNumbers.remove(best_move)
        printGameBoard()
        check_winner('O')
        if not check_game_over():
            player_turn = True

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
