import pytest

from chess import Board, Color, Square, Castling, Move


def test_str():
    board = Board()

    with pytest.raises(ValueError, match="invalid board string"):
        board.string = ""
    with pytest.raises(ValueError, match="invalid board string"):
        board.string = "8/8/8/8/8/8/8/7"

    assert repr(board) == "Board('8/8/8/8/8/8/8/8')"
    assert board.string == "8/8/8/8/8/8/8/8"
    assert board[Square("a1")] is None

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


def test_generate_moves():
    board = Board()

    # bishop
    board.string = "8/2p5/2P3p1/8/4B3/8/8/8"
    moves = board.generate_moves(Color(True))
    assert len(moves) == 9

    # rook
    board.string = "8/8/4P3/8/2p1r3/2P5/8/8"
    moves = board.generate_moves(Color(False))
    assert len(moves) == 9

    # queen
    board.string = "8/8/4p3/8/4Q3/2p5/2P5/8"
    moves = board.generate_moves(Color(True))
    assert len(moves) == 23

    # knight
    board.string = "8/5P2/8/6n1/4p3/4P3/8/8"
    moves = board.generate_moves(Color(False))
    assert len(moves) == 5

    # pawn
    board.string = "3q4/4P3/8/5Pp1/3p4/1p5p/P2P3P/8"
    moves = board.generate_moves(Color(True), epsquare=Square("g6"))
    assert len(moves) == 14

    # king
    board.string = "8/8/5p2/5P2/4k3/3p4/3P4/8"
    moves = board.generate_moves(Color(False))
    assert len(moves) == 7

    # is attacked
    board.string = "8/8/8/8/4b3/8/8/8"
    assert board.is_attacked(Color(False), Square("h1"))
    assert not board.is_attacked(Color(False), Square("h2"))

    # in check
    board.string = "8/8/3k4/2P5/4p3/4K3/8/8"
    assert not board.in_check(Color(True))
    assert board.in_check(Color(False))
    board.clear()
    assert not board.in_check(Color(True))

    # castle
    board.string = "r3k1nr/p6p/8/8/8/p6p/P5pP/RN2K2R"
    moves = board.generate_moves(Color(True), Castling("KQkq"))
    assert len(moves) == 10


def test_make_undo():
    board = Board()

    board.string = "3q4/4P3/8/5Pp1/3p4/1p5p/P2P3P/4K2R"
    moves = board.generate_moves(Color(True), Castling("K"), Square("g6"))

    # pawn move
    move = moves[moves.index(Move("d2d3"))]
    capture = board.make_move(Color(True), move)
    assert board.string == "3q4/4P3/8/5Pp1/3p4/1p1P3p/P6P/4K2R"
    board.undo_move(Color(True), move, capture)
    assert board.string == "3q4/4P3/8/5Pp1/3p4/1p5p/P2P3P/4K2R"

    # promotion
    move = moves[moves.index(Move("e7e8Q"))]
    capture = board.make_move(Color(True), move)
    assert board.string == "3qQ3/8/8/5Pp1/3p4/1p5p/P2P3P/4K2R"
    board.undo_move(Color(True), move, capture)
    assert board.string == "3q4/4P3/8/5Pp1/3p4/1p5p/P2P3P/4K2R"

    # promotion and capture
    move = moves[moves.index(Move("e7d8Q"))]
    capture = board.make_move(Color(True), move)
    assert board.string == "3Q4/8/8/5Pp1/3p4/1p5p/P2P3P/4K2R"
    board.undo_move(Color(True), move, capture)
    assert board.string == "3q4/4P3/8/5Pp1/3p4/1p5p/P2P3P/4K2R"

    # ep capture
    move = moves[moves.index(Move("f5g6"))]
    capture = board.make_move(Color(True), move)
    assert board.string == "3q4/4P3/6P1/8/3p4/1p5p/P2P3P/4K2R"
    board.undo_move(Color(True), move, capture)
    assert board.string == "3q4/4P3/8/5Pp1/3p4/1p5p/P2P3P/4K2R"

    # castle
    move = moves[moves.index(Move("e1g1"))]
    capture = board.make_move(Color(True), move)
    assert board.string == "3q4/4P3/8/5Pp1/3p4/1p5p/P2P3P/5RK1"
    board.undo_move(Color(True), move, capture)
    assert board.string == "3q4/4P3/8/5Pp1/3p4/1p5p/P2P3P/4K2R"
