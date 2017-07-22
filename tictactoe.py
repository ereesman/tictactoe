import time
import datetime
import logging
import curses
from curses import wrapper as curses_wrapper

"""
A game of tic tac toe

TODO(eddie):
* idempotent draw routine
* semi-blocking event loop

"""
GAME_START = None
GAME_PIECE_LOCS = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
GAME_BOARD_TEMPLATE = '\n\n     +-----------+\n     | {0} | {1} | {2} |\n     |-----------| \n     | {3} | {4} | {5} |\n     |-----------| \n     | {6} | {7} | {8} |\n     +-----------+'
PLAYER_TURN_MSG_TEMPLATE = '\n\n    Player {}\'s turn!'
GAME_CLOCK_TEMPLATE = '\n\n\n+-------+\n|{0}|\n+-------+\n'

# TODO: factor this into a method? 'init_state()'?
STATE = {
    'turn_num': 1,
    'game_piece_locs': GAME_PIECE_LOCS,
    'message': {
        'data': [
            PLAYER_TURN_MSG_TEMPLATE.format('x'), 
            GAME_BOARD_TEMPLATE.format(GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2], GAME_PIECE_LOCS[3],
                                       GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5], GAME_PIECE_LOCS[6],
                                       GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8], GAME_PIECE_LOCS[9])],
        'expire_at': time.time() + 1
    },
    'cursor': {
        'x': 7,
        'y': 5
    }
}

def calculate_time_elapsed():
    return str(datetime.timedelta(seconds=round(time.time() - GAME_START)))

def construct_game_board(game_piece_locs):
    return GAME_BOARD_TEMPLATE.format(GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2], GAME_PIECE_LOCS[3],
                                      GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5], GAME_PIECE_LOCS[6],
                                      GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8], GAME_PIECE_LOCS[9])

def is_tic_tac_toe(player):
    global STATE

    # left to right check
    if STATE['game_piece_locs'][1] == player and STATE['game_piece_locs'][2] == player and STATE['game_piece_locs'][3] == player:
        return True
    elif STATE['game_piece_locs'][4] == player and STATE['game_piece_locs'][5] == player and STATE['game_piece_locs'][6] == player:
        return True
    elif STATE['game_piece_locs'][7] == player and STATE['game_piece_locs'][8] == player and STATE['game_piece_locs'][9] == player:
        return True
    # top to bottom check
    if STATE['game_piece_locs'][1] == player and STATE['game_piece_locs'][4] == player and STATE['game_piece_locs'][7] == player:
        return True
    elif STATE['game_piece_locs'][2] == player and STATE['game_piece_locs'][5] == player and STATE['game_piece_locs'][8] == player:
        return True
    elif STATE['game_piece_locs'][3] == player and STATE['game_piece_locs'][6] == player and STATE['game_piece_locs'][9] == player:
        return True
    # diagonal check
    if STATE['game_piece_locs'][1] == player and STATE['game_piece_locs'][5] == player and STATE['game_piece_locs'][9] == player:
        return True
    elif STATE['game_piece_locs'][3] == player and STATE['game_piece_locs'][5] == player and STATE['game_piece_locs'][7] == player:
        return True
    else:
        return False

def is_game_over(stdscr):
    global STATE

    x_wins_msg = 'Game over! x wins!\n\n'
    o_wins_msg = 'Game over! o wins!\n\n'
    draw_msg = 'Game over! Draw!\n\n'

    stdscr.clear()
    if is_tic_tac_toe('x'):
        return True
    elif is_tic_tac_toe('o'):
        return True
    elif STATE['turn_num'] == 10:
        return True
    else:
        return False

