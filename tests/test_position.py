import pytest

from chess import Position, Move


def test_fen():
    with pytest.raises(ValueError, match="invalid fen"):
        Position(".")
    with pytest.raises(ValueError, match="invalid fen side to move"):
        Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1")
    with pytest.raises(ValueError, match="invalid fen halfmove"):
        Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - x 1")
    with pytest.raises(ValueError, match="invalid fen fullmove"):
        Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0")

    position = Position()
    assert repr(position) == "Position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')"
    assert position.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert position.white
    assert position.castling.rights == 15
    assert position.epsquare is None
    assert position.halfmove == 0
    assert position.fullmove == 1

    position = Position("r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b Kq a3 5 8")
    assert repr(position) == "Position('r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b Kq a3 5 8')"
    assert position.fen == "r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b Kq a3 5 8"
    assert not position.white
    assert position.castling.rights == 9
    assert position.epsquare == "a3"
    assert position.halfmove == 5
    assert position.fullmove == 8

    position.reset()
    assert position.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert str(position) == """\
White to move
+-----------------+
| r n b q k b n r | 8
| p p p p p p p p | 7
| . . . . . . . . | 6
| . . . . . . . . | 5
| . . . . . . . . | 4
| . . . . . . . . | 3
| P P P P P P P P | 2
| R N B Q K B N R | 1
+-----------------+
  a b c d e f g h"""


def test_make_undo():
    position = Position()

    # normal move
    assert position.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert position.make_move("e2e4")
    assert position.fen == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    assert position.make_move(Move("c7c5"))
    assert position.fen == "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
    assert position.make_move("g1f3")
    assert position.fen == "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"

    # illegal move
    assert not position.make_move("e2e4")

    # king in check
    assert position.make_move("d8a5")
    assert position.fen == "rnb1kbnr/pp1ppppp/8/q1p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
    assert not position.make_move("d2d4")

    # undo move
    position.undo_move()
    assert position.fen == "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
    position.undo_move()
    assert position.fen == "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
    position.undo_move()
    assert position.fen == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    position.undo_move()
    assert position.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    with pytest.raises(ValueError, match="no previous moves"):
        position.undo_move()

    # castling rights update
    position.fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
    assert position.make_move("a1d1")
    assert position.fen == "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/3RK2R b Kkq - 1 1"
    assert position.make_move("e8d8")
    assert position.fen == "r2k3r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/3RK2R w K - 2 2"
    position.undo_move()
    assert position.make_move("h3g2")
    assert position.fen == "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q2/PPPBBPpP/3RK2R w Kkq - 0 2"
    assert not position.make_move("e1g1")
    assert position.make_move("e2a6")
    assert position.fen == "r3k2r/p1ppqpb1/Bn2pnp1/3PN3/1p2P3/2N2Q2/PPPB1PpP/3RK2R b Kkq - 0 2"
    assert not position.make_move("e8c8")
    assert position.make_move("e8g8")
    assert position.fen == "r4rk1/p1ppqpb1/Bn2pnp1/3PN3/1p2P3/2N2Q2/PPPB1PpP/3RK2R w K - 1 3"
    position.undo_move()
    assert position.make_move("g2h1Q")
    assert position.fen == "r3k2r/p1ppqpb1/Bn2pnp1/3PN3/1p2P3/2N2Q2/PPPB1P1P/3RK2q w kq - 0 3"


def test_perf():
    def perft(position: Position, depth: int):
        if depth == 0:
            return 1

        nodes = 0
        for move in position.pseudo_legal_moves:
            if position.make_move(move):
                nodes += perft(position, depth - 1)
                position.undo_move()

        return nodes

    position = Position()
    assert perft(position, 3) == 8902

    position.fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
    assert perft(position, 2) == 2039

    position.fen = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
    assert perft(position, 3) == 2812

    position.fen = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
    assert perft(position, 3) == 9467
    position.fen = "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1"
    assert perft(position, 3) == 9467

    position.fen = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
    assert perft(position, 2) == 1486

    position.fen = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
    assert perft(position, 2) == 2079
