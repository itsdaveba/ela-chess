import pytest

from chess import History, Move, Piece, Castling, Square, Counter


def test_history():
    history = History()

    move = Move.from_string("e2e4")
    irrev = Piece.NONE, Castling.NONE, Square.NONE, Counter(0)
    history.append(move, irrev)
    assert repr(history) == "History([Move.E2E4])"
    assert len(history) == 1

    move, irrev = history.pop()
    assert len(history) == 0

    with pytest.raises(IndexError, match="pop from empty list"):
        history.pop()
