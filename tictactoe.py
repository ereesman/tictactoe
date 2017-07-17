"""

A game of tic tac toe

"""

turn = 0
board = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]

def print_board():

    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3] + ' \n' +
          '-----------\n' +
          ' ' + board[4] + ' | ' + board[5] + ' | ' + board[6] + ' \n' +
          '-----------\n' +
          ' ' + board[7] + ' | ' + board[8] + ' | ' + board[9] + ' \n')

def is_tic_tac_toe(player):

    # top to bottom check
    if (board[1] == player and board[2] == player and board[3] == player):
        return True
    elif (board[4] == player and board[5] == player and board[6] == player):
        return True
    elif (board[7] == player and board[8] == player and board[9] == player):
        return True
    # left to right check
    if (board[1] == player and board[4] == player and board[7] == player):
        return True
    elif (board[2] == player and board[5] == player and board[8] == player):
        return True
    elif (board[3] == player and board[6] == player and board[9] == player):
        return True
    # diagonal check
    if (board[1] == player and board[5] == player and board[9] == player):
        return True
    elif (board[3] == player and board[5] == player and board[7] == player):
        return True
    else:
        return False

def is_game_over():

    if turn >= 8:
        return True
    if is_tic_tac_toe('x'):
        print_board()
        print('Game over! x wins!')
        return True
    if is_tic_tac_toe('o'):
        print_board()
        print('Game over! o wins!')
        return True
    else:
        return False

def game_loop():
    
    global board
    global turn
    
    # while game is not over, take user input by location
    while not is_game_over():
        print('Turn: {}').format(turn)
        print_board()

    # update board at location with x if (turn % 2 == 0), else o
        if (turn % 2 == 0):
            move = input('Player x turn, enter a board position 1...9: ')
            if (board[move] == ' '):
                board[move] = 'x'
                turn += 1
            else:
                print('Board position is occupied!')
        else:
            move = input('Player o turn, enter a board position 1...9: ')
            if (board[move] == ' '):
                board[move] = 'o'
                turn += 1
            else:
                print('Board position is occupied!')

if __name__ == '__main__':
    game_loop()