def draw(stdscr, now):
    global STATE

    stdscr.clear()
    logging.debug('cleared screen...')
    logging.debug('start drawing...')
    if now < STATE['message']['expire_at']:
        logging.debug('message is not expired...')
        for msg in STATE['message']['data']:
            stdscr.addstr(msg)
            logging.debug('drew message: \n{0}\n'.format(msg))
    # move the cursor
    stdscr.addstr(STATE['cursor']['y'], STATE['cursor']['x'], '')
    logging.debug('moved cursor to {0},{1}'.format(STATE['cursor']['y'], STATE['cursor']['x']))
    stdscr.refresh()
    logging.debug('refreshed screen...')
    logging.debug('done drawing...')

def update_state(stdscr, c):
    global STATE
    global PLAYER_TURN_MSG_TEMPLATE

    cursorMoved = False

    try:
        if chr(c) == 'a':
            if STATE['cursor']['x'] > 7:
                STATE['cursor']['x'] -= 4
                cursorMoved = True
                logging.debug('cursor move left')
        if chr(c) == 'd':
            if STATE['cursor']['x'] < 12:
                STATE['cursor']['x'] += 4
                cursorMoved = True
                logging.debug('cursor move right')
        if chr(c) == 'w':
            if STATE['cursor']['y'] > 5:
                STATE['cursor']['y'] -= 2
                cursorMoved = True
                logging.debug('cursor move up')
        if chr(c) == 's':
            if STATE['cursor']['y'] < 9:
                STATE['cursor']['y'] += 2
                cursorMoved = True
                logging.debug('cursor move down')
    except ValueError:
        pass

    if STATE['turn_num'] % 2 is not 0:
        if cursorMoved:
            game_board = construct_game_board(STATE['game_piece_locs'])
            STATE['message'] = {
                'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                         game_board,
                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                'expire_at': time.time() + 1
            }
        else:
            try:
                if STATE['game_piece_locs'][int(chr(c))] == ' ':
                    STATE['game_piece_locs'][int(chr(c))] = 'x'
                    STATE['turn_num'] += 1
                    game_board = construct_game_board(STATE['game_piece_locs'])
                    STATE['message'] = {
                        'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                 game_board,
                                 GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                        'expire_at': time.time() + 1
                    }
            except ValueError:
                game_board = construct_game_board(STATE['game_piece_locs'])
                STATE['message'] = {
                    'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                             game_board,
                             GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                    'expire_at': time.time() + 1
                }
    else:
        if cursorMoved:
            game_board = construct_game_board(STATE['game_piece_locs'])
            STATE['message'] = {
                'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                         game_board,
                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                'expire_at': time.time() + 1
            }
        else:
            try:
                if STATE['game_piece_locs'][int(chr(c))] == ' ':
                    STATE['game_piece_locs'][int(chr(c))] = 'o'
                    STATE['turn_num'] += 1
                    game_board = construct_game_board(STATE['game_piece_locs'])
                    STATE['message'] = {
                        'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                 game_board,
                                 GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                    'expire_at': time.time() + 1
                    }
            except ValueError:
                game_board = construct_game_board(STATE['game_piece_locs'])
                STATE['message'] = {
                    'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                             game_board,
                             GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                    'expire_at': time.time() + 1
                }

def game_loop(stdscr):
    global STATE
    global GAME_START

    stdscr.nodelay(1)

    GAME_START = time.time()

    logging.debug('GAME START!')

    while not is_game_over(stdscr):
        logging.debug('START GAME LOOP!')
        now = time.time()
        draw(stdscr, now)
        logging.debug('start napping...')
        curses.napms(100)
        logging.debug('done napping...')
        c = stdscr.getch()
        if c is not None:
            logging.debug('received keypress...')
            update_state(stdscr, c)
            logging.debug('state updated...')
        logging.debug(STATE)

    STATE['cursor']['y'] = 0
    STATE['cursor']['x'] = 0
    draw(stdscr, now)
    input('GAME OVER! CTRL + C TO QUIT!')

if __name__ == '__main__':
    logging.basicConfig(filename='tictactoe.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    curses_wrapper(game_loop)
