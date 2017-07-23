import time
import sys
import datetime
import logging
import curses
from curses import wrapper as curses_wrapper

"""
A game of tic tac toe
"""

GAME_PIECE_LOCS = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
GAME_BOARD_TEMPLATE = '\n\n     +-----------+\n     | {0} | {1} | {2} |\n     |-----------| \n     | {3} | {4} | {5} |\n     |-----------| \n     | {6} | {7} | {8} |\n     +-----------+'
PLAYER_TURN_MSG_TEMPLATE = '\n\n    Player {0}\'s turn!'
GAME_CLOCK_TEMPLATE = '\n\n       +-------+\n       |{0}|\n       +-------+\n'

def init_state():
    return {
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
    },
    'game_start': time.time()
}

def calculate_time_elapsed(state):
    return str(datetime.timedelta(seconds=round(time.time() - state['game_start'])))

def calculate_hovered_square(state):
    x = state['cursor']['x'] 
    y = state['cursor']['y'] 

    if x == 7 and y == 5:
        return 0
    if x == 11 and y == 5:
        return 1
    if x == 15 and y == 5:
        return 2
    if x == 7 and y == 7:
        return 3
    if x == 11 and y == 7:
        return 4
    if x == 15 and y == 7:
        return 5
    if x == 7 and y == 9:
        return 6
    if x == 11 and y == 9:
        return 7
    if x == 15 and y == 9:
        return 8

def find_lowest_empty_square(state, direction, preference):
    """
    given state return the lowest empty square by index in target direction
    """
    game_piece_array = state['game_piece_locs']
    if direction == 'up':
        for i in preference: # priority order for upwards moves
            logging.debug('CHECKING LOCATION {}!'.format(i))
            if game_piece_array[i] == ' ':
                return i
    elif direction == 'down':
        for i in preference:
            if game_piece_array[i] == ' ':
                return i
    elif direction == 'left':
        for i in preference:
            if game_piece_array[i] == ' ':
                return i
    elif direction == 'right':
        for i in preference:
            if game_piece_array[i] == ' ':
                return i
    return calculate_hovered_square(state) # don't move the cursor

def map_index_to_coordinate(index):
    if index == 0:
        return (7, 5)
    if index == 1:
        return (11, 5)
    if index == 2:
        return (15, 5)
    if index == 3:
        return (7, 7)
    if index == 4:
        return (11, 7)
    if index == 5:
        return (15, 7)
    if index == 6:
        return (7, 9)
    if index == 7:
        return (11, 9)
    if index == 8:
        return (15, 9)

def construct_game_board(game_piece_locs):
    return GAME_BOARD_TEMPLATE.format(GAME_PIECE_LOCS[0], GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2],
                                      GAME_PIECE_LOCS[3], GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5],
                                      GAME_PIECE_LOCS[6], GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8])

def is_tic_tac_toe(player, state):
    # left to right check
    if state['game_piece_locs'][0] == player and state['game_piece_locs'][1] == player and state['game_piece_locs'][2] == player:
        return True
    elif state['game_piece_locs'][3] == player and state['game_piece_locs'][4] == player and state['game_piece_locs'][5] == player:
        return True
    elif state['game_piece_locs'][6] == player and state['game_piece_locs'][7] == player and state['game_piece_locs'][8] == player:
        return True
    # top to bottom check
    if state['game_piece_locs'][0] == player and state['game_piece_locs'][3] == player and state['game_piece_locs'][6] == player:
        return True
    elif state['game_piece_locs'][1] == player and state['game_piece_locs'][4] == player and state['game_piece_locs'][7] == player:
        return True
    elif state['game_piece_locs'][2] == player and state['game_piece_locs'][5] == player and state['game_piece_locs'][8] == player:
        return True
    # diagonal check
    if state['game_piece_locs'][0] == player and state['game_piece_locs'][4] == player and state['game_piece_locs'][8] == player:
        return True
    elif state['game_piece_locs'][2] == player and state['game_piece_locs'][4] == player and state['game_piece_locs'][6] == player:
        return True
    else:
        return False

def is_game_over(stdscr, state):
    x_wins_msg = '\n\n    Player x wins!'
    o_wins_msg = '\n\n    Player o wins!'
    draw_msg = '\n\n        Draw!'

    if is_tic_tac_toe('x', state):
        game_board = construct_game_board(state['game_piece_locs'])
        state['message'] = {
            'data': [x_wins_msg,
                     game_board,
                     GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(state))],
            'expire_at': time.time() + 1
        }
        return True
    elif is_tic_tac_toe('o', state):
        game_board = construct_game_board(state['game_piece_locs'])
        state['message'] = {
            'data': [o_wins_msg,
                     game_board,
                     GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(state))],
            'expire_at': time.time() + 1
        }
        return True
    elif state['turn_num'] == 10:
        game_board = construct_game_board(state['game_piece_locs'])
        state['message'] = {
            'data': [draw_msg,
                     game_board,
                     GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(state))],
            'expire_at': time.time() + 1
        }
        return True
    else:
        return False

