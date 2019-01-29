import numpy as np
from numpy import rot90, fliplr, flipud

from itertools import product


def compose(op1, op2):
    def f(m):
        return op1(op2(m))
    f.__name__ = op1.__name__ + '_' + op2.__name__
    return f


def id(m):
    return m


def rot180(m):
    return rot90(m, k=2)


def rot270(m):
    return rot90(m, k=-1)


def equal(p1, p2):
    if p1.shape == p2.shape:
        return np.all(p1 == p2)
    return False


OPS = list(map(compose, *zip(*product([rot90, rot180, rot270], [id, fliplr, flipud]))))


PIECES = {
    1: np.array([[1, 1, 1],
                 [0, 0, 1],
                 [0, 0, 1]], dtype=np.int),
    2: np.array([[1, 1, 1],
                 [0, 1, 1]], dtype=np.int),
    3: np.array([[1, 1, 1],
                 [1, 0, 1]], dtype=np.int)
}


PIECES_TO_OPS = {}
for p_i, p in PIECES.items():
    ps = [p]
    PIECES_TO_OPS[p_i] = [id]
    for op in OPS:
        if all([not equal(e, op(p)) for e in ps]):
            PIECES_TO_OPS[p_i].append(op)
            ps.append(op(p))


def _place(board, piece, i, j):
    if board[i, j] == 1:
        return None

    ie = i + piece.shape[0]
    je = j + piece.shape[1]
    if ie > board.shape[0] or je > board.shape[1]:
        return None

    new_board = board.copy()
    new_board[i:ie, j:je] += piece

    if np.any(new_board > 1):
        return None

    return new_board


def _finished(board):
    return np.all(board == 1)


def _solve(board, allowed_pieces):
    for p_i in allowed_pieces:
        p = PIECES[p_i]
        for op in PIECES_TO_OPS[p_i]:
            for i in range(board.shape[0]):
                for j in range(board.shape[1]):
                    cur_move = [(p_i, op.__name__, (i, j))]
                    new_board = _place(board, op(p), i, j)
                    if new_board is not None:
                        if _finished(new_board):
                            return cur_move

                        # find solution of subproblem
                        new_allowed_pieces = allowed_pieces.copy()
                        new_allowed_pieces.remove(p_i)
                        subsoln = _solve(new_board, new_allowed_pieces)
                        if subsoln is not None:
                            return cur_move + subsoln
    return None


def solve(board_size, allowed_pieces):
    board = np.zeros(board_size, dtype=np.int)
    return _solve(board, allowed_pieces)


def main():
    # print(PIECES_TO_OPS)

    board_size = (5, 3)
    allowed_pieces = [1, 2, 3]

    soln = solve(board_size, allowed_pieces)
    print(soln)


if __name__ == "__main__":
    main()
