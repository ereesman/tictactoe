import time
import curses
from curses import wrapper

"""
A game of tic tac toe
"""

board = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
turn = 1

def print_board(stdscr):
    global board

    stdscr.addstr(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3] + ' \n' +
                  '-----------\n' +
                  ' ' + board[4] + ' | ' + board[5] + ' | ' + board[6] + ' \n' +
                  '-----------\n' +
                  ' ' + board[7] + ' | ' + board[8] + ' | ' + board[9] + ' \n')

def is_tic_tac_toe(player):
    global board

    # left to right check
    if board[1] == player and board[2] == player and board[3] == player:
        return True
    elif board[4] == player and board[5] == player and board[6] == player:
        return True
    elif board[7] == player and board[8] == player and board[9] == player:
        return True
    # top to bottom check
    if board[1] == player and board[4] == player and board[7] == player:
        return True
    elif board[2] == player and board[5] == player and board[8] == player:
        return True
    elif board[3] == player and board[6] == player and board[9] == player:
        return True
    # diagonal check
    if board[1] == player and board[5] == player and board[9] == player:
        return True
    elif board[3] == player and board[5] == player and board[7] == player:
        return True
    else:
        return False

def is_game_over(stdscr):
    global board
    global turn

    stdscr.clear()
    if is_tic_tac_toe('x'):
        stdscr.addstr('Game over! x wins!\n\n')
        print_board(stdscr)
        stdscr.refresh()
        return True
    elif is_tic_tac_toe('o'):
        stdscr.addstr('Game over! o wins!\n\n')
        print_board(stdscr)
        stdscr.refresh()
        return True
    elif turn >= 10:
        stdscr.addstr('Game over! Draw!\n\n')
        print_board(stdscr)
        stdscr.refresh()
        return True
    else:
        return False

def print_board_pos_occupied(stdscr):
    global board
    global turn

    stdscr.clear()
    stdscr.addstr('Turn: ' + str(turn) + '\n\n')
    print_board(stdscr)
    stdscr.addstr('\nBoard position is occupied!')
    stdscr.refresh()
    time.sleep(1)

def print_not_a_number(stdscr):
    global board
    global turn

    stdscr.clear()
    stdscr.addstr('Turn: ' + str(turn) + '\n\n')
    print_board(stdscr)
    stdscr.addstr('\noops, you didn\'t enter a number!')
    stdscr.refresh()
    time.sleep(1)

def game_loop(stdscr):
    global board
    global turn
    
    # inside game loop
    while not is_game_over(stdscr):

        stdscr.clear()
        stdscr.addstr('Turn: ' + str(turn) + '\n\n')
        print_board(stdscr)
        stdscr.refresh()

        if turn % 2 is not 0:
            stdscr.addstr('\nPlayer x turn, enter a board position 1...9: ')
            c = stdscr.getch()
            try:
                if board[int(chr(c))] == ' ':
                    board[int(chr(c))] = 'x'
                    turn += 1
                else:
                    print_board_pos_occupied(stdscr)
            except ValueError:
                print_not_a_number(stdscr)
        else:
            stdscr.addstr('\nPlayer o turn, enter a board position 1...9: ')
            stdscr.refresh()
            c = stdscr.getch()
            try:
                if board[int(chr(c))] == ' ':
                    board[int(chr(c))] = 'o'
                    turn += 1
                else:
                    print_board_pos_occupied(stdscr)
            except ValueError:
                print_not_a_number(stdscr)

    input('\nCTRL + C TO EXIT')

if __name__ == '__main__':
    wrapper(game_loop)