def draw(stdscr, state,  now):
    stdscr.erase()
    logging.debug('cleared screen...')
    logging.debug('start drawing...')
    if now < state['message']['expire_at']:
        logging.debug('message is not expired...')
        for msg in state['message']['data']:
            try:
                stdscr.addstr(msg, curses.color_pair(1))
            except Exception:
                stdscr.erase()
            logging.debug('drew message: \n{0}\n'.format(msg))
    # move the cursor
    try:
        stdscr.addstr(state['cursor']['y'], state['cursor']['x'], '')
    except Exception:
        stdscr.erase()
    logging.debug('moved cursor to {0},{1}'.format(state['cursor']['y'], state['cursor']['x']))
    stdscr.refresh()
    logging.debug('refreshed screen...')
    logging.debug('done drawing...')

def update_state(stdscr, curr_state, c):
    new_state = {
    'turn_num': curr_state['turn_num'],
    'game_piece_locs': curr_state['game_piece_locs'],
    'message': {
        'data': [],
        'expire_at': time.time() + 1
    },
    'cursor': {
        'x': curr_state['cursor']['x'],
        'y': curr_state['cursor']['y']
    },
    'game_start': curr_state['game_start']
}

    # only enter the update routine if we received a keypress, 
    # otherwise extend current state
    if c > 0: 
        # determine if we only moved the cursor
        # TODO: this routine could be made better/less brittle by making the offsets relative to
        # a fixed position, i.e. top left coordinate of the gameboard
        cursorMoved = False
        try:
            if chr(c) == 'a':
                if curr_state['cursor']['x'] > 7:
                    new_state['cursor']['x'] -= 4
                    if new_state['game_piece_locs'][calculate_hovered_square(new_state)] != ' ':
                        logging.debug('LEFT - square is not empty!')
                        free_sq = find_lowest_empty_square(new_state, "left", [3, 6, 0, 4, 1, 7])
                        logging.debug('lowest free square is: {}'.format(free_sq))
                        coord = map_index_to_coordinate(free_sq)
                        logging.debug('coord is: {}'.format(coord))
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
                    logging.debug('cursor move left')
            if chr(c) == 'd':
                if curr_state['cursor']['x'] < 12:
                    new_state['cursor']['x'] += 4
                    if new_state['game_piece_locs'][calculate_hovered_square(new_state)] != ' ':
                        logging.debug('RIGHT - square is not empty!')
                        free_sq = find_lowest_empty_square(new_state, "right", [5, 2, 8, 4, 7, 1])
                        logging.debug('lowest free square is: {}'.format(free_sq))
                        coord = map_index_to_coordinate(free_sq)
                        logging.debug('coord is: {}'.format(coord))
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
                    logging.debug('cursor move right')
            if chr(c) == 'w':
                if curr_state['cursor']['y'] > 5:
                    new_state['cursor']['y'] -= 2
                    if new_state['game_piece_locs'][calculate_hovered_square(new_state)] != ' ':
                        logging.debug('UP - square is not empty!')
                        free_sq = find_lowest_empty_square(new_state, "up", [1, 0, 2, 4, 3, 5])
                        logging.debug('lowest free square is: {}'.format(free_sq))
                        coord = map_index_to_coordinate(free_sq)
                        logging.debug('coord is: {}'.format(coord))
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
                    logging.debug('cursor move up')
            if chr(c) == 's':
                if curr_state['cursor']['y'] < 9:
                    new_state['cursor']['y'] += 2
                    if new_state['game_piece_locs'][calculate_hovered_square(new_state)] != ' ':
                        logging.debug('DOWN - square is not empty!')
                        free_sq = find_lowest_empty_square(new_state, "down", [7, 6, 8, 5, 4, 6])
                        logging.debug('lowest free square is: {}'.format(free_sq))
                        coord = map_index_to_coordinate(free_sq)
                        logging.debug('coord is: {}'.format(coord))
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
                    logging.debug('cursor move down')
        except ValueError:
            pass

        index = calculate_hovered_square(new_state)
        logging.debug('hovered square/index: {0}'.format(index))

        # x's turn
        if curr_state['turn_num'] % 2 is not 0:
            if cursorMoved:
                game_board = construct_game_board(new_state['game_piece_locs'])
                new_state['message'] = {
                    'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                             game_board,
                             GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                    'expire_at': time.time() + 1
                }
            else:
                try:
                    if c == ord(' '): # spacebar keypress
                        if curr_state['game_piece_locs'][index] == ' ':
                            new_state['game_piece_locs'][index] = 'x'
                            new_state['turn_num'] += 1
                            free_sq = find_lowest_empty_square(new_state, "right", [0, 1, 2, 3, 4, 5, 6, 7, 8])
                            logging.debug('lowest free square is: {}'.format(free_sq))
                            coord = map_index_to_coordinate(free_sq)
                            logging.debug('coord is: {}'.format(coord))
                            new_state['cursor']['x'] = coord[0]
                            new_state['cursor']['y'] = coord[1]
                            game_board = construct_game_board(new_state['game_piece_locs'])
                            new_state['message'] = {
                                'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                         game_board,
                                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                                'expire_at': time.time() + 1
                            }
                            logging.debug('set it back to player o\'s turn!')
                        else:
                            new_state['game_piece_locs'][index] = 'x'
                            new_state['turn_num'] += 1
                            game_board = construct_game_board(new_state['game_piece_locs'])
                            new_state['message'] = {
                                'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                         game_board,
                                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                                'expire_at': time.time() + 1
                            }
                    else: # not spacebar keypress
                        game_board = construct_game_board(new_state['game_piece_locs'])
                        new_state['message'] = {
                            'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                     game_board,
                                     GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                            'expire_at': time.time() + 1
                        }
                        logging.debug('leaving it set to player x\'s turn!')
                except ValueError:
                    logging.debug('caught ValueError, still player x\'s turn!')
                    game_board = construct_game_board(new_state['game_piece_locs'])
                    new_state['message'] = {
                        'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                 game_board,
                                 GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                        'expire_at': time.time() + 1
                    }
        # o's turn
        else:
            if cursorMoved:
                game_board = construct_game_board(new_state['game_piece_locs'])
                new_state['message'] = {
                    'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                             game_board,
                             GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                    'expire_at': time.time() + 1
                }
            else:
                try:
                    if c == ord(' '): # spacebar keypress
                        if curr_state['game_piece_locs'][index] == ' ':
                            new_state['game_piece_locs'][index] = 'o'
                            new_state['turn_num'] += 1
                            free_sq = find_lowest_empty_square(new_state, "right", [0, 1, 2, 3, 4, 5, 6, 7, 8])
                            logging.debug('lowest free square is: {}'.format(free_sq))
                            coord = map_index_to_coordinate(free_sq)
                            logging.debug('coord is: {}'.format(coord))
                            new_state['cursor']['x'] = coord[0]
                            new_state['cursor']['y'] = coord[1]
                            game_board = construct_game_board(new_state['game_piece_locs'])
                            new_state['message'] = {
                                'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                         game_board,
                                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                                'expire_at': time.time() + 1
                            }
                            logging.debug('set it back to player x\'s turn!')
                        else:
                            new_state['game_piece_locs'][index] = 'o'
                            new_state['turn_num'] += 1
                            game_board = construct_game_board(new_state['game_piece_locs'])
                            new_state['message'] = {
                                'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                         game_board,
                                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                                'expire_at': time.time() + 1
                            }                            
                    else: # not spacebar keypress
                        game_board = construct_game_board(new_state['game_piece_locs'])
                        new_state['message'] = {
                            'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                     game_board,
                                     GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                            'expire_at': time.time() + 1
                        }
                        logging.debug('leaving it set to player o\'s turn!')
                except ValueError:
                    logging.debug('caught ValueError, still player o\'s turn!')
                    game_board = construct_game_board(new_state['game_piece_locs'])
                    new_state['message'] = {
                        'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                 game_board,
                                 GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                        'expire_at': time.time() + 1
                    }
        return new_state
    else: # persist current screen state
        if new_state['turn_num'] % 2 is not 0:
            game_board = construct_game_board(new_state['game_piece_locs'])
            new_state['message'] = {
                'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                         game_board,
                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                'expire_at': time.time() + 1
            }
        else:
            game_board = construct_game_board(new_state['game_piece_locs'])
            new_state['message'] = {
                'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                         game_board,
                         GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(new_state))],
                'expire_at': time.time() + 1
            }
        return new_state

