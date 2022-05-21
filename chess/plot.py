"""Plotting functions."""
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from .constants import COL_NAMES, ROW_NAMES
from .coords import coords_to_np

CMAP = ["#faedcd", "#d4a373", "#94cdff", "#ebffb0"]


def make_background():
    background = np.zeros((8, 8), dtype=int)
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                background[i, j] = 1
    return background


BACKGROUND = make_background()


def show_board(board, cmap=CMAP, piece=None, moves=None):

    background = BACKGROUND.copy()

    if piece is not None:
        piece_idx = coords_to_np(piece.coords)
        background[piece_idx] = 2

        if moves is not None and len(moves) > 0:
            moves_idx = [
                coords_to_np(move.get_new_coords(piece.coords)) for move in moves
            ]
            for move_idx in moves_idx:
                background[move_idx] = 3

    board = board.copy().astype(str)
    board[board == "None"] = ""

    center = None if cmap is None else (len(cmap) - 1) / 2

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    sns.heatmap(
        background,
        cmap=cmap,
        center=center,
        # annot=board, annot_kws={'fontsize': 14, 'fontweight': 'bold'},  # noqa: E501
        fmt="s",
        square=True,
        cbar=False,
        linewidths=1,
        linecolor="black",
        ax=ax,
    )
    for i in range(8):
        for j in range(8):
            if board[i, j]:
                sym, col = board[i, j][0], board[i, j][1]
                col = "white" if col == "w" else "black"
                path_effects = (
                    [pe.withStroke(linewidth=3, foreground="black")]
                    if col == "white"
                    else []
                )
                if sym != " ":
                    ax.text(
                        j + 0.5,
                        i + 0.5,
                        sym,
                        size=16,
                        ha="center",
                        va="center",
                        fontweight="bold",
                        color=col,
                        path_effects=path_effects,
                    )
    ax.set_xticklabels(COL_NAMES, fontsize=12)
    ax.set_yticklabels(ROW_NAMES, fontsize=12)
    ax.xaxis.set_ticks_position("none")
    ax.yaxis.set_ticks_position("none")
    plt.show()
