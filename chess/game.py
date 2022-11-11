"""Game class."""
import numpy as np

from .board import Board
from .coords import coords_to_loc
from .engine import init_pieces
from .moves import Move, Castling, is_in_check
from .pieces import Bishop, Ghost, Knight, Pawn, Queen, Rook
from .players import Player


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

        self.history = []
        self.move_number = 1
        self.turn = "white"
        self.is_finished = False
        self.winner = None
        self.draw = False

        self.automatic_promotion = True
        self.default_promotion = "Q"

    @classmethod
    def create(cls):
        player1 = Player("white")
        player2 = Player("black")
        return cls(player1, player2)

    def reset(self):
        # reset pieces
        self.player1.pieces = init_pieces(self.player1.color)
        self.player2.pieces = init_pieces(self.player2.color)

        # flush captured pieces for both players
        self.player1.captured_pieces = []
        self.player2.captured_pieces = []

        # reset history and set turn to "white"
        self.history = []
        self.turn = "white"

    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"
        if self.turn == "white":
            self.move_number += 1
        print(f"Switch to {self.turn}")

    def next_move(self, move: Move = None, verbose: bool = True):
        # remove current player's ghosts
        for piece in self.current_player.pieces:
            if isinstance(piece, Ghost):
                self.current_player.pieces.remove(piece)

        # get move
        if move is None:
            move = self.current_player.get_move(self.board)
        if move is None:
            if self.current_player.in_check:
                self.winner = (
                    "white" if self.current_player.color == "black" else "black"
                )
                print(f"{self.winner} player won the game!")
            else:
                self.draw = True
                print("Draw")
            self.is_finished = True
            return

        (piece, move) = move
        init_coords = piece.coords
        new_coords = move.get_new_coords(piece.coords)

        # check if adversary piece is captured
        captured_piece = False
        target_cell = self.board.get_piece(new_coords)
        if target_cell is not None and (target_cell.color != self.current_player.color):
            # take adversary piece
            captured_piece = True
            if isinstance(target_cell, Ghost):
                self.other_player.pieces.remove(target_cell)
                target_cell = self.board.get_piece((piece.x + move.x, piece.y))
            self.current_player.captured_pieces.append(target_cell)
            self.other_player.pieces.remove(target_cell)
            if verbose:
                print(
                    f"{self.current_player} captured "
                    f"{self.other_player} {target_cell.SYMBOL}"
                )

        # move piece
        self.current_player.move(piece, move)
        # move Rook if move is Castling
        if isinstance(move, Castling):
            # move pieces
            castling_rook = self.board.get_piece(
                (move.rook_col, 1 if piece.color == "white" else 8)
            )
            self.current_player.move(castling_rook, move.rook_move)

        # mark intermediary cell as "Ghost" if Pawn is moving two cells
        if isinstance(piece, Pawn) and np.abs(move.y) == 2:
            ghost = Ghost(
                (piece.x, piece.y - np.sign(move.y)), color=self.current_player.color
            )
            self.current_player.pieces.append(ghost)

        if verbose:
            print(
                f"[{self.move_number}] {self.current_player} moves "
                f"{piece.SYMBOL} from {coords_to_loc(init_coords)} "
                f"to {coords_to_loc(new_coords)}"
            )

        # check if piece is pawn and can be changed to another piece
        promoted_piece = False
        if isinstance(piece, Pawn):
            # change Pawn to chosen piece
            if (self.current_player.color == "white" and piece.y == 8) or (
                self.current_player.color == "black" and piece.y == 1
            ):
                promoted_piece = True
                if self.automatic_promotion:
                    promotion = self.default_promotion
                else:
                    promotion = input('Change to: "Q", "R", "B", "N".')
                if promotion == "Q":
                    piece = Queen(
                        piece.coords, color=self.current_player.color, has_moved=True
                    )
                elif promotion == "R":
                    piece = Rook(
                        piece.coords, color=self.current_player.color, has_moved=True
                    )
                elif promotion == "B":
                    piece = Bishop(
                        piece.coords, color=self.current_player.color, has_moved=True
                    )
                elif promotion == "N":
                    piece = Knight(
                        piece.coords, color=self.current_player.color, has_moved=True
                    )
                i = self.current_player.get_piece(piece.coords)[0]
                self.current_player.pieces[i] = piece
                if verbose:
                    print(f"* Pawn promoted to {piece.SYMBOL}")

        # check if move lead to an "in check" position against the other player
        in_check, in_check_pieces = is_in_check(
            self.other_player, self.current_player, self.board
        )
        if in_check:
            self.other_player.in_check = True
            if verbose:
                print(f"{self.other_player} is in check by {in_check_pieces}")
        else:
            self.other_player.in_check = False

        # update history
        movestr = ""
        if promoted_piece:
            # = promotion
            movestr = f"{coords_to_loc(piece.coords)}+{piece.SYMBOL}"
        elif captured_piece:
            if isinstance(piece, Pawn):
                movestr += (
                    f"{coords_to_loc(init_coords)}x" f"{coords_to_loc(piece.coords)}"
                )
            else:
                movestr += f"{piece.SYMBOL}x{coords_to_loc(piece.coords)}"
        elif isinstance(move, Castling):
            movestr = move.symbol
        else:
            if isinstance(piece, Pawn):
                movestr += f"{coords_to_loc(piece.coords)}"
            else:
                movestr += f"{piece.SYMBOL}{coords_to_loc(piece.coords)}"
        # Rook
        self.history.append((self.move_number, self.turn, movestr))

        # switch turn
        self.switch_turn()

        return captured_piece

    @property
    def board(self):
        return Board([self.player1, self.player2])

    def get_history(self, delimiter: str = "\n"):
        prev_move_number = 1
        msgs = []
        msg = ""
        for (move_number, turn, move) in self.history:
            if move_number != prev_move_number:
                msgs.append(msg)
                msg = ""
            prev_move_number = move_number
            if turn == "white":
                msg = f"{move_number}. {move}"
            else:
                msg += f" {move}"
        if msg != "":
            msgs.append(msg)
        return delimiter.join(msgs)

    def show_history(self, delimiter: str = "\n"):
        print(self.get_history(delimiter))

    def get_player(self, color: str):
        if color not in ["white", "black"]:
            raise ValueError('`color` must be either "white" or "black".')
        return self.player1 if self.player1.color == color else self.player2

    @property
    def white_player(self):
        return self.get_player("white")

    @property
    def black_player(self):
        return self.get_player("black")

    @property
    def current_player(self):
        return self.get_player(self.turn)

    @property
    def other_player(self):
        other_color = "black" if self.turn == "white" else "white"
        return self.get_player(other_color)

    def print_board(self):
        print(self.board)

    def show_board(self, loc: str = None, show_moves: bool = False, **kwargs):
        self.board.show(loc=loc, show_moves=show_moves, **kwargs)
