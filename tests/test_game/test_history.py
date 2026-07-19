import pytest

from chess import History, Move, Piece, Castling, Square, Counter


def test_history():
    history = History()

    irrev = Piece.NONE, Castling.NONE, Square.NONE, Counter(0)

    move = Move.from_string("e2e4")
    history.append(move, irrev)
    assert repr(history) == "History([Move.E2E4])"
    assert len(history) == 1
    move = Move.from_string("e7e5")
    history.append(move, irrev)
    assert repr(history) == "History([Move.E2E4, Move.E7E5])"
    assert len(history) == 2
    assert history.movetext() == "e2e4 e7e5"

    move, irrev = history.pop()
    assert len(history) == 1
    move, irrev = history.pop()
    assert len(history) == 0

    with pytest.raises(IndexError, match="pop from empty list"):
        history.pop()
