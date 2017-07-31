import time
import datetime
import logging
import curses
from curses import wrapper as curses_wrapper
"""
A game of tic tac toe
"""

GAME_PIECE_LOCS = [' '] * 9

PLAYER_TURN_MSG_TEMPLATE = ('\n' + '    ' + 'Player {0}\'s turn!')

GAME_BOARD_TEMPLATE = (
    '\n' + '     ' + '+-----------+' + '\n' + '     ' + '| {0} | {1} | {2} |' +
    '\n' + '     ' + '|-----------|' + '\n' + '     ' + '| {3} | {4} | {5} |' +
    '\n' + '     ' + '|-----------|' + '\n' + '     ' + '| {6} | {7} | {8} |' +
    '\n' + '     ' + '+-----------+')

GAME_CLOCK_TEMPLATE = ('\n' + '       ' + '+-------+' + '\n' + '       ' +
                       '|{0}|' + '\n' + '       ' + '+-------+' + '\n')


def init_state():

    return {
        'turn_num': 1,
        'game_piece_locs': GAME_PIECE_LOCS,
        'message': {
            'data': [
                PLAYER_TURN_MSG_TEMPLATE.format('x'),
                GAME_BOARD_TEMPLATE.format(
                    GAME_PIECE_LOCS[0], GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2],
                    GAME_PIECE_LOCS[3], GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5],
                    GAME_PIECE_LOCS[6], GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8])
            ],
            'expire_at':
            time.time() + 1
        },
        'cursor': {
            'x': 7,
            'y': 3
        },
        'game_start': time.time()
    }


def calculate_time_elapsed(state):

    return str(
        datetime.timedelta(seconds=round(time.time() - state['game_start'])))


def calculate_hovered_square(state):

    x = state['cursor']['x']
    y = state['cursor']['y']

    if x == 7 and y == 3:
        return 0
    if x == 11 and y == 3:
        return 1
    if x == 15 and y == 3:
        return 2
    if x == 7 and y == 5:
        return 3
    if x == 11 and y == 5:
        return 4
    if x == 15 and y == 5:
        return 5
    if x == 7 and y == 7:
        return 6
    if x == 11 and y == 7:
        return 7
    if x == 15 and y == 7:
        return 8


def map_index_to_coordinate(index):
    """
    TODO(eddie): this could be better ala non-hardcoded coords
    """

    if index == 0:
        return (7, 3)
    if index == 1:
        return (11, 3)
    if index == 2:
        return (15, 3)
    if index == 3:
        return (7, 5)
    if index == 4:
        return (11, 5)
    if index == 5:
        return (15, 5)
    if index == 6:
        return (7, 7)
    if index == 7:
        return (11, 7)
    if index == 8:
        return (15, 7)


def find_all_empty_squares(state):
    """
    returns a list of indices of all empty squares
    """
    empty_squares = []
    game_piece_array = state['game_piece_locs']
    for i in range(0, len(game_piece_array) - 1):
        if game_piece_array[i] == ' ':
            empty_squares.append(i)
    logging.debug("FOUND ALL EMPTY SQUARES: {}".format(empty_squares))
    return empty_squares


def find_nearest_empty_square(state):
    """
    returns an index of the nearest empty square
    """
    idx = calculate_hovered_square(state)
    empties = find_all_empty_squares(state)
    closest = min(empties, key=lambda x: abs(x - idx))
    return closest


def find_lowest_empty_square(state, direction, preference):
    """
    given state return the lowest empty square by index in target direction
    """
    game_piece_array = state['game_piece_locs']
    if direction == 'up':
        for i in preference:  # priority order for upwards moves
            if (game_piece_array[i] == ' '
                    and calculate_hovered_square(state) != i):
                return i
    elif direction == 'down':
        for i in preference:
            if (game_piece_array[i] == ' '
                    and calculate_hovered_square(state) != i):
                return i
    elif direction == 'left':
        for i in preference:
            if (game_piece_array[i] == ' '
                    and calculate_hovered_square(state) != i):
                return i
    elif direction == 'right':
        for i in preference:
            if (game_piece_array[i] == ' '
                    and calculate_hovered_square(state) != i):
                return i
    return calculate_hovered_square(state)  # don't move the cursor


def construct_game_board(game_piece_locs):

    return GAME_BOARD_TEMPLATE.format(
        GAME_PIECE_LOCS[0], GAME_PIECE_LOCS[1], GAME_PIECE_LOCS[2],
        GAME_PIECE_LOCS[3], GAME_PIECE_LOCS[4], GAME_PIECE_LOCS[5],
        GAME_PIECE_LOCS[6], GAME_PIECE_LOCS[7], GAME_PIECE_LOCS[8])


