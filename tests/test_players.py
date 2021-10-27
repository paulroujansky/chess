"""Test Player class."""
import pytest
from chess.players import Player


@pytest.mark.parametrize('color', ('white', 'black'))
def test_player_creation(color):
    player = Player(color)
