import pytest

from chess import Color


def test_color():
    assert len(Color) == 2

    assert Color.WHITE.char == "w"
    assert Color.BLACK.char == "b"

    with pytest.raises(ValueError, match="invalid color char"):
        Color.from_char("-")

    assert Color.from_char("w") == Color.WHITE
    assert Color.from_char("b") == Color.BLACK
