import pytest

from chess import Square


def test_square():
    assert len(Square) == 65

    assert Square.A1.string == "a1"
    assert Square.H8.string == "h8"
    assert Square.NONE.string == "-"

    with pytest.raises(ValueError, match="invalid square string"):
        assert Square.from_string("X")
    with pytest.raises(ValueError, match="invalid square string"):
        assert Square.from_string("X1")

    assert Square.from_string("a1") == Square.A1
    assert Square.from_string("h8") == Square.H8
    assert Square.from_string("A1") == Square.A1
    assert Square.from_string("H8") == Square.H8
    assert Square.from_string("-") == Square.NONE
