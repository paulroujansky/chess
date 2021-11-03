"""Test engine functions."""
import pytest
from chess.engine import init_pieces


@pytest.mark.parametrize("color", ("white", "black"))
def test_piece_initialization(color):
    init_pieces(color)
