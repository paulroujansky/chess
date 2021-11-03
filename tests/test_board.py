"""Test Board class."""
from chess.board import Board
from chess.players import Player


def test_board_creation():
    # create players
    player1 = Player("white")
    player2 = Player("black")
    Board.from_players([player1, player2])
