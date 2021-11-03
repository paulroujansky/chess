"""Player class."""
import numpy as np

from .engine import init_pieces
from .pieces import King


class Player:
    def __init__(self, color, pieces=None):

        if color not in ["white", "black"]:
            raise ValueError('`color` must be either "white" or "black".')
        self.color = color
        self.in_check = False

        if pieces is None:
            pieces = init_pieces(color)
        self.pieces = pieces

        self.captured_pieces = []

    def __repr__(self):
        return f'Player("{self.color}")'

    def get_valid_moves(self, board, conditions=None, check_check=True):
        valid_moves = []
        for piece in self.pieces:
            moves = piece.get_valid_moves(board, conditions, check_check)
            if len(moves):
                valid_moves.append((piece, moves))
        return valid_moves

    def get_move(self, board, conditions=None, check_check=True, strategy="random"):
        # get all valid moves
        valid_moves = self.get_valid_moves(board, conditions, check_check=check_check)
        if len(valid_moves) == 0:
            return None

        # valid_moves_ = []
        # for (piece, moves) in valid_moves:
        #     if any(isinstance(move, Castling) for move in moves):
        #         valid_moves_.append((piece, [move for move in moves if isinstance(move, Castling)]))  # noqa: E501
        # if len(valid_moves_) > 0:
        #     valid_moves = valid_moves_

        if strategy == "random":
            # randomly select piece
            idx = np.random.choice(len(valid_moves), 1)[0]
            (piece, moves) = valid_moves[idx]
            # randomly select move
            idx = np.random.choice(len(moves), 1)[0]
            move = moves[idx]

        return (piece, move)

    def get_piece(self, coords):
        for i, piece in enumerate(self.pieces):
            if piece.coords == coords:
                return (i, piece)

    def get_king(self):
        for i, piece in enumerate(self.pieces):
            if isinstance(piece, King):
                return (i, piece)

    def move(self, piece, move):
        return piece.move(move.get_new_coords(piece.coords))
