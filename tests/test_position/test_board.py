import pytest

from chess import Board, Color, Square


def test_board():
    with pytest.raises(ValueError, match="invalid board string"):
        Board("")
    with pytest.raises(ValueError, match="invalid board string"):
        Board("8/8/8/8/8/8/8/7")

    board = Board()
    assert repr(board) == "8/8/8/8/8/8/8/8"

    board.string = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"
    assert board.string == "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"
    assert str(board) == """\
r . b k . . . r
p . . p B p N p
n . . . . n . .
. p . N P . . P
. . . . . . P .
. . . P . . . .
P . P . K . . .
q . . . . . b ."""

    # bishop
    board.string = "8/8/2p5/8/4B3/2p5/2P5/8"
    assert len(board.generate_pseudo_legal_moves(Color.WHITE)) == 9

    # rook
    board.string = "8/8/8/2P1r3/8/4p3/4P3/8"
    assert len(board.generate_pseudo_legal_moves(Color.BLACK)) == 9

    # queen
    board.string = "8/2p1p3/2P1P1p1/8/2p1Q3/8/8/8"
    assert len(board.generate_pseudo_legal_moves(Color.WHITE)) == 18

    # knight
    board.string = "8/5p2/5P2/4n3/8/3P4/8/8"
    assert len(board.generate_pseudo_legal_moves(Color.BLACK)) == 7

    # king
    board.string = "8/8/8/5p2/3pKP2/3P4/8/8"
    assert len(board.generate_pseudo_legal_moves(Color.WHITE)) == 6

    # pawn
    board.string = "7q/5PP1/8/3pP3/2P4p/P5p1/1P5P/8"
    assert len(board.generate_pseudo_legal_moves(Color.WHITE, Square.D6)) == 21

    # castling


def test_string():
    board = Board()

    board.string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    assert board.string == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    board.string = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R"
    assert board.string == "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R"

    board.string = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8"
    assert board.string == "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8"

    board.string = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1"
    assert board.string == "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1"

    board.string = "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R"
    assert board.string == "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R"

    board.string = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R"
    assert board.string == "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R"

    board.string = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1"
    assert board.string == "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1"
