import time
import math
import datetime
import logging
import curses
from curses import wrapper as curses_wrapper
'''
A game of tic tac toe
'''

BOARD_SQUARES = [' '] * 9
GAME_START = None

# default time to live of a game state in seconds
DEFAULT_STATE_TTL = 1

# x and y delta of top left curses/screen
# position and top left board square
X_EDGE = 7
Y_EDGE = 3

# x and y delta of board squares
X_STEP = 4
Y_STEP = 2

BOARD_WIDTH = (X_STEP * 3) + 1
CLOCK_WIDTH = 9

HORIZONTAL_OFFSET = 5 * ' '


def init_state():
    '''
    returns the starting game state
    '''
    global GAME_START

    GAME_START = time.time()

    return {
        'turn_num': 1,
        'board_squares': BOARD_SQUARES,
        'cursor': {
            'x': X_EDGE,
            'y': Y_EDGE
        },
        'message_expire_at': time.time() + DEFAULT_STATE_TTL
    }


def calculate_time_elapsed(state):

    return str(datetime.timedelta(seconds=round(time.time() - GAME_START)))


def map_coordinate_to_index(state):

    xscreen = state['cursor']['x']
    yscreen = state['cursor']['y']

    # map from screen (curses) coordinate to real coordinate first
    xreal = (xscreen - X_EDGE) / X_STEP
    yreal = (yscreen - Y_EDGE) / Y_STEP

    # calculate index from real coordinates
    return xreal + (3 * yreal)


def map_index_to_coordinate(index):

    # map from index to real coordinates first
    xreal = int(math.ceil(index % 3))
    yreal = index // 3

    # calculate screen (curses) coordinates from real coordinates
    xscreen = (xreal * X_STEP) + X_EDGE
    yscreen = (yreal * Y_STEP) + Y_EDGE

    return (xscreen, yscreen)


def find_all_empty_squares(state):
    '''
    returns a list of indices of all empty squares
    '''
    empty_squares = []
    game_piece_array = state['board_squares']
    for i in range(0, len(game_piece_array)):
        if game_piece_array[i] == ' ':
            empty_squares.append(i)
    return empty_squares


def find_nearest_empty_square(state):
    '''
    returns an index of the nearest empty square
    '''
    idx = map_coordinate_to_index(state)
    empties = find_all_empty_squares(state)
    closest = min(empties, key=lambda x: abs(x - idx))
    return closest


def find_lowest_empty_square(state, direction, preference):
    '''
    given state return the lowest empty square by index in target direction
    '''
    game_piece_array = state['board_squares']
    if direction == 'up':
        for i in preference:  # priority order for upwards moves
            if (game_piece_array[i] == ' '
                    and map_coordinate_to_index(state) != i):
                return i
    elif direction == 'down':
        for i in preference:
            if (game_piece_array[i] == ' '
                    and map_coordinate_to_index(state) != i):
                return i
    elif direction == 'left':
        for i in preference:
            if (game_piece_array[i] == ' '
                    and map_coordinate_to_index(state) != i):
                return i
    elif direction == 'right':
        for i in preference:
            if (game_piece_array[i] == ' '
                    and map_coordinate_to_index(state) != i):
                return i
    return map_coordinate_to_index(state)  # don't move the cursor


def is_tic_tac_toe(player, state):

    # tuples are (start_index, offset)
    winning_states = [(0, 1), (3, 1), (6, 1), (0, 3), (1, 3), (2, 3), (0, 4),
                      (2, 2)]

    for s in winning_states:
        if (state['board_squares'][s[0]] == player
                and state['board_squares'][s[0] + s[1]] == player
                and state['board_squares'][s[0] + (s[1] * 2)] == player):
            return True
    return False


def is_game_over(stdscr, state):

    if is_tic_tac_toe('x', state):
        return True
    elif is_tic_tac_toe('o', state):
        return True
    elif state['turn_num'] == 10:
        return True
    else:
        return False


def draw(stdscr, state, now):

    stdscr.erase()
    if now < state['message_expire_at']:
        # draw header message
        draw_header_message(stdscr, state)
        # draw game board
        draw_game_board(stdscr, state)
        # draw timer
        draw_game_timer(stdscr, state)
    # move the cursor
    try:
        stdscr.addstr(state['cursor']['y'], state['cursor']['x'], '')
    except Exception:
        stdscr.erase()
    stdscr.refresh()


