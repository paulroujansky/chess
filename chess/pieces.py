"""Piece classes."""
from abc import ABC

from .coords import Coords, coords_to_loc
from .moves import KingSideCastling, Move, QueenSideCastling, is_move_valid
from .utils import staticproperty


class Piece(ABC, Coords):

    MOVES = []

    def __init__(self, coords, color, has_moved=False):
        self.color = color
        self.has_moved = has_moved

        Coords.__init__(self, coords)

    def move(self, new_coords):
        self.coords = new_coords
        self.has_moved = True
        return self.coords

    def __repr__(self):
        return f"{self.SYMBOL}{self.color[0]}"

    @property
    def theoretical_moves(self):
        (x, y) = self.coords
        moves = []
        for move in self.MOVES:
            if 1 <= x + move.x <= 8 and 1 <= y + move.y <= 8:
                moves.append(move)
        return moves

    def get_valid_moves(self, board, conditions=None, check_check=True):
        return [
            move
            for move in self.theoretical_moves
            if is_move_valid(self, move, board, conditions, check_check)
        ]

    def get_move(self, new_loc, board, **kwargs):
        for move in self.get_valid_moves(board, **kwargs):
            if coords_to_loc(move.get_new_coords(self.coords)) == new_loc:
                return move
        raise ValueError(f'No move with new location "{new_loc}"')


class Pawn(Piece):

    SYMBOL = "P"
    VALUE = 1

    def __init__(self, coords, color, has_moved=False):
        Piece.__init__(self, coords, color, has_moved)

    @property
    def MOVES(self):
        way = +1 if self.color == "white" else -1
        moves = [
            Move((0, way), "empty"),
            Move((+1, way), "adversary OR en_passant"),
            Move((-1, way), "adversary OR en_passant"),
        ]
        if not self.has_moved:
            moves += [Move((0, 2 * way), ["empty", "empty_row", "first_move"])]
        return moves


class Ghost(Piece):

    SYMBOL = " "

    def __init__(self, coords, color, has_moved=True):
        Piece.__init__(self, coords, color, has_moved)


class Knight(Piece):

    MOVES = [
        Move((-2, +1), ["empty OR adversary"]),
        Move((-2, -1), ["empty OR adversary"]),
        Move((+2, +1), ["empty OR adversary"]),
        Move((+2, -1), ["empty OR adversary"]),
        Move((+1, -2), ["empty OR adversary"]),
        Move((+1, +2), ["empty OR adversary"]),
        Move((-1, +2), ["empty OR adversary"]),
        Move((-1, -2), ["empty OR adversary"]),
    ]
    SYMBOL = "N"
    VALUE = 3

    def __init__(self, coords, color, has_moved=False):
        Piece.__init__(self, coords, color, has_moved)


class Bishop(Piece):

    SYMBOL = "B"
    VALUE = 3

    def __init__(self, coords, color, has_moved=False):
        Piece.__init__(self, coords, color, has_moved)

    @staticproperty
    def MOVES():
        moves = []
        for i in range(1, 8, 1):
            moves.append(Move((+i, i), ["empty OR adversary", "empty_diag"]))
            moves.append(Move((+i, -i), ["empty OR adversary", "empty_diag"]))
            moves.append(Move((-i, +i), ["empty OR adversary", "empty_diag"]))
            moves.append(Move((-i, -i), ["empty OR adversary", "empty_diag"]))
        return moves


class Rook(Piece):

    SYMBOL = "R"
    VALUE = 6

    def __init__(self, coords, color, has_moved=False):
        Piece.__init__(self, coords, color, has_moved)

    @staticproperty
    def MOVES():
        moves = []
        for i in range(1, 8, 1):
            moves.append(Move((0, +i), ["empty OR adversary", "empty_row"]))
            moves.append(Move((0, -i), ["empty OR adversary", "empty_row"]))
            moves.append(Move((+i, 0), ["empty OR adversary", "empty_row"]))
            moves.append(Move((-i, 0), ["empty OR adversary", "empty_row"]))
        return moves


class Queen(Piece):

    SYMBOL = "Q"
    VALUE = 9

    def __init__(self, coords, color, has_moved=False):
        Piece.__init__(self, coords, color, has_moved)

    @staticproperty
    def MOVES():
        moves = []
        for i in range(1, 8, 1):
            # diagonals
            moves.append(Move((+i, i), ["empty OR adversary", "empty_diag"]))
            moves.append(Move((+i, -i), ["empty OR adversary", "empty_diag"]))
            moves.append(Move((-i, +i), ["empty OR adversary", "empty_diag"]))
            moves.append(Move((-i, -i), ["empty OR adversary", "empty_diag"]))
            # rows
            moves.append(Move((0, +i), ["empty OR adversary", "empty_row"]))
            moves.append(Move((0, -i), ["empty OR adversary", "empty_row"]))
            moves.append(Move((+i, 0), ["empty OR adversary", "empty_row"]))
            moves.append(Move((-i, 0), ["empty OR adversary", "empty_row"]))
        return moves


class King(Piece):

    SYMBOL = "K"
    MOVES = [
        Move((0, +1), "empty OR adversary"),
        Move((0, -1), "empty OR adversary"),
        Move((+1, 0), "empty OR adversary"),
        Move((+1, +1), "empty OR adversary"),
        Move((+1, -1), "empty OR adversary"),
        Move((-1, 0), "empty OR adversary"),
        Move((-1, +1), "empty OR adversary"),
        Move((-1, -1), "empty OR adversary"),
        QueenSideCastling(),
        KingSideCastling(),
    ]

    def __init__(self, coords, color, has_moved=False):
        Piece.__init__(self, coords, color, has_moved)
