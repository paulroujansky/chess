"""Coordinates class and functions."""
from __future__ import annotations

import numpy as np

from .constants import COL_NAMES, ROW_NAMES


class Coords:
    def __init__(self, coords: tuple):
        self.coords = coords

    def __eq__(self, other: Coords):
        return self.coords == other.coords

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def loc(self):
        return coords_to_loc(self.coords)

    @classmethod
    def from_loc(cls, loc):
        return cls(loc_to_coords(loc))

    @property
    def np_coords(self):
        return coords_to_np_coords(self.coords)

    @classmethod
    def from_np_coords(cls, row, col):
        return cls(np_coords_to_coords(row, col))


def coords_to_loc(coords: tuple) -> str:
    (x, y) = coords
    if not 1 <= x <= 8 or not 1 <= y <= 8:
        raise ValueError("`coords` (x, y) must be between 1 and 8")
    return COL_NAMES[x - 1] + ROW_NAMES[::-1][y - 1]


def loc_to_coords(loc: str) -> tuple:
    col, row = loc[0], loc[1]
    if row not in ROW_NAMES:
        raise ValueError(f"`row` must be in {ROW_NAMES}")
    if col not in COL_NAMES:
        raise ValueError(f"`col` must be in {COL_NAMES}")
    x = int(np.where(np.array(COL_NAMES) == col)[0]) + 1
    y = int(np.where(np.array(ROW_NAMES)[::-1] == row)[0]) + 1
    return (x, y)


def coords_to_np_coords(coords: tuple) -> tuple:
    (x, y) = coords
    if not 1 <= x <= 8 or not 1 <= y <= 8:
        raise ValueError("`coords` (x, y) must be between 1 and 8")
    return len(ROW_NAMES) - coords[1], coords[0] - 1


def np_coords_to_coords(row: int, col: int) -> tuple:
    (x, y) = (col + 1, len(ROW_NAMES) - row)
    if not 1 <= x <= 8 or not 1 <= y <= 8:
        raise ValueError("`coords` (x, y) must be between 1 and 8")
    return (x, y)