def is_tic_tac_toe(player, state):

    # left to right check
    if (state['game_piece_locs'][0] == player
            and state['game_piece_locs'][1] == player
            and state['game_piece_locs'][2] == player):
        return True
    elif (state['game_piece_locs'][3] == player
          and state['game_piece_locs'][4] == player
          and state['game_piece_locs'][5] == player):
        return True
    elif (state['game_piece_locs'][6] == player
          and state['game_piece_locs'][7] == player
          and state['game_piece_locs'][8] == player):
        return True
    # top to bottom check
    if (state['game_piece_locs'][0] == player
            and state['game_piece_locs'][3] == player
            and state['game_piece_locs'][6] == player):
        return True
    elif (state['game_piece_locs'][1] == player
          and state['game_piece_locs'][4] == player
          and state['game_piece_locs'][7] == player):
        return True
    elif (state['game_piece_locs'][2] == player
          and state['game_piece_locs'][5] == player
          and state['game_piece_locs'][8] == player):
        return True
    # diagonal check
    if (state['game_piece_locs'][0] == player
            and state['game_piece_locs'][4] == player
            and state['game_piece_locs'][8] == player):
        return True
    elif (state['game_piece_locs'][2] == player
          and state['game_piece_locs'][4] == player
          and state['game_piece_locs'][6] == player):
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
            'data': [
                x_wins_msg, game_board,
                GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(state))
            ],
            'expire_at':
            time.time() + 1
        }
        return True
    elif is_tic_tac_toe('o', state):
        game_board = construct_game_board(state['game_piece_locs'])
        state['message'] = {
            'data': [
                o_wins_msg, game_board,
                GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(state))
            ],
            'expire_at':
            time.time() + 1
        }
        return True
    elif state['turn_num'] == 10:
        game_board = construct_game_board(state['game_piece_locs'])
        state['message'] = {
            'data': [
                draw_msg, game_board,
                GAME_CLOCK_TEMPLATE.format(calculate_time_elapsed(state))
            ],
            'expire_at':
            time.time() + 1
        }
        return True
    else:
        return False


