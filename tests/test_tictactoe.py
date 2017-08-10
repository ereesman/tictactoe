import sys
import time
import pytest

sys.path.append('../')
from tictactoe import is_tic_tac_toe


@pytest.mark.parametrize("board_squares,player",
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
