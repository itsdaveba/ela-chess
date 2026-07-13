import pytest

from chess import Move, MoveType, Square, Piece


def test_move():
    move = Move(Square.E2, Square.E4, MoveType.PAWN_MOVE)
    assert repr(move) == "Move.E2E4"
    assert str(move) == "e2e4"

    move = Move(Square.E7, Square.E8, MoveType.PAWN_MOVE | MoveType.PROMOTION, Piece.QUEEN)
    assert repr(move) == "Move.E7E8Q"
    assert str(move) == "e7e8q"

    assert not move == "e7e8q"
    assert not move == Move.from_string("e2e4")
    assert not move == Move.from_string("e7e4")
    assert not move == Move.from_string("e7e8")
    assert move == Move.from_string("e7e8q")

    with pytest.raises(ValueError, match="invalid move string"):
        Move.from_string("-")

    assert Move.from_string("e2e4").string == "e2e4"
    assert Move.from_string("E2E4").string == "e2e4"
    assert Move.from_string("e7e8q").string == "e7e8q"
    assert Move.from_string("E7E8Q").string == "e7e8q"


def test_type():
    assert len(MoveType) == 7
    assert not MoveType.NONE