def draw(stdscr, state, now):

    stdscr.erase()
    if now < state['message']['expire_at']:
        for msg in state['message']['data']:
            try:
                stdscr.addstr(msg, curses.color_pair(1))
            except Exception:
                stdscr.erase()
    # move the cursor
    try:
        stdscr.addstr(state['cursor']['y'], state['cursor']['x'], '')
    except Exception:
        stdscr.erase()
    stdscr.refresh()


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
        '''
        TODO(eddie): this routine could be made better/less brittle
        by making the offsets relative to
        a fixed position, i.e. top left coordinate of the gameboard
        '''
        cursorMoved = False
        try:
            if c == curses.KEY_LEFT:
                if curr_state['cursor']['x'] > 7:
                    new_state['cursor']['x'] -= 4
                    if new_state['game_piece_locs'][calculate_hovered_square(
                            new_state)] != ' ':
                        free_sq = find_lowest_empty_square(
                            curr_state, "left", [3, 6, 4, 0, 1, 7])
                        coord = map_index_to_coordinate(free_sq)
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
            elif c == curses.KEY_RIGHT:
                if curr_state['cursor']['x'] < 12:
                    new_state['cursor']['x'] += 4
                    if new_state['game_piece_locs'][calculate_hovered_square(
                            new_state)] != ' ':
                        if calculate_hovered_square(curr_state) == 0:
                            free_sq = find_lowest_empty_square(
                                curr_state, "right", [1, 2, 4, 5, 8, 7])
                        else:
                            free_sq = find_lowest_empty_square(
                                curr_state, "right", [5, 8, 4, 2, 7, 1])
                        coord = map_index_to_coordinate(free_sq)
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
            elif c == curses.KEY_UP:
                if curr_state['cursor']['y'] > 3:
                    new_state['cursor']['y'] -= 2
                    if new_state['game_piece_locs'][calculate_hovered_square(
                            new_state)] != ' ':
                        free_sq = find_lowest_empty_square(
                            curr_state, "up", [4, 1, 0, 2, 3, 5])
                        coord = map_index_to_coordinate(free_sq)
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
            elif c == curses.KEY_DOWN:
                if curr_state['cursor']['y'] < 7:
                    new_state['cursor']['y'] += 2
                    if new_state['game_piece_locs'][calculate_hovered_square(
                            new_state)] != ' ':
                        free_sq = find_lowest_empty_square(
                            curr_state, "down", [4, 7, 6, 8, 5, 3])
                        coord = map_index_to_coordinate(free_sq)
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
            # TODO(eddie): figure out some way to collapse arrow keys
            # and wasd controls
            elif chr(c) == 'a':
                if curr_state['cursor']['x'] > 7:
                    new_state['cursor']['x'] -= 4
                    if new_state['game_piece_locs'][calculate_hovered_square(
                            new_state)] != ' ':
                        free_sq = find_lowest_empty_square(
                            curr_state, "left", [3, 6, 4, 0, 1, 7])
                        coord = map_index_to_coordinate(free_sq)
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
            elif chr(c) == 'd':
                if curr_state['cursor']['x'] < 12:
                    new_state['cursor']['x'] += 4
                    if new_state['game_piece_locs'][calculate_hovered_square(
                            new_state)] != ' ':
                        if calculate_hovered_square(curr_state) == 0:
                            free_sq = find_lowest_empty_square(
                                curr_state, "right", [1, 2, 4, 5, 8, 7])
                        else:
                            free_sq = find_lowest_empty_square(
                                curr_state, "right", [5, 8, 4, 2, 7, 1])
                        coord = map_index_to_coordinate(free_sq)
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
            elif chr(c) == 'w':
                if curr_state['cursor']['y'] > 3:
                    new_state['cursor']['y'] -= 2
                    if new_state['game_piece_locs'][calculate_hovered_square(
                            new_state)] != ' ':
                        free_sq = find_lowest_empty_square(
                            curr_state, "up", [4, 1, 0, 2, 3, 5])
                        coord = map_index_to_coordinate(free_sq)
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
            elif chr(c) == 's':
                if curr_state['cursor']['y'] < 7:
                    new_state['cursor']['y'] += 2
                    if new_state['game_piece_locs'][calculate_hovered_square(
                            new_state)] != ' ':
                        free_sq = find_lowest_empty_square(
                            curr_state, "down", [4, 7, 6, 8, 5, 3])
                        coord = map_index_to_coordinate(free_sq)
                        new_state['cursor']['x'] = coord[0]
                        new_state['cursor']['y'] = coord[1]
                    cursorMoved = True
        except ValueError:
            pass

        index = calculate_hovered_square(new_state)

        # x's turn
        if curr_state['turn_num'] % 2 is not 0:
            if cursorMoved:
                game_board = construct_game_board(new_state['game_piece_locs'])
                new_state['message'] = {
                    'data': [
                        PLAYER_TURN_MSG_TEMPLATE.format('x'), game_board,
                        GAME_CLOCK_TEMPLATE.format(
                            calculate_time_elapsed(new_state))
                    ],
                    'expire_at':
                    time.time() + 1
                }
            else:
                try:
                    if c == ord(' '):  # spacebar keypress
                        if curr_state['game_piece_locs'][index] == ' ':
                            new_state['game_piece_locs'][index] = 'x'
                            new_state['turn_num'] += 1
                            free_sq = find_nearest_empty_square(new_state)
                            coord = map_index_to_coordinate(free_sq)
                            new_state['cursor']['x'] = coord[0]
                            new_state['cursor']['y'] = coord[1]
                            game_board = construct_game_board(
                                new_state['game_piece_locs'])
                            new_state['message'] = {
                                'data': [
                                    PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                    game_board,
                                    GAME_CLOCK_TEMPLATE.format(
                                        calculate_time_elapsed(new_state))
                                ],
                                'expire_at':
                                time.time() + 1
                            }
                        else:
                            new_state['game_piece_locs'][index] = 'x'
                            new_state['turn_num'] += 1
                            game_board = construct_game_board(
                                new_state['game_piece_locs'])
                            new_state['message'] = {
                                'data': [
                                    PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                    game_board,
                                    GAME_CLOCK_TEMPLATE.format(
                                        calculate_time_elapsed(new_state))
                                ],
                                'expire_at':
                                time.time() + 1
                            }
                    else:  # not spacebar keypress
                        game_board = construct_game_board(
                            new_state['game_piece_locs'])
                        new_state['message'] = {
                            'data': [
                                PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                game_board,
                                GAME_CLOCK_TEMPLATE.format(
                                    calculate_time_elapsed(new_state))
                            ],
                            'expire_at':
                            time.time() + 1
                        }
                except ValueError:
                    game_board = construct_game_board(
                        new_state['game_piece_locs'])
                    new_state['message'] = {
                        'data': [
                            PLAYER_TURN_MSG_TEMPLATE.format('x'), game_board,
                            GAME_CLOCK_TEMPLATE.format(
                                calculate_time_elapsed(new_state))
                        ],
                        'expire_at':
                        time.time() + 1
                    }
        # o's turn
        else:
            if cursorMoved:
                game_board = construct_game_board(new_state['game_piece_locs'])
                new_state['message'] = {
                    'data': [
                        PLAYER_TURN_MSG_TEMPLATE.format('o'), game_board,
                        GAME_CLOCK_TEMPLATE.format(
                            calculate_time_elapsed(new_state))
                    ],
                    'expire_at':
                    time.time() + 1
                }
            else:
                try:
                    if c == ord(' '):  # spacebar keypress
                        if curr_state['game_piece_locs'][index] == ' ':
                            new_state['game_piece_locs'][index] = 'o'
                            new_state['turn_num'] += 1
                            free_sq = find_nearest_empty_square(new_state)
                            coord = map_index_to_coordinate(free_sq)
                            new_state['cursor']['x'] = coord[0]
                            new_state['cursor']['y'] = coord[1]
                            game_board = construct_game_board(
                                new_state['game_piece_locs'])
                            new_state['message'] = {
                                'data': [
                                    PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                    game_board,
                                    GAME_CLOCK_TEMPLATE.format(
                                        calculate_time_elapsed(new_state))
                                ],
                                'expire_at':
                                time.time() + 1
                            }
                        else:
                            new_state['game_piece_locs'][index] = 'o'
                            new_state['turn_num'] += 1
                            game_board = construct_game_board(
                                new_state['game_piece_locs'])
                            new_state['message'] = {
                                'data': [
                                    PLAYER_TURN_MSG_TEMPLATE.format('x'),
                                    game_board,
                                    GAME_CLOCK_TEMPLATE.format(
                                        calculate_time_elapsed(new_state))
                                ],
                                'expire_at':
                                time.time() + 1
                            }
                    else:  # not spacebar keypress
                        game_board = construct_game_board(
                            new_state['game_piece_locs'])
                        new_state['message'] = {
                            'data': [
                                PLAYER_TURN_MSG_TEMPLATE.format('o'),
                                game_board,
                                GAME_CLOCK_TEMPLATE.format(
                                    calculate_time_elapsed(new_state))
                            ],
                            'expire_at':
                            time.time() + 1
                        }
                except ValueError:
                    game_board = construct_game_board(
                        new_state['game_piece_locs'])
                    new_state['message'] = {
                        'data': [
                            PLAYER_TURN_MSG_TEMPLATE.format('o'), game_board,
                            GAME_CLOCK_TEMPLATE.format(
                                calculate_time_elapsed(new_state))
                        ],
                        'expire_at':
                        time.time() + 1
                    }
        return new_state
    else:  # persist current screen state
        if new_state['turn_num'] % 2 is not 0:
            game_board = construct_game_board(new_state['game_piece_locs'])
            new_state['message'] = {
                'data': [
                    PLAYER_TURN_MSG_TEMPLATE.format('x'), game_board,
                    GAME_CLOCK_TEMPLATE.format(
                        calculate_time_elapsed(new_state))
                ],
                'expire_at':
                time.time() + 1
            }
        else:
            game_board = construct_game_board(new_state['game_piece_locs'])
            new_state['message'] = {
                'data': [
                    PLAYER_TURN_MSG_TEMPLATE.format('o'), game_board,
                    GAME_CLOCK_TEMPLATE.format(
                        calculate_time_elapsed(new_state))
                ],
                'expire_at':
                time.time() + 1
            }
        return new_state


def game_loop(stdscr):

    # color
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # non-blocking on input
    stdscr.nodelay(1)
    # allow function keys to be interpreted as a single value
    stdscr.keypad(1)

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
        if c > 0:
            game_is_started = True
        else:
            stdscr.erase()

    # game start
    state = init_state()
    curses.curs_set(1)
    # main game loop
    while not is_game_over(stdscr, state):
        now = time.time()
        draw(stdscr, state, now)
        curses.napms(100)
        c = stdscr.getch()
        state = update_state(stdscr, state, c)

    state['cursor']['y'] = 0
    state['cursor']['x'] = 0
    draw(stdscr, state, now)
    input('GAME OVER! CTRL + C TO QUIT!')


if __name__ == '__main__':
    logging.basicConfig(
        filename='tictactoe.log',
        level=logging.DEBUG,
        format='%(asctime)s %(message)s')
    curses_wrapper(game_loop)
