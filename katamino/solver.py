import numpy as np

from katamino.common import finished, PIECES, place


def _solve(board, allowed_pieces):
    for p_n in allowed_pieces:
        ps = PIECES[p_n]  # get all possible rotations/reflections of this piece
        for n, p in ps.items():
            for i in range(board.shape[0]):
                for j in range(board.shape[1]):
                    cur_move = [(n, (i, j))]
                    new_board = place(board, p, i, j)
                    if new_board is not None:
                        if finished(new_board):
                            return cur_move

                        # find solution of subproblem
                        new_allowed_pieces = allowed_pieces.copy()
                        new_allowed_pieces.remove(p_n)
                        subsoln = _solve(new_board, new_allowed_pieces)
                        if subsoln is not None:
                            return cur_move + subsoln
    return None


def solve(board_size, allowed_pieces):
    board = np.zeros(board_size, dtype=np.int)
    return _solve(board, allowed_pieces)


def main():
    board_size = (5, 3)
    # board_size = (5, 12)
    allowed_pieces = ['L', 'N', 'V']
    # allowed_pieces = list('FILNPTUVWXYZ')

    soln = solve(board_size, allowed_pieces)
    print(soln)


if __name__ == "__main__":
    main()
