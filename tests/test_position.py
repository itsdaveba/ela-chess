import pytest

from chess import Position, Color


def test_fen():
    with pytest.raises(ValueError):
        Position(".")

    position = Position()
    assert repr(position) == "Position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')"
    assert position.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert position.side == Color('w')
    assert position.castling.rights == 15
    assert position.epsquare is None
    assert position.halfmove == 0
    assert position.fullmove == 1

    position = Position("r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b Kq a3 5 8")
    assert repr(position) == "Position('r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b Kq a3 5 8')"
    assert position.fen == "r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b Kq a3 5 8"
    assert position.side == Color('b')
    assert position.castling.rights == 9
    assert position.epsquare == "a3"
    assert position.halfmove == 5
    assert position.fullmove == 8

    position.reset()
    assert position.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
