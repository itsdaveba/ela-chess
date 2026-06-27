from chess import Color


def test_color():
    assert len(Color) == 2
    assert Color.WHITE != Color.BLACK