def draw_header_message(stdscr, state):

    x_turn_msg = 'Player x\'s turn!'
    o_turn_msg = 'Player o\'s turn!'
    x_win_msg = 'Player x wins!'
    o_win_msg = 'Player o wins!'
    cats_game_msg = 'Cat\'s Game!'

    if not is_game_over(stdscr, state):
        if state['turn_num'] % 2 is not 0:
            draw_string_to_curses(stdscr, x_turn_msg)
        else:
            draw_string_to_curses(stdscr, o_turn_msg)
    else:
        if is_tic_tac_toe('x', state):
            draw_string_to_curses(stdscr, x_win_msg)
        elif is_tic_tac_toe('o', state):
            draw_string_to_curses(stdscr, o_win_msg)
        else:
            draw_string_to_curses(stdscr, cats_game_msg)


def draw_game_board(stdscr, state):

    draw_string_to_curses(stdscr, render_horiz_rail(BOARD_WIDTH))
    draw_string_to_curses(stdscr, render_game_square_lane(0, state))
    draw_string_to_curses(stdscr, render_horiz_wall())
    draw_string_to_curses(stdscr, render_game_square_lane(3, state))
    draw_string_to_curses(stdscr, render_horiz_wall())
    draw_string_to_curses(stdscr, render_game_square_lane(6, state))
    draw_string_to_curses(stdscr, render_horiz_rail(BOARD_WIDTH))


def render_horiz_rail(width):

    rail_str = ''
    for i in range(0, width):
        if i == 0 or i == width - 1:
            rail_str = rail_str + '+'
        else:
            rail_str = rail_str + ('-')
    return rail_str


def render_horiz_wall():

    return '-' * BOARD_WIDTH


def render_game_square_lane(start, state):

    lane_str = '|'
    pad = ' ' * (X_STEP / 4)
    for i in range(0, 3):
        lane_str = lane_str + pad + state['board_squares'][start + i] \
                   + pad + '|'
    return lane_str


def draw_game_timer(stdscr, state):

    draw_string_to_curses(stdscr, render_horiz_rail(CLOCK_WIDTH))
    draw_string_to_curses(stdscr, '|' + calculate_time_elapsed(state) + '|')
    draw_string_to_curses(stdscr, render_horiz_rail(CLOCK_WIDTH))


def draw_string_to_curses(stdscr, string):

    try:
        stdscr.addstr('\n' + HORIZONTAL_OFFSET + string, curses.color_pair(1))
    except Exception:
        stdscr.erase()


def move_cursor_left(state):

    if state['cursor']['x'] > X_EDGE:
        state['cursor']['x'] -= X_STEP
        if state['board_squares'][map_coordinate_to_index(state)] != ' ':
            free_sq = find_lowest_empty_square(state, "left",
                                               [3, 6, 4, 0, 1, 7])
            coord = map_index_to_coordinate(free_sq)
            state['cursor']['x'] = coord[0]
            state['cursor']['y'] = coord[1]
    return state


def move_cursor_right(state):

    if state['cursor']['x'] < (X_EDGE * 2) + 1:
        state['cursor']['x'] += X_STEP
        if state['board_squares'][map_coordinate_to_index(state)] != ' ':
            if map_coordinate_to_index(state) == 0:
                free_sq = find_lowest_empty_square(state, "right",
                                                   [1, 2, 4, 5, 8, 7])
            else:
                free_sq = find_lowest_empty_square(state, "right",
                                                   [5, 8, 4, 2, 7, 1])
                coord = map_index_to_coordinate(free_sq)
                state['cursor']['x'] = coord[0]
                state['cursor']['y'] = coord[1]
    return state


def move_cursor_up(state):

    if state['cursor']['y'] > Y_EDGE:
        state['cursor']['y'] -= Y_STEP
        if state['board_squares'][map_coordinate_to_index(state)] != ' ':
            free_sq = find_lowest_empty_square(state, "up", [4, 1, 0, 2, 3, 5])
            coord = map_index_to_coordinate(free_sq)
            state['cursor']['x'] = coord[0]
            state['cursor']['y'] = coord[1]
    return state


def move_cursor_down(state):

    if state['cursor']['y'] < (Y_EDGE * 2) + 1:
        state['cursor']['y'] += Y_STEP
        if state['board_squares'][map_coordinate_to_index(state)] != ' ':
            free_sq = find_lowest_empty_square(state, "down",
                                               [4, 7, 6, 8, 5, 3])
            coord = map_index_to_coordinate(free_sq)
            state['cursor']['x'] = coord[0]
            state['cursor']['y'] = coord[1]
    return state


