import sys
import time
import pytest

sys.path.append('../')
from tictactoe import is_tic_tac_toe
from tictactoe import render_horiz_rail
from tictactoe import render_horiz_wall
from tictactoe import render_game_square_lane


@pytest.mark.parametrize('board_squares,player',
                         [(['x', 'x', 'x'] + [' '] * 6,
                           'x'),
                          ([' '] * 3 + ['o', 'o', 'o'] + [' '] * 3,
                           'o')])
def test_positive_is_tic_tac_toe(board_squares, player):

    x_edge = 7
    y_edge = 3
    default_message_ttl = 1

    test_state = {
        'turn_num': 1,
        'board_squares': board_squares,
        'cursor': {
            'x': x_edge,
            'y': y_edge
        },
        'message_expire_at': time.time() + default_message_ttl
    }

    assert is_tic_tac_toe(player, test_state) is True


def test_positive_render_horiz_rail():

    step = 4
    length_without_corners = (step * 3) - 1
    expected_rail = '+' + ('-' * length_without_corners) + '+'

    assert render_horiz_rail() == expected_rail


def test_positive_render_horiz_wall():

    step = 4
    wall_len = (step * 3) + 1
    expected_wall = '-' * wall_len

    assert render_horiz_wall() == expected_wall


def test_positive_render_game_square_lane():

    board_squares = ['x', 'x', 'x'] + [' '] * 6
    test_state = {
        'turn_num': 1,
        'board_squares': board_squares,
        'cursor': {
            'x': 7,
            'y': 3
        },
        'message_expire_at': time.time() + 1
    }
    step = 4
    pad = ' ' * (step / 4)
    expected_lane_str = '|' + pad + board_squares[0] + pad + '|' \
                        + pad + board_squares[1] + pad + '|' \
                        + pad + board_squares[2] + pad + '|'

    assert render_game_square_lane(0, test_state) == expected_lane_str
