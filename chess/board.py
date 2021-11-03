"""Board class and functions."""
from copy import deepcopy

import numpy as np

from .constants import COL_NAMES, ROW_NAMES
from .coords import coords_to_loc, coords_to_np, loc_to_coords
from .plot import show_board


def create_board():
    board = np.zeros((8, 8), dtype=object)
    board.fill(None)
    return board


def board_to_string(board):
    board = board.copy().astype(str)
    board[board == "None"] = ""

    strng = ""

    for i, (row, row_name) in enumerate(zip(board, ROW_NAMES)):

        row_str = "| " + " | ".join([f" {cell:1s} " for cell in row]) + " |"
        row_name_str = f"{row_name} "
        strng += " " * len(row_name_str) + "+" + "-" * (len(row_str) - 2) + "+"
        strng += "\n"
        strng += row_name_str + row_str
        strng += "\n"

    col_names_str = (
        "  " + "   ".join([f" {col_name:1s} " for col_name in COL_NAMES]) + "  "
    )
    strng += " " * len(row_name_str) + "+" + "-" * (len(col_names_str) - 2) + "+"
    strng += "\n"
    strng += " " * len(row_name_str) + col_names_str

    return strng


def display_board(board):
    print(board_to_string(board))


class Board:
    def __init__(self, players=None):
        self.chessboard = create_board()
        if players:
            self.add_players(players)

    def copy(self):
        return deepcopy(self)

    @classmethod
    def from_players(cls, players):
        return Board(players)

    def add_players(self, players):
        self.players = players
        for player in players:
            for piece in player.pieces:
                self.set_piece(piece)

    def get_player(self, color):
        for player in self.players:
            if player.color == color:
                return player

    def to_str_arr(self):
        chessboard = self.chessboard.copy()
        chessboard[chessboard == None] = ""  # noqa: E711
        return chessboard.astype(str)

    def __str__(self):
        return board_to_string(self.to_str_arr())

    def show(self, loc=None, show_moves=False, **kwargs):
        moves = None
        piece = None
        if loc is not None:
            piece = self.get_piece(loc)
            if piece is not None and show_moves:
                moves = piece.get_valid_moves(self)
        show_board(self.to_str_arr(), piece=piece, moves=moves, **kwargs)

    def get_piece(self, loc):
        if isinstance(loc, str):
            coords = loc_to_coords(loc)
        elif isinstance(loc, (tuple, list)):
            coords = tuple(loc)
        else:
            raise ValueError("`loc` must be either a str or a 2-tuple")
        return self.chessboard[coords_to_np(coords)]

    def set_piece(self, piece):
        self.chessboard[coords_to_np(piece.coords)] = piece

    def del_piece(self, piece):
        self.chessboard[coords_to_np(piece.coords)] = None

    def get_moves(self, loc):
        piece = self.get_piece(loc)
        if piece is None:
            return []
        else:
            return [
                coords_to_loc(move.get_new_coords(piece.coords))
                for move in piece.get_valid_moves()
            ]
