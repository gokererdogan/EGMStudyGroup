import numpy as np
from numpy import rot90, fliplr, flipud
import matplotlib.pyplot as plt

from itertools import product


def compose(op1, op2):
    def f(m):
        return op1(op2(m))
    if op1.__name__ == 'id':
        fname = op2.__name__
    elif op2.__name__ == 'id':
        fname = op1.__name__
    else:
        fname = op1.__name__ + '_' + op2.__name__
    f.__name__ = fname
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


_PIECES = {
    'F': np.array([[0, 1, 1],
                   [1, 1, 0],
                   [0, 1, 0]],
                  dtype=np.int),
    'I': np.array([[1],
                   [1],
                   [1],
                   [1],
                   [1]],
                  dtype=np.int),
    'L': np.array([[1, 0],
                   [1, 0],
                   [1, 0],
                   [1, 1]],
                  dtype=np.int),
    'N': np.array([[0, 1],
                   [0, 1],
                   [1, 1],
                   [1, 0]],
                  dtype=np.int),
    'P': np.array([[1, 1],
                   [1, 1],
                   [1, 0]],
                  dtype=np.int),
    'T': np.array([[1, 1, 1],
                   [0, 1, 0],
                   [0, 1, 0]],
                  dtype=np.int),
    'U': np.array([[1, 0, 1],
                   [1, 1, 1]],
                  dtype=np.int),
    'V': np.array([[0, 0, 1],
                   [0, 0, 1],
                   [1, 1, 1]],
                  dtype=np.int),
    'W': np.array([[0, 0, 1],
                   [0, 1, 1],
                   [1, 1, 0]],
                  dtype=np.int),
    'X': np.array([[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]],
                  dtype=np.int),
    'Y': np.array([[0, 1],
                   [1, 1],
                   [0, 1],
                   [0, 1]],
                  dtype=np.int),
    'Z': np.array([[1, 1, 0],
                   [0, 1, 0],
                   [0, 1, 1]],
                  dtype=np.int),
}


# construct all possible fixed pieces
PIECES = {}
for name, p in _PIECES.items():
    PIECES[name] = {name: p}
    for op in OPS:
        newp = op(p)
        if all([not equal(e, newp) for e in PIECES[name].values()]):
            PIECES[name][name + "_" + op.__name__] = newp


def place(board, piece, i, j):
    ie = i + piece.shape[0]
    je = j + piece.shape[1]
    if ie > board.shape[0] or je > board.shape[1]:
        return None

    new_board = board.copy()
    new_board[i:ie, j:je] += piece

    if np.any(new_board[i:ie, j:je] > 1):
        return None

    return new_board


def finished(board):
    return np.all(board == 1)


def construct_exact_cover_matrix(board_size, allowed_pieces, occupied_cells=None):
    board = np.zeros(board_size, dtype=np.int)
    if occupied_cells is not None:
        board[tuple(zip(*occupied_cells))] = 1

    num_cells = board_size[0] * board_size[1]
    num_pieces = len(allowed_pieces)

    row_names = []
    rows = []
    for pi, p_n in enumerate(allowed_pieces):
        ps = PIECES[p_n]  # get all possible rotations/reflections of this piece
        for n, p in ps.items():
            for i in range(board_size[0]):
                for j in range(board_size[1]):
                    new_board = place(board, p, i, j)
                    if new_board is not None:
                        row = np.zeros(num_pieces + num_cells)
                        row[pi] = 1
                        ci_s = np.nonzero(new_board.flatten())
                        row[num_pieces + ci_s[0]] = 1
                        rows.append(row)
                        row_names.append((n, (i, j)))

    m = np.array(rows)
    # remove cols we don't care about (i.e., occupied cells)
    keep_cols = np.ones(num_pieces + num_cells, dtype=np.bool)
    keep_cols[num_pieces + np.nonzero(board.flatten())[0]] = False
    m = m[:, keep_cols]
    return m, np.array(row_names, dtype=np.object)


def draw_solution(board_size, solution):
    piece_names = list(PIECES.keys())
    board = np.zeros(board_size, dtype=np.int)
    filled_board = np.sum(np.stack([(piece_names.index(p_n[0])+1) * place(board, PIECES[p_n[0]][p_n], i, j)
                                    for p_n, (i, j) in solution], axis=0), axis=0)
    plt.matshow(filled_board, cmap='Paired')
    plt.show()
    return filled_board


if __name__ == "__main__":
    print("Number of pieces: ", len(PIECES))
    num_fixed_pieces = 0
    for n, ps in PIECES.items():
        print("All possible rotations/reflections for {}:".format(n), sorted(ps.keys()))
        num_fixed_pieces += len(ps)
    print("Number of fixed pieces: ", num_fixed_pieces)
