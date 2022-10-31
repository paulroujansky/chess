"""Graphical User Interface (GUI) based on PyQt library."""
import sys
from functools import partial
from random import randint
from typing import List

import fire
import numpy as np
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QSizePolicy,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from chess.coords import coords_to_loc, coords_to_np_coords, np_coords_to_coords
from chess.game import Game
from chess.moves import Move
from chess.pieces import Piece
from chess.plot import BACKGROUND, CMAP


class CheckerBoard(QMainWindow):
    def __init__(self, play_against_computer: bool):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle("Chess")
        self.setWindowIcon(QIcon("static/img/chess_pieces/black_knight.png"))

        self.play_against_computer = play_against_computer
        if self.play_against_computer:
            self.computer_color = "white" if randint(0, 1) else "black"
            self.human_color = "white" if self.computer_color == "black" else "black"

        # create chess game
        self.game = Game.create()

        self.selected_piece: Piece = None
        self.valid_moves: List[Move] = None

        # Set the central widget and the general layout

        self.player_label = QLabel()

        top_layout = QVBoxLayout()
        if self.play_against_computer:
            top_layout.addWidget(QLabel(f"You play {self.human_color}!"))
        top_layout.addWidget(self.player_label)

        dummy_label = QLabel()
        dummy_label.setFixedHeight(20)
        self.white_captured_pieces_layout = QHBoxLayout()
        self.white_captured_pieces_layout.addWidget(dummy_label)
        self.white_captured_pieces_layout.setAlignment(Qt.AlignLeft)
        self.white_captured_pieces_layout.addStretch()
        self.black_captured_pieces_layout = QHBoxLayout()
        self.black_captured_pieces_layout.addWidget(dummy_label)
        self.black_captured_pieces_layout.setAlignment(Qt.AlignLeft)
        self.black_captured_pieces_layout.addStretch()

        self.create_checker_board_layout()

        self.history_layout = QVBoxLayout()
        history_title_label = QLabel("<b>History</b>")
        history_title_label.setFixedWidth(200)
        self.history_content_label = QLabel()
        self.history_layout.addWidget(history_title_label)
        self.history_layout.addWidget(self.history_content_label)
        self.history_layout.addStretch(1)

        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(10)
        self.main_layout.addLayout(top_layout, 0, 0)
        self.main_layout.addLayout(self.black_captured_pieces_layout, 1, 0)
        self.main_layout.addLayout(self.checker_board_layout, 2, 0)
        self.main_layout.addLayout(self.history_layout, 2, 1)
        self.main_layout.addLayout(self.white_captured_pieces_layout, 3, 0)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        central_widget = QWidget(self)
        central_widget.setLayout(self.main_layout)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

        self.setCentralWidget(central_widget)

        self.update_layout()

        # self.setFixedSize(self.width(), self.height())
        self.setFixedSize(700, 580)

        self.show()

        if self.play_against_computer:
            QMessageBox.information(
                self,
                "Time to start",
                f"You play {self.human_color}, computer plays {self.computer_color}",
            )

        if self.computer_color == "white":
            self.computer_play()

    def computer_play(self):
        self.game.next_move()
        self.update_layout()

    def select_cell(self, i, j):

        loc = coords_to_loc(np_coords_to_coords(i, j))

        piece = self.game.board.get_piece(loc)

        if piece and piece.color == self.game.turn:
            self.select_piece(piece)

        elif self.selected_piece is not None:

            (ip, jp) = coords_to_np_coords(self.selected_piece.coords)
            if i == ip and j == jp:
                self.selected_piece = None
                self.valid_moves = None

            if self.valid_moves:
                self.select_move(i, j)

        self.update_layout()

        if self.game.is_finished:
            if self.game.draw:
                QMessageBox.information(self, "End of the game", "Draw!")
            else:
                QMessageBox.information(
                    self, "End of the game", f"{self.game.winner} won the game!"
                )
            sys.exit()

    def select_piece(self, piece: Piece):
        self.selected_piece = piece
        self.valid_moves = [
            coords_to_np_coords(move.get_new_coords(piece.coords))
            for move in piece.get_valid_moves(self.game.board)
        ]

    def select_move(self, i, j):
        if (i, j) in self.valid_moves:
            move = self.selected_piece.get_move(
                coords_to_loc(np_coords_to_coords(i, j)), self.game.board
            )
            self.game.next_move(move=(self.selected_piece, move))
            self.selected_piece = None
            self.valid_moves = None

            if self.play_against_computer:
                self.computer_play()

    def create_checker_board_layout(self):
        self.checker_board_layout = QGridLayout()
        self.checker_board_layout.setSpacing(0)
        self.checker_board_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.buttons = np.zeros_like(BACKGROUND, dtype="O")
        n_rows, n_cols = BACKGROUND.shape
        for i in range(n_rows):
            for j in range(n_cols):
                button = QPushButton()
                button.setFixedSize(60, 60)
                button.clicked.connect(partial(self.select_cell, i, j))
                self.buttons[i, j] = button
                self.checker_board_layout.addWidget(button, i, j)

    def update_layout(self):
        self.update_top_layout()
        self.update_history_layout()
        self.update_checker_board_layout()

    def update_top_layout(self):
        self.player_label.setText(f"<b>Player:</b> {self.game.current_player.color}")

    def update_history_layout(self):
        self.history_content_label.setText(self.game.get_history())

    def update_checker_board_layout(self):

        n_rows, n_cols = BACKGROUND.shape
        board_str = self.game.board.to_str_arr()

        for i in range(n_rows):
            for j in range(n_cols):
                bg_color = CMAP[BACKGROUND[i, j]]
                button_stylesheet = f"""
                    QPushButton {{
                        background-color: {bg_color};
                        border: None;
                        font-size: 16px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: yellow;
                    }}
                """

                self.buttons[i, j].setStyleSheet(button_stylesheet)
                if board_str[i, j] and board_str[i, j][0] != " ":
                    self.buttons[i, j].setIcon(QIcon(get_piece_img(board_str[i, j])))
                    self.buttons[i, j].setIconSize(QSize(50, 50))
                else:
                    self.buttons[i, j].setIcon(QIcon())

        if self.selected_piece:
            (ip, jp) = coords_to_np_coords(self.selected_piece.coords)
            self.buttons[ip, jp].setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {CMAP[2]};
                    border: 3px solid #00539c;
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: yellow;
                }}
            """
            )

        if self.valid_moves:
            for (im, jm) in self.valid_moves:
                self.buttons[im, jm].setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: {CMAP[3]};
                        border: None;
                        font-size: 16px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: yellow;
                    }}
                """
                )

        if self.game.white_player.captured_pieces:
            for i in range(
                self.white_captured_pieces_layout.count() - 2,
                len(self.game.white_player.captured_pieces),
            ):
                captured_piece = self.game.white_player.captured_pieces[i]
                print("White captured piece ", i, captured_piece)
                captured_piece_label = QLabel()
                captured_piece_pixmap = QPixmap(get_piece_img(str(captured_piece)))
                captured_piece_label.setPixmap(captured_piece_pixmap.scaled(20, 20))
                self.white_captured_pieces_layout.insertWidget(i, captured_piece_label)

        if self.game.black_player.captured_pieces:
            for i in range(
                self.black_captured_pieces_layout.count() - 2,
                len(self.game.black_player.captured_pieces),
            ):
                captured_piece = self.game.black_player.captured_pieces[i]
                print("Black captured piece ", i, captured_piece)
                captured_piece_label = QLabel()
                captured_piece_pixmap = QPixmap(get_piece_img(str(captured_piece)))
                captured_piece_label.setPixmap(captured_piece_pixmap.scaled(20, 20))
                self.black_captured_pieces_layout.insertWidget(i, captured_piece_label)


def get_piece_img(piece_name):
    piece, color = piece_name[0], piece_name[1]
    if piece == "R":
        piece = "rook"
    elif piece == "N":
        piece = "knight"
    elif piece == "B":
        piece = "bishop"
    elif piece == "Q":
        piece = "queen"
    elif piece == "K":
        piece = "king"
    elif piece == "P":
        piece = "pawn"
    else:
        raise ValueError(f"Invalid piece '{piece}'. Valid pieces are: R, N, B, Q, K, P")

    if color == "b":
        color = "black"
    elif color == "w":
        color = "white"
    else:
        raise ValueError(f"Invalid color '{color}'. Valid colors are: b, w")

    piece_img_path = rf"static/img/chess_pieces/{color}_{piece}.png"

    return piece_img_path


def main(play_against_computer: bool = False):
    # create an instance of QApplication
    app = QApplication(sys.argv)

    # show the chess GUI
    view = CheckerBoard(play_against_computer)

    # execute the chess main loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    fire.Fire(main)
