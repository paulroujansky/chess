from chess.coords import Coords


def test_coords():

    coords = Coords((1, 1))
    assert coords.x == 1 and coords.y == 1
    assert coords.loc == "a1"
    assert coords.np_coords == (7, 0)

    assert Coords.from_loc("a1") == Coords.from_np_coords(7, 0) == Coords((1, 1))

    coords = Coords((3, 4))
    assert coords.x == 3 and coords.y == 4
    assert coords.loc == "c4"
    assert coords.np_coords == (4, 2)

    assert Coords.from_loc("c4") == Coords.from_np_coords(4, 2) == Coords((3, 4))
