import pytest

from chess import MoveType, Move, Square


def test_move_type():
    with pytest.raises(ValueError, match="invalid move type flags"):
        MoveType(-1)

    type = MoveType(0)
    assert repr(type) == "MoveType('NORMAL_MOVE')"
    assert type.flags == 0
    assert type.str == "NORMAL_MOVE"

    type = MoveType(13)
    assert repr(type) == "MoveType('PAWN_MOVE|PROMOTION|CAPTURE')"
    assert type.flags == 13
    assert type.str == "PAWN_MOVE|PROMOTION|CAPTURE"


def test_move():
    with pytest.raises(ValueError, match="invalid move arguments"):
        Move()
    with pytest.raises(ValueError, match="invalid move arguments"):
        Move(0)
    with pytest.raises(ValueError, match="invalid move string"):
        Move("x")
    with pytest.raises(ValueError, match="invalid move arguments"):
        Move(0, 0)
    with pytest.raises(ValueError, match="invalid move arguments"):
        Move(0, 0, 0)
    with pytest.raises(ValueError, match="invalid move arguments"):
        Move(Square("e2"), Square("e4"), "x")

    move = Move("e2e4")
    assert repr(move) == "Move.E2E4"
    assert move.source == Square("e2")
    assert move.target == Square("e4")
    assert move.promotion is None
    assert move.str == "e2e4"

    move = Move("e7e8Q")
    assert repr(move) == "Move.E7E8Q"
    assert move.source == Square("e7")
    assert move.target == Square("e8")
    assert move.promotion == 4
    assert move.str == "e7e8q"

    move = Move(Square("e2"), Square("e4"), None)
    assert repr(move) == "Move.E2E4"
    assert move.source == Square("e2")
    assert move.target == Square("e4")
    assert move.promotion is None
    assert move.str == "e2e4"

    move = Move(Square("e7"), Square("e8"), 4)
    assert repr(move) == "Move.E7E8Q"
    assert move.source == Square("e7")
    assert move.target == Square("e8")
    assert move.promotion == 4
    assert move.str == "e7e8q"
