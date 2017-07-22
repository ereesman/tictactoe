import time
import logging
import curses
from curses import wrapper as curses_wrapper

"""
A game of tic tac toe

TODO(eddie):
* idempotent draw routine
* semi-blocking event loop

"""
GAME_PIECE_LOCS = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
GAME_BOARD_TEMPLATE = '\n\n     +-----------+\n     | {} | {} | {} |\n     |-----------| \n     | {} | {} | {} |\n     |-----------| \n     | {} | {} | {} |\n     +-----------+'
PLAYER_TURN_MSG_TEMPLATE = '\n\n    Player {}\'s turn!'

state = {
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

def construct_game_board(game_piece_locs):
    return GAME_BOARD_TEMPLATE.format(GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2], GAME_PIECE_LOCS[3],
                                      GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5], GAME_PIECE_LOCS[6],
                                      GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8], GAME_PIECE_LOCS[9])

def is_tic_tac_toe(player):
    global state

    # left to right check
    if state['game_piece_locs'][1] == player and state['game_piece_locs'][2] == player and state['game_piece_locs'][3] == player:
        return True
    elif state['game_piece_locs'][4] == player and state['game_piece_locs'][5] == player and state['game_piece_locs'][6] == player:
        return True
    elif state['game_piece_locs'][7] == player and state['game_piece_locs'][8] == player and state['game_piece_locs'][9] == player:
        return True
    # top to bottom check
    if state['game_piece_locs'][1] == player and state['game_piece_locs'][4] == player and state['game_piece_locs'][7] == player:
        return True
    elif state['game_piece_locs'][2] == player and state['game_piece_locs'][5] == player and state['game_piece_locs'][8] == player:
        return True
    elif state['game_piece_locs'][3] == player and state['game_piece_locs'][6] == player and state['game_piece_locs'][9] == player:
        return True
    # diagonal check
    if state['game_piece_locs'][1] == player and state['game_piece_locs'][5] == player and state['game_piece_locs'][9] == player:
        return True
    elif state['game_piece_locs'][3] == player and state['game_piece_locs'][5] == player and state['game_piece_locs'][7] == player:
        return True
    else:
        return False

def is_game_over(stdscr):
    global state

    x_wins_msg = 'Game over! x wins!\n\n'
    o_wins_msg = 'Game over! o wins!\n\n'
    draw_msg = 'Game over! Draw!\n\n'

    stdscr.clear()
    if is_tic_tac_toe('x'):
        return True
    elif is_tic_tac_toe('o'):
        return True
    elif state['turn_num'] == 10:
        return True
    else:
        return False

def draw(stdscr, now):
    global state

    stdscr.clear()
    logging.debug('cleared screen...')
    logging.debug('start drawing...')
    if now < state['message']['expire_at']:
        logging.debug('message is not expired...')
        for msg in state['message']['data']:
            stdscr.addstr(msg)
            logging.debug('drew message: \n{0}\n'.format(msg))
    # move the cursor
    stdscr.addstr(state['cursor']['y'], state['cursor']['x'], '')
    logging.debug('moved cursor to {0},{1}'.format(state['cursor']['y'], state['cursor']['x']))
    stdscr.refresh()
    logging.debug('refreshed screen...')
    logging.debug('done drawing...')

def update_state(stdscr, c):
    global state
    global PLAYER_TURN_MSG_TEMPLATE

    cursorMoved = False

    try:
        if chr(c) == 'a':
            if state['cursor']['x'] > 7:
                state['cursor']['x'] -= 4
                cursorMoved = True
                logging.debug('cursor move left')
        if chr(c) == 'd':
            if state['cursor']['x'] < 12:
                state['cursor']['x'] += 4
                cursorMoved = True
                logging.debug('cursor move right')
        if chr(c) == 'w':
            if state['cursor']['y'] > 5:
                state['cursor']['y'] -= 2
                cursorMoved = True
                logging.debug('cursor move up')
        if chr(c) == 's':
            if state['cursor']['y'] < 9:
                state['cursor']['y'] += 2
                cursorMoved = True
                logging.debug('cursor move down')
    except ValueError:
        pass

    if state['turn_num'] % 2 is not 0:
        if cursorMoved:
            game_board = construct_game_board(state['game_piece_locs'])
            state['message'] = {
                'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                         game_board],
                'expire_at': time.time() + 1
            }
        else:
            try:
                if state['game_piece_locs'][int(chr(c))] == ' ':
                    state['game_piece_locs'][int(chr(c))] = 'x'
                    state['turn_num'] += 1
                    game_board = construct_game_board(state['game_piece_locs'])
                    state['message'] = {
                        'data': [PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                 game_board],
                        'expire_at': time.time() + 1
                    }
            except ValueError:
                game_board = construct_game_board(state['game_piece_locs'])
                state['message'] = {
                    'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                             game_board],
                    'expire_at': time.time() + 1
                }
    else:
        if cursorMoved:
            game_board = construct_game_board(state['game_piece_locs'])
            state['message'] = {
                'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                         game_board],
                'expire_at': time.time() + 1
            }
        else:
            try:
                if state['game_piece_locs'][int(chr(c))] == ' ':
                    state['game_piece_locs'][int(chr(c))] = 'o'
                    state['turn_num'] += 1
                    game_board = construct_game_board(state['game_piece_locs'])
                    state['message'] = {
                        'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                 game_board],
                    'expire_at': time.time() + 1
                    }
            except ValueError:
                game_board = construct_game_board(state['game_piece_locs'])
                state['message'] = {
                    'data': [PLAYER_TURN_MSG_TEMPLATE.format('x'),
                             game_board],
                    'expire_at': time.time() + 1
                }

def game_loop(stdscr):
    global state

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
        logging.debug(state)
    draw(stdscr, now)

    input('\n\n\nGAME OVER!\nCTRL + C TO QUIT!')

if __name__ == '__main__':
    logging.basicConfig(filename='tictactoe.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    curses_wrapper(game_loop)
