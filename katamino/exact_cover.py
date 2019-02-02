from typing import Optional

import numpy as np

from katamino.common import construct_exact_cover_matrix, draw_solution


def _find_exact_cover(m: np.ndarray, row_ids: np.ndarray):
    if m.size == 0:  # successful
        return []

    col_sums = np.sum(m, axis=0)
    if np.any(col_sums == 0):  # failed to find a solution
        return None

    # pick column with fewest number of 1s
    c = np.argmin(col_sums)

    # choose a row such that m[r, c] = 1
    rs = np.nonzero(m[:, c])[0]
    for r in rs:
        keep_col = np.ones(m.shape[1], dtype=np.bool)
        keep_row = np.ones(m.shape[0], dtype=np.bool)

        # include r in the partial solution
        selected_row_id = row_ids[r]

        # delete columns m[r, j] = 1
        js = np.nonzero(m[r, :])[0]
        keep_col[js] = False
        for j in js:
            # delete rows m[k, j] = 1
            ks = np.nonzero(m[:, j])[0]
            keep_row[ks] = False

        keep_row[r] = True  # don't delete the row we selected

        # find solution for reduced matrix
        reduced_m = m[keep_row, :][:, keep_col]
        subsoln = _find_exact_cover(reduced_m, row_ids[keep_row])
        if subsoln is not None:
            return [selected_row_id] + subsoln

    return None


def find_exact_cover(m: np.ndarray, row_names: Optional[np.ndarray] = None):
    """
    Find the set of rows that cover all the columns.

    This is a pretty faithful implementation of the Algorithm X in Knuth's dancing links paper (implemented with numpy
    arrays instead of the doubly linked circular list structure he uses).

    :param m: Binary matrix.
    :param row_names: Names of rows. If not provided, uses row number.
    :return: A list of the rows that cover all the columns. If no such set exists, returns an empty list.
    """
    assert m.dtype == np.bool, "Input matrix must be binary (dtype=bool)."

    if row_names is None:
        row_names = np.arange(m.shape[0])
    soln = _find_exact_cover(m, row_names)
    if soln is None:
        soln = []
    return soln


def solve_katamino(board_size, allowed_pieces, occupied_cells=None):
    print("Problem with board size {} and pieces {}:".format(board_size, allowed_pieces))
    m, row_names = construct_exact_cover_matrix(board_size, allowed_pieces, occupied_cells)
    print("Exact cover matrix has shape:", m.shape)

    soln = find_exact_cover(m.astype(np.bool), row_names)
    print("Found solution:")
    print(soln)
    draw_solution(board_size, soln)
    print()


def main():
    solve_katamino((5, 3), 'LNV')

    solve_katamino((6, 10), 'FILNPTUVWXYZ')
    solve_katamino((5, 12), 'FILNPTUVWXYZ')
    solve_katamino((4, 15), 'FILNPTUVWXYZ')
    solve_katamino((3, 20), 'FILNPTUVWXYZ')

    solve_katamino((8, 8), 'FILNPTUVWXYZ', occupied_cells=((3, 3), (3, 4), (4, 3), (4, 4)))


if __name__ == "__main__":
    main()
