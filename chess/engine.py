"""Engine function."""
from itertools import product

import numpy as np


def init_pieces(color):
    from .pieces import Bishop, King, Knight, Pawn, Queen, Rook

    if color == 'white':
        first_row = 1
        second_row = 2
    else:
        first_row = 8
        second_row = 7

    pieces = (
        [Pawn((i, second_row), color) for i in range(1, 9)] +
        [Rook((1, first_row), color), Rook((8, first_row), color)] +
        [Knight((2, first_row), color), Knight((7, first_row), color)] +
        [Bishop((3, first_row), color), Bishop((6, first_row), color)] +
        [Queen((4, first_row), color), King((5, first_row), color)]
    )

    return pieces


def shuffle_pieces(pieces):
    idx_list = list(product(range(1, 9), range(1, 9)))

    idx = np.random.choice(
        np.arange(len(idx_list)), len(pieces), replace=False)

    for piece, i in zip(pieces, idx):
        piece.coords = idx_list[i]

    return pieces
