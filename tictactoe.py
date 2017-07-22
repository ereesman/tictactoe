import time
import datetime
import logging
import curses
from curses import wrapper as curses_wrapper

"""
A game of tic tac toe

TODO(eddie):
* factor initial state creation into a method? 'init_state()'?
* refactor update_state() to be a pure function, state = update_state(state)
* colors
* score(?)
* start menu(?)
* game over/player wins message
* minmax AI (computer opponent)

"""


GAME_START = None
GAME_PIECE_LOCS = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
GAME_BOARD_TEMPLATE = '\n\n     +-----------+\n     | {0} | {1} | {2} |\n     |-----------| \n     | {3} | {4} | {5} |\n     |-----------| \n     | {6} | {7} | {8} |\n     +-----------+'
PLAYER_TURN_MSG_TEMPLATE = '\n\n    Player {0}\'s turn!'
GAME_CLOCK_TEMPLATE = '\n\n       +-------+\n       |{0}|\n       +-------+\n'

STATE = {
    'turn_num': 1,
    'game_piece_locs': GAME_PIECE_LOCS,
    'message': {
        'data': [
            PLAYER_TURN_MSG_TEMPLATE.format('x'),
            GAME_BOARD_TEMPLATE.format(GAME_PIECE_LOCS[0], GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2],
                                       GAME_PIECE_LOCS[3], GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5],
                                       GAME_PIECE_LOCS[6], GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8])
        ],
        'expire_at': time.time() + 1
    },
    'cursor': {
        'x': 7,
        'y': 5
    }
}

def calculate_time_elapsed():
    return str(datetime.timedelta(seconds=round(time.time() - GAME_START)))

def calculate_hovered_square():
    index = None
    x = STATE['cursor']['x'] 
    y = STATE['cursor']['y'] 

    if x == 7 and y == 5:
        index = 0
    if x == 11 and y == 5:
        index = 1
    if x == 15 and y == 5:
        index = 2
    if x == 7 and y == 7:
        index = 3
    if x == 11 and y == 7:
        index = 4
    if x == 15 and y == 7:
        index = 5
    if x == 7 and y == 9:
        index = 6
    if x == 11 and y == 9:
        index = 7
    if x == 15 and y == 9:
        index = 8

    return index

def construct_game_board(game_piece_locs):
    return GAME_BOARD_TEMPLATE.format(GAME_PIECE_LOCS[0], GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2],
                                      GAME_PIECE_LOCS[3], GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5],
                                      GAME_PIECE_LOCS[6], GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8])

def is_tic_tac_toe(player):
    global STATE

    # left to right check
    if STATE['game_piece_locs'][0] == player and STATE['game_piece_locs'][1] == player and STATE['game_piece_locs'][2] == player:
        return True
    elif STATE['game_piece_locs'][3] == player and STATE['game_piece_locs'][4] == player and STATE['game_piece_locs'][5] == player:
        return True
    elif STATE['game_piece_locs'][6] == player and STATE['game_piece_locs'][7] == player and STATE['game_piece_locs'][8] == player:
        return True
    # top to bottom check
    if STATE['game_piece_locs'][0] == player and STATE['game_piece_locs'][3] == player and STATE['game_piece_locs'][6] == player:
        return True
    elif STATE['game_piece_locs'][1] == player and STATE['game_piece_locs'][4] == player and STATE['game_piece_locs'][7] == player:
        return True
    elif STATE['game_piece_locs'][2] == player and STATE['game_piece_locs'][5] == player and STATE['game_piece_locs'][8] == player:
        return True
    # diagonal check
    if STATE['game_piece_locs'][0] == player and STATE['game_piece_locs'][4] == player and STATE['game_piece_locs'][8] == player:
        return True
    elif STATE['game_piece_locs'][2] == player and STATE['game_piece_locs'][4] == player and STATE['game_piece_locs'][6] == player:
        return True
    else:
        return False

def is_game_over(stdscr):
    global STATE

    x_wins_msg = 'Game over! x wins!\n\n'
    o_wins_msg = 'Game over! o wins!\n\n'
    draw_msg = 'Game over! Draw!\n\n'

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

    stdscr.erase()
    logging.debug('cleared screen...')
    logging.debug('start drawing...')
    if now < STATE['message']['expire_at']:
        logging.debug('message is not expired...')
        for msg in STATE['message']['data']:
            stdscr.addstr(msg, curses.color_pair(1))
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

    # only enter the update routine if we received a keypress, 
    # otherwise extend current state
    if c > 0: 
        # determine if we only moved the cursor
        # TODO: this routine could be made better/less brittle by making the offsets relative to
        # a fixed position, i.e. top left coordinate of the gameboard
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

        index = calculate_hovered_square()
        logging.debug('hovered square/index: {0}'.format(index))

        # x's turn
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
                    if c == ord(' '): # spacebar keypress
                        if STATE['game_piece_locs'][index] == ' ':
                            STATE['game_piece_locs'][index] = 'x'
                            STATE['turn_num'] += 1
                            game_board = construct_game_board(STATE['game_piece_locs'])
                            STATE['message'] = {
                                'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                         game_board,
                                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                                'expire_at': time.time() + 1
                            }
                            logging.debug('set it back to player o\'s turn!')
                    else: # not spacebar keypress
                        game_board = construct_game_board(STATE['game_piece_locs'])
                        STATE['message'] = {
                            'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                     game_board,
                                     GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                            'expire_at': time.time() + 1
                        }
                        logging.debug('leaving it set to player x\'s turn!')
                except ValueError:
                    logging.debug('caught ValueError, still player x\'s turn!')
                    game_board = construct_game_board(STATE['game_piece_locs'])
                    STATE['message'] = {
                        'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                 game_board,
                                 GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                        'expire_at': time.time() + 1
                    }
        # o's turn
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
                    if c == ord(' '): # spacebar keypress
                        if STATE['game_piece_locs'][index] == ' ':
                            STATE['game_piece_locs'][index] = 'o'
                            STATE['turn_num'] += 1
                            game_board = construct_game_board(STATE['game_piece_locs'])
                            STATE['message'] = {
                                'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                         game_board,
                                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                                'expire_at': time.time() + 1
                            }
                            logging.debug('set it back to player x\'s turn!')
                    else: # not spacebar keypress
                        game_board = construct_game_board(STATE['game_piece_locs'])
                        STATE['message'] = {
                            'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                     game_board,
                                     GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                            'expire_at': time.time() + 1
                        }
                        logging.debug('leaving it set to player o\'s turn!')
                except ValueError:
                    logging.debug('caught ValueError, still player o\'s turn!')
                    game_board = construct_game_board(STATE['game_piece_locs'])
                    STATE['message'] = {
                        'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                 game_board,
                                 GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                        'expire_at': time.time() + 1
                    }
    else: # persist current screen state
        if STATE['turn_num'] % 2 is not 0:
            game_board = construct_game_board(STATE['game_piece_locs'])
            STATE['message'] = {
                'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                         game_board,
                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed())],
                'expire_at': time.time() + 1
            }
        else:
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

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # non-blocking on input
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
        logging.debug('UPDATING STATE!')
        update_state(stdscr, c)
        logging.debug('STATE UPDATED!')
        logging.debug(STATE)
        logging.debug('END GAME LOOP!')

    STATE['cursor']['y'] = 0
    STATE['cursor']['x'] = 0
    draw(stdscr, now)
    input('GAME OVER! CTRL + C TO QUIT!')

if __name__ == '__main__':
    logging.basicConfig(filename='tictactoe.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    curses_wrapper(game_loop)
