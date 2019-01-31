import numpy as np
from numpy import rot90, fliplr

from itertools import product


PIECES = {
    'orange': np.array([[1, 1, 1],
                        [0, 0, 1],
                        [0, 0, 1]], dtype=np.int),
    'purple': np.array([[1, 1, 1],
                        [0, 1, 1]], dtype=np.int),
    'yellow': np.array([[1, 1, 1],
                        [1, 0, 1]], dtype=np.int)
}

PIECE_FLAGS = {key: item+1 for (key, item) in zip(PIECES, range(len(PIECES)))}

def get_piece_configs(piece):
    config_list = []
    for num_rotate in range(3):
        piece_candidate = rot90(piece, k=num_rotate)
        if not is_piece_in_list(piece_candidate, config_list):
            config_list.append(piece_candidate)
        piece_candidate = fliplr(piece_candidate)
        if not is_piece_in_list(piece_candidate, config_list):
            config_list.append(piece_candidate)
    return config_list


def is_piece_in_list(piece, piece_list):
    is_flag = False
    for old_piece in piece_list:
        if equal(old_piece, piece):
            is_flag = True
    return is_flag

def equal(p1, p2):
    if p1.shape == p2.shape:
        return np.all(p1 == p2)
    return False


def _place(board, piece, position, flag):
    new_board = board.copy()
    new_board[position[0]:position[0] + piece.shape[0],
        position[1]:position[1] + piece.shape[1]] += flag*piece

    old_empty_spaces = np.sum(board == 0)
    new_empty_spaces = np.sum(new_board == 0)

    if new_empty_spaces != old_empty_spaces - 5:
        return None
    else:
        return new_board


def _finished(board):
    return np.all(board)


def _solve(board, allowed_pieces):

    for piece_color in allowed_pieces:
        new_piece = PIECES[piece_color]
        new_piece_flag = PIECE_FLAGS[piece_color]
        for new_piece_config in get_piece_configs(new_piece):
            # print(new_piece_config)
            for i in range(board.shape[0] - new_piece_config.shape[0] + 1):
                for j in range(board.shape[1] - new_piece_config.shape[1] + 1):
                    new_board = _place(board, new_piece_config, (i, j), new_piece_flag)

                    if new_board is not None:
                        # print(new_board)
                        if _finished(new_board):
                            print(new_board)
                            return new_board


                        # find solution of subproblem
                        new_allowed_pieces = allowed_pieces.copy()
                        new_allowed_pieces.remove(piece_color)
                        subsoln = _solve(new_board, new_allowed_pieces)
                        if subsoln is not None:
                            return new_board
    return None


def solve(board_size, allowed_pieces):
    board = np.zeros(board_size, dtype=np.int)
    return _solve(board, allowed_pieces)


def main():
    # print(PIECES_TO_OPS)

    board_size = (5, 3)
    allowed_pieces = ['orange', 'purple', 'yellow']

    soln = solve(board_size, allowed_pieces)
    print(soln)


if __name__ == "__main__":
    main()
