import pytest

from chess import Position, Move


def test_position():
    with pytest.raises(ValueError, match="invalid fen"):
        Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    position = Position()
    assert position.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    assert len(position.pseudo_legal_moves) == 20


def test_fen():
    position = Position()

    position.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert position.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    position.fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
    assert position.fen == "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"

    position.fen = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
    assert position.fen == "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"

    position.fen = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
    assert position.fen == "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"

    position.fen = "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1"
    assert position.fen == "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1"

    position.fen = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
    assert position.fen == "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"

    position.fen = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
    assert position.fen == "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"


def test_make_undo():
    moves = []
    irrev_infos = []
    position = Position("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2QK2R w KQkq - 0 1")

    # make
    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("f3e5"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k2r/Pppp1ppp/1b3nbN/nP2N3/BBP1P3/q7/Pp1P2PP/R2QK2R b KQkq - 1 1"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("f6g4"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k2r/Pppp1ppp/1b4bN/nP2N3/BBP1P1n1/q7/Pp1P2PP/R2QK2R w KQkq - 2 2"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("d1g4"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k2r/Pppp1ppp/1b4bN/nP2N3/BBP1P1Q1/q7/Pp1P2PP/R3K2R b KQkq - 0 2"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("b2a1q"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k2r/Pppp1ppp/1b4bN/nP2N3/BBP1P1Q1/q7/P2P2PP/q3K2R w Kkq - 0 3"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("e1e2"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k2r/Pppp1ppp/1b4bN/nP2N3/BBP1P1Q1/q7/P2PK1PP/q6R b kq - 1 3"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("h8g8"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k1r1/Pppp1ppp/1b4bN/nP2N3/BBP1P1Q1/q7/P2PK1PP/q6R w q - 2 4"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("d2d4"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k1r1/Pppp1ppp/1b4bN/nP2N3/BBPPP1Q1/q7/P3K1PP/q6R b q d3 0 4"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("c7c5"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k1r1/Pp1p1ppp/1b4bN/nPp1N3/BBPPP1Q1/q7/P3K1PP/q6R w q c6 0 5"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("b5c6"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "r3k1r1/Pp1p1ppp/1bP3bN/n3N3/BBPPP1Q1/q7/P3K1PP/q6R b q - 0 5"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("e8c8"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "2kr2r1/Pp1p1ppp/1bP3bN/n3N3/BBPPP1Q1/q7/P3K1PP/q6R w - - 1 6"

    pseudo_legal_moves = position.pseudo_legal_moves
    moves.append(pseudo_legal_moves[pseudo_legal_moves.index(Move.from_string("c6c7"))])
    irrev_infos.append(position.make_move(moves[-1]))
    assert position.fen == "2kr2r1/PpPp1ppp/1b4bN/n3N3/BBPPP1Q1/q7/P3K1PP/q6R b - - 0 6"

    # undo
    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "2kr2r1/Pp1p1ppp/1bP3bN/n3N3/BBPPP1Q1/q7/P3K1PP/q6R w - - 1 6"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k1r1/Pp1p1ppp/1bP3bN/n3N3/BBPPP1Q1/q7/P3K1PP/q6R b q - 0 5"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k1r1/Pp1p1ppp/1b4bN/nPp1N3/BBPPP1Q1/q7/P3K1PP/q6R w q c6 0 5"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k1r1/Pppp1ppp/1b4bN/nP2N3/BBPPP1Q1/q7/P3K1PP/q6R b q d3 0 4"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k1r1/Pppp1ppp/1b4bN/nP2N3/BBP1P1Q1/q7/P2PK1PP/q6R w q - 2 4"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k2r/Pppp1ppp/1b4bN/nP2N3/BBP1P1Q1/q7/P2PK1PP/q6R b kq - 1 3"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k2r/Pppp1ppp/1b4bN/nP2N3/BBP1P1Q1/q7/P2P2PP/q3K2R w Kkq - 0 3"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k2r/Pppp1ppp/1b4bN/nP2N3/BBP1P1Q1/q7/Pp1P2PP/R3K2R b KQkq - 0 2"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k2r/Pppp1ppp/1b4bN/nP2N3/BBP1P1n1/q7/Pp1P2PP/R2QK2R w KQkq - 2 2"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k2r/Pppp1ppp/1b3nbN/nP2N3/BBP1P3/q7/Pp1P2PP/R2QK2R b KQkq - 1 1"

    position.undo_move(moves.pop(), irrev_infos.pop())
    assert position.fen == "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2QK2R w KQkq - 0 1"
