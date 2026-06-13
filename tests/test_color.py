import pytest

from chess import Color


def test_color():
    with pytest.raises(ValueError, match="invalid color char"):
        Color('x')

    color = Color(True)
    assert color != 1
    assert color == Color(True)
    assert repr(color) == "Color.WHITE"
    assert color.white
    assert color.char == 'w'
    assert color.name == "WHITE"

    color = Color('b')
    assert color != 0
    assert color == Color('b')
    assert repr(color) == "Color.BLACK"
    assert not color.white
    assert color.char == 'b'
    assert color.name == "BLACK"
