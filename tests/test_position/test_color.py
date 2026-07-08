import pytest

from chess import Color


def test_color():
    assert len(Color) == 3

    assert Color.WHITE.char == "w"
    assert Color.WHITE.opponent == Color.BLACK

    assert Color.BLACK.char == "b"
    assert Color.BLACK.opponent == Color.WHITE

    assert Color.NONE.char == "-"
    assert Color.NONE.opponent == Color.NONE

    with pytest.raises(ValueError, match="invalid color char"):
        Color.from_char("-")

    assert Color.from_char("w") == Color.WHITE
    assert Color.from_char("b") == Color.BLACK