def game_loop(stdscr):
    # color
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # non-blocking on input
    stdscr.nodelay(1)

    # draw banner
    b = open('banner.txt', 'r')
    banner = b.read()
    curses.curs_set(0)
    game_is_started = False
    while not game_is_started:
        try:
            stdscr.addstr(banner, curses.color_pair(1))
            stdscr.refresh()
            curses.napms(100)
        except Exception:
            stdscr.erase()
        c = stdscr.getch()
        if c == ord(' '):
            game_is_started = True
        else:
            stdscr.erase()

    # game start
    state = init_state()
    curses.curs_set(1)
    # main game loop
    while not is_game_over(stdscr, state):
        logging.debug('START GAME LOOP!')
        now = time.time()
        draw(stdscr, state, now)
        logging.debug('start napping...')
        curses.napms(100)
        logging.debug('done napping...')
        c = stdscr.getch()
        logging.debug('UPDATING STATE!')
        state = update_state(stdscr, state, c)
        logging.debug('STATE UPDATED!')
        logging.debug(state)
        logging.debug('END GAME LOOP!')

    state['cursor']['y'] = 0
    state['cursor']['x'] = 0
    draw(stdscr, state, now)
    input('GAME OVER! CTRL + C TO QUIT!')

if __name__ == '__main__':
    logging.basicConfig(filename='tictactoe.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    curses_wrapper(game_loop)
