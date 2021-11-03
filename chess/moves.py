"""Move functions."""
import numpy as np

from .coords import Coords


class Move(Coords):
    def __init__(self, coords, conditions=None):
        if not isinstance(conditions, list):
            conditions = [conditions]
        self.conditions = conditions

        Coords.__init__(self, coords)

    def __repr__(self):
        (x, y) = self.coords
        sign_x = "+" if x >= 0 else ""
        sign_y = "+" if y >= 0 else ""
        return f"({sign_x}{x}, {sign_y}{y})"

    def get_new_coords(self, init_coords):
        return (init_coords[0] + self.x, init_coords[1] + self.y)


class Castling(Move):
    def __init__(self, coords, symbol, rook_col, rook_move):
        Move.__init__(self, coords)
        self.symbol = symbol
        self.rook_col = rook_col
        self.rook_move = rook_move


class QueenSideCastling(Castling):
    def __init__(self):
        Castling.__init__(
            self, coords=(-2, 0), symbol="0-0-0", rook_col=1, rook_move=Move((+3, 0))
        )


class KingSideCastling(Castling):
    def __init__(self):
        Castling.__init__(
            self, coords=(+2, 0), symbol="0-0", rook_col=8, rook_move=Move((-2, 0))
        )


def is_move_valid(piece, move, board, conditions=None, check_check=True):
    from .pieces import Rook

    init_coords = piece.coords
    new_coords = move.get_new_coords(init_coords)

    target_cell = board.get_piece(new_coords)

    sx = np.sign(move.x)
    sy = np.sign(move.y)

    if conditions is not None:  # useless ?  TODO
        if not any([cond in conditions for cond in move.conditions]):
            return False

    for condition in move.conditions:
        if condition == "first_move":
            if piece.has_moved:
                return False
        if condition == "empty":
            if target_cell is not None:
                return False
        elif condition == "adversary OR en_passant":
            if target_cell is None or (
                target_cell is not None and target_cell.color == piece.color
            ):
                # implement "en-passant" check
                return False
        elif condition == "empty OR adversary":
            if target_cell is not None and target_cell.color == piece.color:
                return False
        elif condition == "empty_diag":
            for x, y in zip(range(sx, move.x, sx), range(sy, move.y, sy)):
                if board.get_piece((piece.x + x, piece.y + y)) is not None:
                    return False
        elif condition == "empty_row":
            if move.x == 0:
                for y in range(sy, move.y, sy):
                    if board.get_piece((piece.x, piece.y + y)) is not None:
                        return False
            elif move.y == 0:
                for x in range(sx, move.x, sx):
                    if board.get_piece((piece.x + x, piece.y)) is not None:
                        return False

    # check condition if current move is castling
    if isinstance(move, Castling):
        # check that King is not in check
        if board.get_player(piece.color).in_check:
            return False
        # check that King has not moved yet
        if piece.has_moved:
            return False
        # check that row is empty
        for x in range(sx, move.rook_col - piece.x, sx):
            if board.get_piece((piece.x + x, piece.y)) is not None:
                return False
        # check that target Rook has not moved neither
        castling_rook = board.get_piece(
            (1 if piece.color == "white" else 8, move.rook_col)
        )
        if castling_rook is None or not isinstance(castling_rook, Rook):
            return False
        else:
            if castling_rook.has_moved:
                return False

    # every moves have to lead to a non-check position for the current player
    if check_check:
        # simulate move
        current_player = board.get_player(piece.color)
        other_player = board.get_player("white" if piece.color == "black" else "black")

        if target_cell is not None and target_cell.color != piece.color:
            # take adversary piece
            captured_piece = True
            current_player.captured_pieces.append(target_cell)
            other_player.pieces.remove(target_cell)
            board.del_piece(target_cell)
        else:
            captured_piece = False

        board.del_piece(piece)
        piece.coords = new_coords
        board.set_piece(piece)

        # check if move lead to an in-check position for the current player
        in_check, in_check_pieces = is_in_check(current_player, other_player, board)
        # revert back simulated move
        board.del_piece(piece)
        piece.coords = init_coords
        board.set_piece(piece)
        if captured_piece:
            current_player.captured_pieces.remove(target_cell)
            other_player.pieces.append(target_cell)
            board.set_piece(target_cell)

        if in_check:
            return False

    return True


def is_in_check(current_player, other_player, board):
    current_king = current_player.get_king()[1]
    valid_moves = other_player.get_valid_moves(board, check_check=False)
    in_check_pieces = []
    for piece, moves in valid_moves:
        for move in moves:
            if move.get_new_coords(piece.coords) == current_king.coords:
                in_check_pieces.append(piece)
                # print(piece.SYMBOL, piece.coords, current_king.coords)
    in_check = len(in_check_pieces) > 0
    return in_check, in_check_pieces