def increment_state_ttl(state):

    state['message_expire_at'] = time.time() + DEFAULT_STATE_TTL
    return state


def place_game_piece(player, state):

    index = map_coordinate_to_index(state)

    state['board_squares'][index] = player
    state['turn_num'] += 1
    free_sq = find_nearest_empty_square(state)
    coord = map_index_to_coordinate(free_sq)
    state['cursor']['x'] = coord[0]
    state['cursor']['y'] = coord[1]
    state = increment_state_ttl(state)


def update_state(stdscr, state, key):

    new_state = {
        'turn_num': state['turn_num'],
        'board_squares': state['board_squares'],
        'cursor': {
            'x': state['cursor']['x'],
            'y': state['cursor']['y']
        },
        'message_expire_at': state['message_expire_at']
    }

    # only enter the update routine if we received a keypress,
    # otherwise extend current state
    if key > 0:
        # determine if we only moved the cursor
        cursorMoved = False
        try:
            if key == curses.KEY_LEFT:
                new_state = move_cursor_left(state)
                cursorMoved = True
            elif key == curses.KEY_RIGHT:
                new_state = move_cursor_right(state)
                cursorMoved = True
            elif key == curses.KEY_UP:
                new_state = move_cursor_up(state)
                cursorMoved = True
            elif key == curses.KEY_DOWN:
                new_state = move_cursor_down(state)
                cursorMoved = True
            # TODO(eddie): figure out some way to collapse arrow keys
            # and wasd controls
            elif chr(key) == 'a':
                new_state = move_cursor_left(state)
                cursorMoved = True
            elif chr(key) == 'd':
                new_state = move_cursor_right(state)
                cursorMoved = True
            elif chr(key) == 'w':
                new_state = move_cursor_up(state)
                cursorMoved = True
            elif chr(key) == 's':
                new_state = move_cursor_down(state)
                cursorMoved = True
        except ValueError:
            pass

        # x's turn
        if state['turn_num'] % 2 is not 0:
            if cursorMoved:
                new_state = increment_state_ttl(new_state)
            else:
                try:
                    if key == ord(' '):  # spacebar keypress
                        place_game_piece('x', new_state)
                    else:  # not spacebar keypress
                        new_state = increment_state_ttl(new_state)
                except ValueError:
                    new_state = increment_state_ttl(new_state)
        # o's turn
        else:
            if cursorMoved:
                new_state = increment_state_ttl(new_state)
            else:
                try:
                    if key == ord(' '):  # spacebar keypress
                        place_game_piece('o', new_state)
                    else:  # not spacebar keypress
                        new_state = increment_state_ttl(new_state)
                except ValueError:
                    new_state = increment_state_ttl(new_state)
        return new_state
    else:  # persist current screen state
        new_state = increment_state_ttl(new_state)
        return new_state


def draw_banner(stdscr):

    b = open('banner.txt', 'r')
    banner = b.read()
    curses.curs_set(0)
    game_is_started = False
    while not game_is_started:
        draw_string_to_curses(stdscr, banner)
        stdscr.refresh()
        curses.napms(100)
        c = stdscr.getch()
        if c > 0:
            game_is_started = True
        else:
            stdscr.erase()


def draw_game_over(stdscr, state, now):

    state['cursor']['y'] = 0
    state['cursor']['x'] = 0
    draw(stdscr, state, now)
    try:
        input('GAME OVER! CTRL + C TO QUIT!')
    except KeyboardInterrupt:
        pass


def game_loop(stdscr):

    # color
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # non-blocking on input
    stdscr.nodelay(1)
    # allow function keys to be interpreted as a single value
    stdscr.keypad(1)

    # draw banner
    draw_banner(stdscr)

    # game start
    state = init_state()
    curses.curs_set(1)

    # main game loop
    while not is_game_over(stdscr, state):
        now = time.time()
        draw(stdscr, state, now)
        curses.napms(100)
        key = stdscr.getch()
        state = update_state(stdscr, state, key)

    draw_game_over(stdscr, state, now)


if __name__ == '__main__':
    logging.basicConfig(
        filename='tictactoe.log',
        level=logging.DEBUG,
        format='%(asctime)s %(message)s')
    curses_wrapper(game_loop)
