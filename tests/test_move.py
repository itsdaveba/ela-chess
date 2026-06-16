import pytest

from chess import MoveType, Move, Square


def test_move_type():
    with pytest.raises(ValueError, match="invalid move type flags"):
        MoveType(-1)

    type = MoveType(0)
    assert repr(type) == "MoveType('NORMAL_MOVE')"
    assert type.flags == 0
    assert type.string == "NORMAL_MOVE"
    assert not type & 1

    type = MoveType(13)
    assert repr(type) == "MoveType('PAWN_MOVE|PROMOTION|CAPTURE')"
    assert type.flags == 13
    assert type.string == "PAWN_MOVE|PROMOTION|CAPTURE"
    assert type & 1


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
        Move(0, 0, 0, 0)
    with pytest.raises(ValueError, match="invalid move arguments"):
        Move(Square("e2"), Square("e4"), 0, "x")

    move = Move("e2e4")
    assert move != []
    assert move == "e2e4"
    assert move == Move("e2e4")
    assert repr(move) == "Move.E2E4"
    assert str(move) == "e2e4"
    assert move.source == Square("e2")
    assert move.target == Square("e4")
    assert move.promotion is None
    assert not move.type.flags
    assert move.string == "e2e4"

    move = Move("e7e8Q")
    assert move != []
    assert move == "e7e8Q"
    assert move == Move("e7e8Q")
    assert repr(move) == "Move.E7E8Q"
    assert str(move) == "e7e8q"
    assert move.source == Square("e7")
    assert move.target == Square("e8")
    assert move.promotion == 4
    assert not move.type.flags
    assert move.string == "e7e8q"

    move = Move(Square("e2"), Square("e4"), 3, None)
    assert move != []
    assert move == "e2e4"
    assert move == Move("e2e4")
    assert repr(move) == "Move.E2E4"
    assert str(move) == "e2e4"
    assert move.source == Square("e2")
    assert move.target == Square("e4")
    assert move.promotion is None
    assert move.type.flags == 3
    assert move.string == "e2e4"

    move = Move(Square("e7"), Square("e8"), 5, 4)
    assert move != []
    assert move == "e7e8Q"
    assert move == Move("e7e8Q")
    assert repr(move) == "Move.E7E8Q"
    assert str(move) == "e7e8q"
    assert move.source == Square("e7")
    assert move.target == Square("e8")
    assert move.promotion == 4
    assert move.type.flags == 5
    assert move.string == "e7e8q"
