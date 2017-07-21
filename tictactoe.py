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
GAME_BOARD_TEMPLATE = '  {} | {} | {} \n ----------- \n  {} | {} | {} \n ----------- \n  {} | {} | {} \n'
TURN_MSG_TEMPLATE = 'Turn: {}\n\n'
PLAYER_TURN_MSG_TEMPLATE = '\nPlayer {} turn, enter a board position 1...9: '

state = {
    'turn_num': 1,
    'game_piece_locs': GAME_PIECE_LOCS,
    'message': {
        'data': [
            TURN_MSG_TEMPLATE.format(1),
            GAME_BOARD_TEMPLATE.format(GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2], GAME_PIECE_LOCS[3],
                                       GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5], GAME_PIECE_LOCS[6],
                                       GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8], GAME_PIECE_LOCS[9]),
            PLAYER_TURN_MSG_TEMPLATE.format('x')], 
        'expire_at': time.time() + 1
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

    logging.debug('start drawing...')
    if now < state['message']['expire_at']:
        logging.debug('message is not expired...')
        stdscr.clear()
        logging.debug('cleared screen...')
        for msg in state['message']['data']:
            stdscr.addstr(msg)
            logging.debug('drew msg: \n{0}\n'.format(msg))
    stdscr.refresh()
    logging.debug('refreshed screen...')
    logging.debug('done drawing...')

def update_state(c):
    global state
    global TURN_MSG_TEMPLATE
    global PLAYER_TURN_MSG_TEMPLATE

    player_o_turn_msg = '\nPlayer o turn, enter a board position 1...9: '
 
    if state['turn_num'] % 2 is not 0:
        try:
            if state['game_piece_locs'][int(chr(c))] == ' ':
                state['game_piece_locs'][int(chr(c))] = 'x'
                state['turn_num'] += 1
        except ValueError:
            pass
        game_board = construct_game_board(state['game_piece_locs'])
        state['message'] = {'data': [TURN_MSG_TEMPLATE.format(state['turn_num']), game_board, PLAYER_TURN_MSG_TEMPLATE.format('x')], 'expire_at': time.time() + 1}
    else:
        try:
            if state['game_piece_locs'][int(chr(c))] == ' ':
                state['game_piece_locs'][int(chr(c))] = 'o'
                state['turn_num'] += 1
        except ValueError:
            pass
        game_board = construct_game_board(state['game_piece_locs'])
        state['message'] = {'data': [TURN_MSG_TEMPLATE.format(state['turn_num']), game_board, PLAYER_TURN_MSG_TEMPLATE.format('o')], 'expire_at': time.time() + 1}


def game_loop(stdscr):
    global state

    logging.debug('GAME START!')

    while not is_game_over(stdscr):
        logging.debug('START GAME LOOP!')
        now = time.time()
        draw(stdscr, now)
        logging.debug('star...')
        curses.napms(100)
        logging.debug('done napping...')
        c = stdscr.getch()
        if c is not None:
            logging.debug('received keypress...')
            update_state(c)
    draw(stdscr, now)

    input('\nCTRL + C TO EXIT')

if __name__ == '__main__':
    logging.basicConfig(filename='tictactoe.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    curses_wrapper(game_loop)
