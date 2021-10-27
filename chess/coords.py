"""Coordinates class and functions."""
import numpy as np

from .constants import COL_NAMES, ROW_NAMES


class Coords:

    def __init__(self, coords):
        self.coords = coords

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]


def coords_to_loc(coords):
    (x, y) = coords
    if not 1 <= x <= 8 or not 1 <= y <= 8:
        raise ValueError('`coords` (x, y) must be between 1 and 8')
    return COL_NAMES[x - 1] + ROW_NAMES[::-1][y - 1]


def loc_to_coords(loc):
    col, row = loc[0], loc[1]
    if row not in ROW_NAMES:
        raise ValueError(f'`row` must be in {ROW_NAMES}')
    if col not in COL_NAMES:
        raise ValueError(f'`col` must be in {COL_NAMES}')
    x = int(np.where(np.array(COL_NAMES) == col)[0]) + 1
    y = int(np.where(np.array(ROW_NAMES)[::-1] == row)[0]) + 1
    return (x, y)


def coords_to_np(coords):
    (x, y) = coords
    if not 1 <= x <= 8 or not 1 <= y <= 8:
        raise ValueError('`coords` (x, y) must be between 1 and 8')
    return len(ROW_NAMES) - coords[1], coords[0] - 1


def np_to_coords(row, col):
    (x, y) = (col + 1, len(ROW_NAMES) - row)
    if not 1 <= x <= 8 or not 1 <= y <= 8:
        raise ValueError('`coords` (x, y) must be between 1 and 8')
    return (x, y)
