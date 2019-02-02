import numpy as np
from scipy.ndimage.measurements import label

from katamino.common import finished, PIECES, place, draw_solution

import matplotlib.pyplot as plt


def _check_region_sizes(board):
    regions, num_regions = label(1 - board)
    region_sizes = np.array([np.sum(regions == i) % 5 for i in range(1, num_regions+1)])
    if np.any(region_sizes > 0):
        return False
    return True


def _solve(board, allowed_pieces, subsolns, plot=False):
    soln_k = tuple(board.flatten()) + tuple(sorted(allowed_pieces))
    if soln_k in subsolns:
        return subsolns[soln_k]

    # measure empty region sizes. no solution if any is not a multiple of 5.
    if not _check_region_sizes(board):
        return None

    p_n = allowed_pieces[0]
    ps = PIECES[p_n]  # get all possible rotations/reflections of this piece
    for n, p in ps.items():
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                cur_move = [(n, (i, j))]
                new_board = place(board, p, i, j)
                if new_board is not None:
                    if plot:
                        plt.gca().matshow(2*(new_board - board) + board)
                        plt.pause(0.05)

                    if finished(new_board):
                        return cur_move

                    # find solution of subproblem
                    new_allowed_pieces = allowed_pieces.copy()
                    new_allowed_pieces.remove(p_n)
                    subsoln = _solve(new_board, new_allowed_pieces, subsolns, plot)
                    soln_k = tuple(new_board.flatten()) + tuple(sorted(new_allowed_pieces))
                    subsolns[soln_k] = subsoln
                    if subsoln is not None:
                        return cur_move + subsoln
    return None


def solve(board_size, allowed_pieces, plot=False):
    if plot:
        f = plt.figure()
        f.add_subplot(111)
        plt.ion()
        plt.show()

    board = np.zeros(board_size, dtype=np.int)
    return _solve(board, allowed_pieces, {}, plot)


def main():
    plot = True
    # board_size = (5, 3)
    # allowed_pieces = ['L', 'N', 'V']
    #
    # soln = solve(board_size, allowed_pieces, plot)
    # print(soln)
    # draw_solution(board_size, soln)

    board_size = (5, 12)
    allowed_pieces = list('FILNPTUVWXYZ')

    soln = solve(board_size, allowed_pieces, plot)
    print(soln)
    draw_solution(board_size, soln)


if __name__ == "__main__":
    main()
