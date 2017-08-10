import sys
import time

sys.path.append('../')
from tictactoe import is_tic_tac_toe


def test_positive_is_tic_tac_toe():

    x_edge = 7
    y_edge = 3
    default_message_ttl = 1
    player = 'x'

    board_squares = [' '] * 9

    board_squares[0] = 'x'
    board_squares[1] = 'x'
    board_squares[2] = 'x'

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
